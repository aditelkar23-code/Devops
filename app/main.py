import os
import psycopg2
from psycopg2 import OperationalError
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="DevOps Challenge API")


@app.get("/")
def root():
    return {"application": "DevOps Challenge API", "status": "running"}


@app.get("/health")
def health():
    """A lightweight health endpoint used by Kubernetes liveness/readiness probes.
    This must NOT require the database to be available.
    """
    return {"status": "healthy"}


@app.get("/db-health")
def db_health():
    """Checks connectivity to PostgreSQL by executing a simple SELECT 1.

    Expects DB_HOST, DB_NAME, DB_USER, DB_PASSWORD environment variables.
    Returns HTTP 200 with a small JSON payload on success, or HTTP 503 on failure.
    """
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not all([db_host, db_name, db_user, db_password]):
        raise HTTPException(status_code=503, detail="Database environment variables are not fully set")

    try:
        # Short connection timeout so the request fails fast if DB is unreachable
        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            connect_timeout=5,
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result and result[0] == 1:
            return JSONResponse(status_code=200, content={"db": "ok"})
        else:
            raise HTTPException(status_code=503, detail="Unexpected database response")

    except OperationalError as e:
        # PostgreSQL connection/authentication errors surface here
        raise HTTPException(status_code=503, detail=f"Database connection failed: {e}")
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=503, detail=f"Database error: {e}")
