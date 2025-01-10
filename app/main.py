from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import psycopg2
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Inicializar métricas de Prometheus
Instrumentator().instrument(app).expose(app)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    try:
        conn = get_db_connection()
        conn.close()
        return JSONResponse(content={"status": "healthy"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "unhealthy", "error": str(e)}, status_code=500)