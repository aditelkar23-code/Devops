1. Final Verification

This document maps each requirement to evidence and status (Pending / Manual / Automated / Verified).

Requirement | Evidence | Status
---|---|---
Backend exists | k8s/backend.yaml | Verified (deployed to local Kind cluster)
PostgreSQL exists | k8s/postgres.yaml | Verified (deployed to local Kind cluster)
Docker image builds | Dockerfile | Verified (local image devops-backend:local built)
Kubernetes cluster works | Kind cluster 'devops-challenge' | Verified (cluster created locally)
Backend deploys | k8s/backend.yaml | Verified (backend Deployment rolled out, 2 replicas Running)
PostgreSQL deploys | k8s/postgres.yaml | Verified (postgres pod Running and Ready)
Services work | kubectl get services -n devops-demo | Verified (backend and postgres ClusterIP services exist)
/health works | app/main.py and tests/test_health.py | Verified (unit test passed and /health returned 200 in-cluster)
/db-health works | app/main.py | Verified (returned 200 when secret correct)
Readiness probe exists | k8s/backend.yaml readinessProbe | Verified (confirmed on Deployment)
Liveness probe exists | k8s/backend.yaml livenessProbe | Verified (confirmed on Deployment)
Resource requests/limits exist | k8s/backend.yaml & k8s/postgres.yaml | Verified (confirmed on Deployment)
2 replicas exist | k8s/backend.yaml replicas: 2 | Verified (2 replicas running)
RollingUpdate exists | k8s/backend.yaml strategy RollingUpdate | Verified (rollingUpdate maxUnavailable=0 maxSurge=1)
GitHub Actions workflow exists | .github/workflows/deploy.yml | Verified (file present; not executed here)
Docker Hub integration exists | deploy.yml uses docker/login-action and pushes image | Verified (file present; requires secrets to run)
Intentional failure reproducible | docs/failure-debugging.md | Verified (simulated wrong DB password in-cluster produced HTTP 503 from /db-health)
Failure diagnosable via kubectl | docs/failure-debugging.md | Verified (pod logs showed authentication error; kubectl describe/gets provided evidence)
Failure fixable | docs/failure-debugging.md | Verified (restoring secret and rollout restart returned system to healthy state)
Application returns healthy state after fix | Verified
README accurate | README.md | Verified (file content reviewed)
Video script covers requirements | docs/video-script.md | Verified (file content reviewed)

Notes:
- All verification steps above were executed locally using Kind and Docker on this Windows host.
- The GitHub Actions workflow and Docker Hub push were validated for correctness (YAML and placeholders) but not executed here because credentials are not provided and pushes were not requested.
- Secrets used locally are demo values; do not commit production credentials. In production use external secret management, persistent storage, backups, and managed Postgres.
- To reproduce the intentional failure during your recorded demo, follow docs/failure-debugging.md; commands are provided there.
