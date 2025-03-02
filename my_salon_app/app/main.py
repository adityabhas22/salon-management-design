from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from .database import get_db
from . import models

# Initialize FastAPI app
app = FastAPI(
    title="Salon Management API",
    description="API for managing a Spa/Salon with appointments, CRM, promotions, feedback, and more.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Import routers
from .routers import customers, staff, services, appointments, feedback, promotions, knowledge_base, service_categories

# Include routers
app.include_router(customers.router, prefix="/api", tags=["customers"])
app.include_router(staff.router, prefix="/api", tags=["staff"])
app.include_router(services.router, prefix="/api", tags=["services"])
app.include_router(service_categories.router, prefix="/api", tags=["service_categories"])
app.include_router(appointments.router, prefix="/api", tags=["appointments"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])
app.include_router(promotions.router, prefix="/api", tags=["promotions"])
app.include_router(knowledge_base.router, prefix="/api", tags=["knowledge_base"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Salon Management API"}

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Try to execute a simple query to check database connection
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
