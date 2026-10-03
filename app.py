# FastAPI entry point.

from fastapi import FastAPI, Request

from api.routes import router
from api.ready_to_post_routes import router as ready_to_post_router
from fastapi.exceptions import RequestValidationError
from middleware.error_handler import generic_exception_handler, validation_exception_handler

app = FastAPI(title="Social Campaign Generator API")

app.include_router(router)
app.include_router(ready_to_post_router)

app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.api_route("/", methods=["GET", "HEAD"])
def root(request: Request):
    """
        Return a welcome message with the link to the API docs.
    """
    return {
        "message": "Welcome to the API. Visit the link below to try it out.",
        "docs_url": f"{request.base_url}docs"
    }