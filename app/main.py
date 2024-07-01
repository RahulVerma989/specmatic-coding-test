from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import json
from .routes import router

app = FastAPI(
    title="Products API",
    description="This API manages a catalog of products, allowing for operations such as listing, creating, updating, and deleting products.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Products",
            "description": "Operations related to product management."
        },
        {
            "name": "Admin",
            "description": "Administrative operations such as updating and deleting products, accessible only to admin users."
        }
    ]
)

app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles validation errors thrown when request data does not conform to expected schemas.

    Args:
        request (Request): The request object that led to the validation error.
        exc (RequestValidationError): The exception object containing details about what went wrong.

    Returns:
        JSONResponse: A JSON response that includes the timestamp, error details, HTTP status, and the path of the request.
    """
    # Generate a timestamp
    timestamp = datetime.now().isoformat()
    # Extract details for each error
    errors = [{'loc': e['loc'], 'msg': e['msg'], 'type': e['type']} for e in exc.errors()]
    # Prepare the response body according to the ErrorResponseBody schema
    content = {
        "timestamp": timestamp,
        "status": 400,
        "error": json.dumps(errors),  # Convert list of errors to a JSON string
        "path": request.url.path
    }
    return JSONResponse(
        status_code=400,
        content=content
    )