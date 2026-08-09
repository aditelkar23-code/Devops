Requirement | Evidence
---|---
Working deployment | kubectl get pods -n devops-demo
Backend | k8s/backend.yaml, FastAPI app in app/main.py
Database dependency | k8s/postgres.yaml
Containerization | Dockerfile
CI/CD | .github/workflows/deploy.yml
Reliability | readiness/liveness probes in k8s/backend.yaml
Failure simulation | docs/failure-debugging.md (wrong DB password)
Debugging | kubectl logs/describe/events steps in docs/failure-debugging.md
Fix | Secret update and rollout restart procedure in docs/failure-debugging.md
Architecture | README Mermaid diagram
Tradeoffs | README "Production Tradeoffs" section
Video | docs/video-script.md
