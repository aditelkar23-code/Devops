Video script — 8–12 minutes

SECTION 1 — LIVE DEMO (3–4 minutes)

- Intro (10–15s): "This demo shows a minimal FastAPI app, deployed to a Kind cluster using GitHub Actions. We'll show health endpoints and DB connectivity."

- Show repository tree briefly (10s).

- Show Kind cluster and pods:
  - kubectl get pods -n devops-demo
  - kubectl get svc -n devops-demo

- Show backend /health working:
  - kubectl port-forward svc/backend 8080:80 -n devops-demo &
  - curl http://127.0.0.1:8080/health

- Show /db-health (connected):
  - curl http://127.0.0.1:8080/db-health

SECTION 2 — ARCHITECTURE (2–3 minutes)

- Explain the flow: developer → GitHub → GitHub Actions → Docker Hub + Kind → Kubernetes → FastAPI + Postgres.
- Explain key components: Dockerfile, Kubernetes manifests, GitHub Actions workflow.
- Explain the reliability improvement: readiness and liveness probes protect the service and allow Kubernetes to restart unhealthy containers.

SECTION 3 — FAILURE DEBUGGING (2–3 minutes)

- Show the intentional failure: update the Secret with a wrong DB password and rollout the backend.
- Show kubectl get pods and identify failing pods.
- kubectl describe pod <pod> and kubectl logs <pod>
- Show Postgres auth failure in logs and secret mismatch.
- Fix the secret and rollout restart the deployment; show recovery and /db-health success.

SECTION 4 — TRADEOFFS (1–2 minutes)

- Explain simplifications: Kind used for CI demo, single Postgres replica, demo Secret in repo (for challenge only).
- Explain what production would require: managed DB, persistent storage, external secrets, monitoring, scaling, HA.

Closing (10–15s)

- Recap and point viewer to README and docs for exact commands.
