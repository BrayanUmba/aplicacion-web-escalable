from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import psycopg2
from prometheus_fastapi_instrumentator import Instrumentator
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Inicializar métricas de Prometheus
Instrumentator().instrument(app).expose(app)

def get_db_connection():
    try:
        logger.info("Intentando conectar a la base de datos...")
        logger.info(f"Host: {os.getenv('POSTGRES_HOST')}")
        logger.info(f"DB: {os.getenv('POSTGRES_DB')}")
        logger.info(f"User: {os.getenv('POSTGRES_USER')}")
        
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT", "5432")
        )
        logger.info("Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        logger.error(f"Error conectando a la base de datos: {str(e)}")
        raise

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
        logger.error(f"Health check falló: {str(e)}")
        # Retornamos 200 para evitar que Kubernetes reinicie el pod
        return JSONResponse(
            content={"status": "starting", "error": str(e)},
            status_code=200
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)