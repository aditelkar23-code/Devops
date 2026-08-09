Failure debugging live demo

This document describes an intentional failure (incorrect PostgreSQL password) and a step-by-step debugging workflow.

Symptom

- After rolling out a backend deployment with a bad DB password, the backend fails to become Ready or /db-health returns HTTP 503.

Evidence to gather

- Which pods are failing?  kubectl get pods -n devops-demo
- Pod events and descriptions: kubectl describe pod <pod> -n devops-demo
- Container logs: kubectl logs <pod> -n devops-demo
- Cluster events (most recent first): kubectl get events -n devops-demo --sort-by=.lastTimestamp

Hypothesis

- The backend cannot authenticate to PostgreSQL because the password in the Kubernetes Secret is incorrect.

Investigation steps

1) Verify application pod status:
   kubectl get pods -n devops-demo
   - This shows Ready/Restarts and Pod status.

2) Describe a failing pod to see recent events and reasons:
   kubectl describe pod <backend-pod> -n devops-demo
   - Look for backoff, CrashLoopBackOff, or probe failures. Events show env, mount, and image pull errors.

3) Inspect logs for the backend container:
   kubectl logs <backend-pod> -n devops-demo
   - The FastAPI /db-health handler reports database connection errors. Look for authentication errors like "password authentication failed for user".

4) Inspect PostgreSQL pod logs if needed:
   kubectl logs <postgres-pod> -n devops-demo
   - Postgres logs will show failed authentication attempts with client IPs and user names.

5) Inspect the Secret value (for demo purposes only):
   kubectl get secret postgres-secret -n devops-demo -o yaml
   kubectl get secret postgres-secret -n devops-demo -o jsonpath="{.data.DB_PASSWORD}" | base64 --decode
   - Confirm the value matches the password expected by Postgres (shown in the Postgres pod env on creation).

Root cause

- The Kubernetes Secret contained an incorrect DB_PASSWORD; the backend attempted connections using the wrong password and Postgres rejected authentication.

Fix

1) Update the Kubernetes Secret with the correct password:
   kubectl create secret generic postgres-secret \
     --from-literal=DB_USER=appuser \
     --from-literal=DB_PASSWORD=<correct-password> \
     --from-literal=DB_NAME=appdb -n devops-demo --dry-run=client -o yaml | kubectl apply -f -

2) Rollout the backend to pick up the new secret (environment variables are injected at container start):
   kubectl rollout restart deployment/backend -n devops-demo

Verification

1) Check pod status:
   kubectl get pods -n devops-demo

2) Wait for backend rollout to complete:
   kubectl rollout status deployment/backend -n devops-demo

3) Verify health endpoint:
   kubectl port-forward svc/backend 8080:80 -n devops-demo &
   curl -f http://127.0.0.1:8080/health

4) Verify DB connectivity:
   curl -f http://127.0.0.1:8080/db-health

Notes on methodology

- Symptom -> Evidence -> Hypothesis -> Investigation -> Root cause -> Fix -> Verification.
- Each kubectl command is chosen to reveal a specific piece of evidence (pod status, events, logs, Secret contents).
- Do not hardcode credentials into manifests in production; use an external secret manager.
