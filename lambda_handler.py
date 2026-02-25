"""AWS Lambda handler for FastAPI application."""
import os
from mangum import Mangum

# Create /tmp directories (Lambda writable storage)
os.makedirs("/tmp/uploads", exist_ok=True)
os.makedirs("/tmp/cached_chunks", exist_ok=True)

# Import app AFTER directories are created
from app.main import app, initialize_services

# ✅ Correct Mangum handler for Lambda Function URL
_handler = Mangum(app, lifespan="off")

_services_initialized = False

def handler(event, context):
    """
    Lambda handler with lazy service initialization.
    """
    global _services_initialized

    if not _services_initialized:
        initialize_services()
        _services_initialized = True

    return _handler(event, context)