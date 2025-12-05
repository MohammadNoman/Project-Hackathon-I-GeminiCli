import logging
from pythonjsonlogger.jsonlogger import JsonFormatter

from fastapi import FastAPI, Depends, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .config import settings
from .database.database import get_db

# Configure structured logging
# Get the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove existing handlers to prevent duplicate logs
if root_logger.hasHandlers():
    root_logger.handlers.clear()

# Create a handler
handler = logging.StreamHandler()

# Create a JsonFormatter
# The format string defines the fields to be included in the JSON log
formatter = JsonFormatter('%(levelname)s %(asctime)s %(name)s %(message)s')
handler.setFormatter(formatter)

# Add the handler to the root logger
root_logger.addHandler(handler)

# For uvicorn access logs to also be structured (requires uvicorn config or custom logger)
# For now, this ensures application-level logs are structured.

app = FastAPI()

# Global Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    root_logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}", extra={"status_code": exc.status_code, "detail": exc.detail})
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    root_logger.error(f"Unhandled Exception: {exc}", exc_info=True, extra={"detail": str(exc)})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred."},
    )


@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    root_logger.info("Root endpoint accessed", extra={"custom_field": "some_value"})
    return {"message": "Welcome to FastAPI Backend!", "openai_key_loaded": bool(settings.OPENAI_API_KEY)}

# Basic monitoring endpoint placeholder
@app.get("/metrics")
async def get_metrics():
    # In a real application, this would expose Prometheus metrics
    # For example, using a library like 'prometheus_client'
    # metrics_data = generate_latest(registry).decode('utf-8')
    # return Response(content=metrics_data, media_type="text/plain")
    return {"message": "Metrics endpoint (to be integrated with Prometheus)"}


