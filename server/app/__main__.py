from fastapi import FastAPI, exceptions, openapi

from app.config import get_settings
from app.endpoints import list_of_routes
from app.schemas.application import ErrorResponse
from app.services import FileStorageService, ModelVideo2Frames
from app.utils.application import validation_exception_handler


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Project for detection duplicate "

    tags_metadata = [
        {
            "name": "duplicate_detector",
            "description": description,
        },
    ]

    application = FastAPI(
        title="app",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi.json",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application)
    application.state.settings = settings
    application.add_exception_handler(
        exceptions.RequestValidationError,
        validation_exception_handler,
    )
    application.state.file_service = FileStorageService()
    application.state.video_detection_service = ModelVideo2Frames()
    openapi.utils.validation_error_response_definition = ErrorResponse.schema()
    return application


app = get_app()
