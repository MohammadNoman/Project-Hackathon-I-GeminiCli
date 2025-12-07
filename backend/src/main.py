import logging
from pythonjsonlogger.jsonlogger import JsonFormatter

from fastapi import FastAPI, Depends, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import settings
from .database.database import get_db
from backend.src.models.chat import ChatRequest, ChatResponse
from backend.src.services.rag_service import get_rag_response
from backend.src.api import auth, personalization, localization

# ... (Logging setup) ...

# ... (App setup) ...

# Include Routers
app.include_router(auth.router)
app.include_router(personalization.router)
app.include_router(localization.router)

# ... (Logging setup) ...

# ... (App setup) ...

# Include Routers
app.include_router(auth.router)
app.include_router(personalization.router)

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

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)

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

# Chatbot endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_with_rag(request: ChatRequest):
    root_logger.info(f"Chat request received: {request.query}", extra={"conversation_id": request.conversation_id})
    try:
        # Assuming a default collection name for now. This could be configurable.
        collection_name = "textbook_content" 
        response_content, source_chunks = get_rag_response(request.query, collection_name, request.context_snippet)
        
        return ChatResponse(response=response_content, source_chunks=source_chunks)
    except Exception as e:
        root_logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Basic monitoring endpoint placeholder
@app.get("/metrics")
async def get_metrics():
    # In a real application, this would expose Prometheus metrics
    # For example, using a library like 'prometheus_client'
    # metrics_data = generate_latest(registry).decode('utf-8')
    # return Response(content=metrics_data, media_type="text/plain")
    return {"message": "Metrics endpoint (to be integrated with Prometheus)"}


