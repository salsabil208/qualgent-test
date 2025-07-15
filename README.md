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
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [License](#license)

---

## Overview

This project implements:
- **A Python CLI tool (`qgjob`)** to submit and track test jobs.
- **A FastAPI backend** to queue, group, and schedule jobs by `app_version_id`, using Redis as a fast in-memory queue.
- **A worker/agent** that simulates picking up jobs, running tests, updating their statuses, retrying failed jobs, and prioritizing high-priority jobs.
- **A GitHub Actions workflow** for seamless CI integration.
- **Extensible architecture** ready for scaling, prioritization, retries, and fault-tolerance.

---

## Architecture

![Architecture Diagram](fig.png)

**Components:**
- **CLI Tool:** User-facing interface to submit/check test jobs.
- **Backend (FastAPI):** Receives jobs, groups jobs by `app_version_id`, tracks job status, and exposes REST endpoints.
- **Redis:** Efficient in-memory queue, supports grouping, batching, prioritization, and state persistence.
- **Worker/Agent:** Picks up jobs, runs simulated tests, updates status (queued, running, retrying, done, failed), and handles retries/faults.

---

## Features

- **Modular:** Clear separation between CLI, backend API, queue logic, and worker.
- **Efficient:** Batches jobs by app version to optimize device usage.
- **Prioritization:** Jobs with higher priority are processed first.
- **Retries:** Failed jobs are retried automatically up to a maximum number of attempts.
- **Fault-Tolerant:** Stuck jobs are re-queued for retry.
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
