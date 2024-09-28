from app.endpoints.detecting import api_router as detection_router
from app.endpoints.ping import api_router as application_health_router


list_of_routes = [
    detection_router,
    application_health_router,
]


__all__ = [
    "list_of_routes",
]
