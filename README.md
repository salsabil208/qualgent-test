# QualGent Backend Coding Challenge

A modular, scalable backend and CLI solution for orchestrating AppWright end-to-end tests across local devices, emulators, and BrowserStack.

---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Setup & Installation](#setup--installation)
- [How It Works](#how-it-works)
- [Running an End-to-End Test](#running-an-end-to-end-test)
- [GitHub Actions Integration](#github-actions-integration)
- [Extensibility & Bonus Features](#extensibility--bonus-features)

---

## Overview

This project implements:
- **A Python CLI tool (`qgjob`)** to submit and track test jobs.
- **A FastAPI backend** to queue, group, and schedule jobs by `app_version_id`, using Redis as a fast in-memory queue.
- **A simple worker/agent** that simulates picking up jobs, running tests, and updating their statuses.
- **A GitHub Actions workflow** for seamless CI integration.
- **Extensible architecture** ready for scaling, prioritization, and retries.

---

## Architecture

![Architecture Diagram](docs/architecture.png)

**Components:**
- **CLI Tool:** User-facing interface to submit/check test jobs.
- **Backend (FastAPI):** Receives jobs, groups jobs by `app_version_id`, and tracks job status.
- **Redis:** Efficient job queue, supports grouping and batching.
- **Worker/Agent:** (Simulated) picks up jobs, runs tests, and updates status.

---

## Features

- **Modular:** Clear separation between CLI, backend API, queue logic, and worker.
- **Efficient:** Batches jobs by app version to optimize device usage.
- **Scalable:** Easily extended to support multiple agents and horizontal scaling.
- **Developer-Friendly:** Simple CLI, clear docs, and CI integration.

---

## Setup & Installation

### Prerequisites
- Python 3.12+
- Redis (locally or via Docker)

### Clone the Repo
```sh
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
