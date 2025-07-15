import click
import requests

API_URL = "http://127.0.0.1:8000"  # Update if your backend runs elsewhere

@click.group()
def cli():
    """qgjob CLI tool for submitting and checking test jobs."""
    pass

@cli.command()
@click.option("--org-id", required=True, help="Organization ID")
@click.option("--app-version-id", required=True, help="App version ID")
@click.option("--test", "test_path", required=True, help="Test path (e.g., tests/onboarding.spec.js)")
@click.option("--priority", default=0, show_default=True, help="Job priority")
@click.option("--target", required=True, type=click.Choice(["emulator", "device", "browserstack"]), help="Target device")
def submit(org_id, app_version_id, test_path, priority, target):
    """Submit a test job."""
    payload = {
        "org_id": org_id,
        "app_version_id": app_version_id,
        "test_path": test_path,
        "priority": priority,
        "target": target
    }
    try:
        response = requests.post(f"{API_URL}/jobs/submit", json=payload)
        response.raise_for_status()
        data = response.json()
        click.echo(f"Job submitted! job_id: {data['job_id']}")
    except Exception as e:
        click.echo(f"Failed to submit job: {e}")

@cli.command()
@click.option("--job-id", required=True, help="Job ID to check status for")
def status(job_id):
    """Check the status of a submitted job."""
    try:
        response = requests.get(f"{API_URL}/jobs/status/{job_id}")
        response.raise_for_status()
        data = response.json()
        click.echo(f"Job Status for {job_id}: {data}")
    except requests.HTTPError as http_err:
        if response.status_code == 404:
            click.echo("Job not found.")
        else:
            click.echo(f"HTTP error: {http_err}")
    except Exception as e:
        click.echo(f"Failed to check job status: {e}")

if __name__ == "__main__":
    cli()
