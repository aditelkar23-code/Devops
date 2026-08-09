# DevOps Engineer Infrastructure Challenge

## Overview

This repository implements a minimal FastAPI application, containerized and deployed to a local Kubernetes cluster (Kind) via a GitHub Actions CI/CD pipeline. The goal is to demonstrate containerization, Kubernetes deployment, CI/CD, one reliability improvement (readiness/liveness probes), intentional failure simulation, and operational debugging.

## Architecture

flowchart TD
  DEV[Developer] --> GH[GitHub]
  GH --> GA[GitHub Actions]
  GA --> BUILD[Docker Build]
  BUILD --> REG[Docker Hub]
  GA --> K8S[Kind Kubernetes]
  K8S --> BACKEND[FastAPI Backend]
  K8S --> DB[PostgreSQL]
  BACKEND --> SERVICE[Backend Service]
  BACKEND --> PG_SERVICE[PostgreSQL Service]
  PG_SERVICE --> DB

(See docs for a textual explanation of each component.)

## Components

- Docker: Containerizes the FastAPI application.
- Kubernetes (Kind): Runs Postgres and the FastAPI backend locally for demo.
- GitHub Actions: Runs tests, builds and pushes Docker images, creates a Kind cluster, deploys manifests, and performs rollout verification and smoke tests.
- PostgreSQL: Simple single-replica Postgres 16 deployment for the app database.

## Project structure

```
devops-challenge/
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── requirements-dev.txt
├── tests/
│   └── test_health.py
├── k8s/
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── postgres.yaml
│   └── backend.yaml
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docs/
│   ├── failure-debugging.md
│   ├── video-script.md
│   └── checklist.md
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Prerequisites (local)

- Docker
- kind
- kubectl
- git
- Python 3.12 (for running tests locally)
- Docker Hub account (for CI push)
- GitHub account (to run CI)

## Local development

1. Create virtualenv and install dependencies:

   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r app/requirements.txt -r app/requirements-dev.txt

2. Run the app locally:

   uvicorn app.main:app --host 0.0.0.0 --port 8000

3. Run tests:

   pytest

## Docker

Build the image locally:

  docker build -t <yourhubuser>/devops-backend:local -f Dockerfile .

Run the container:

  docker run --rm -p 8000:8000 -e DB_HOST=postgres -e DB_NAME=appdb -e DB_USER=appuser -e DB_PASSWORD=password <yourhubuser>/devops-backend:local

## Kubernetes (Kind)

Create a cluster and deploy (local demo):

  kind create cluster --name devops-challenge
  kubectl apply -f k8s/namespace.yaml
  kubectl apply -f k8s/secret.yaml
  kubectl apply -f k8s/postgres.yaml
  # Replace placeholder image in k8s/backend.yaml with your image tag before applying
  sed "s|YOUR_DOCKERHUB_USERNAME/devops-backend:latest|<yourhubuser>/devops-backend:<git-sha>|g" k8s/backend.yaml > /tmp/backend.yaml
  kubectl apply -f /tmp/backend.yaml

  # On Windows, use Git Bash / WSL for the sed command, or copy k8s/backend.yaml and update the image value manually.

Port-forward to test the service locally:

  kubectl port-forward svc/backend 8080:80 -n devops-demo

Then visit:

  http://localhost:8080/
  http://localhost:8080/health
  http://localhost:8080/db-health

## CI/CD (GitHub Actions)

The GitHub Actions workflow builds and pushes a Docker image to Docker Hub and performs an automated deployment into a ephemeral Kind cluster inside the runner. It requires the following GitHub Secrets:

- DOCKERHUB_USERNAME — your Docker Hub username
- DOCKERHUB_TOKEN — a Docker Hub access token or password

Notes:
- The CI demonstrates the flow (build, push, deploy, verify) inside a runner using Kind. This is not a persistent production cluster — it's ephemeral and for CI validation only.

## Reliability improvement: readiness & liveness probes

The backend deployment includes both readiness and liveness HTTP probes that call `/health`.

Why:
- Readiness prevents a pod that is still initializing or not ready (for example, missing dependencies) from receiving traffic.
- Liveness allows Kubernetes to detect and restart containers that are in a bad state.

Tradeoffs:
- Poorly configured probes may cause unnecessary restarts or keep traffic from reaching containers during a normal slow startup; choose conservative timeouts and thresholds.

## Intentional failure

An intentional failure scenario is provided in docs/failure-debugging.md: set the Kubernetes Secret DB_PASSWORD to an incorrect value and observe the backend fail to connect to Postgres. The docs include exact kubectl commands for investigation and remediation.

## Future improvements (production)

- Use a managed database with persistent storage, backups, and HA.
- Use external secret management (Vault, cloud KMS) instead of committing demo secrets.
- Add monitoring, logging, autoscaling, image scanning and signing, and RBAC hardening.


---

For detailed steps, debugging commands and the video script see the docs/ folder.
