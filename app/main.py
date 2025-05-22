from fastapi import FastAPI
from .api.endpoints.credentials import router as credentials_router
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import check_db_connection, Base, engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Credentials API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables before the application starts
@app.on_event("startup")
async def startup_event():
    try:
        # Create tables
        logger.info("Creating database tables...")
        # Base.metadata.drop_all(bind=engine)  # Drop existing tables
        Base.metadata.create_all(bind=engine)  # Create new tables
        
        # Check database connection
        db_connected = await check_db_connection()
        if not db_connected:
            logger.error("Failed to connect to the database. Shutting down...")
            exit(1)
        logger.info("Application started successfully!")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        exit(1)

app.include_router(
    credentials_router,
    prefix=f"{settings.API_V1_STR}/credentials",
    tags=["credentials"]
)