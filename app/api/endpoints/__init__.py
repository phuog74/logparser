from .credentials import router as credentials_router

# Export routers để có thể import trực tiếp từ app.api.endpoints
__all__ = ["credentials_router"]