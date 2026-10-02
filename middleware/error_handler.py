# Error handlers for the API that return a clean JSON error message instead of a raw traceback.

from fastapi import Request
from fastapi.responses import JSONResponse


async def generic_exception_handler(request: Request, exc: Exception):
    """
        Catches any unhandled exception and returns a 500 error response.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Something went wrong while generating the campaign.",
            "detail": str(exc),
        },
    )


async def validation_exception_handler(request: Request, exc: Exception):
    """
        Catches request validation errors and returns a 400 error response.
    """
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid input.",
            "detail": str(exc),
        },
    )