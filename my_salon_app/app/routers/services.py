from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.database import get_db
from app.models import Service, ServiceCategory
from app.schemas import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceListResponse

router = APIRouter(
    prefix="/services",
    tags=["services"]
)

@router.post("", response_model=ServiceResponse)
async def create_service(service: ServiceCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new service.
    """
    # Verify category exists if provided
    if service.category_id:
        category_result = await db.execute(select(ServiceCategory).filter(ServiceCategory.id == service.category_id))
        category = category_result.scalars().first()
        if not category:
            raise HTTPException(status_code=404, detail="Service category not found")
    
    # Create service
    db_service = Service(**service.model_dump())
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service

@router.get("", response_model=ServiceListResponse)
async def read_services(
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    duration: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve services with optional filtering.
    """
    query = select(Service)
    
    # Apply filters if provided
    if name:
        query = query.filter(Service.name.ilike(f"%{name}%"))
    if category_id:
        query = query.filter(Service.category_id == category_id)
    if min_price is not None:
        query = query.filter(Service.price >= min_price)
    if max_price is not None:
        query = query.filter(Service.price <= max_price)
    if duration:
        query = query.filter(Service.duration_minutes == duration)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    services = result.scalars().all()
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(Service)
    if name:
        count_query = count_query.filter(Service.name.ilike(f"%{name}%"))
    if category_id:
        count_query = count_query.filter(Service.category_id == category_id)
    if min_price is not None:
        count_query = count_query.filter(Service.price >= min_price)
    if max_price is not None:
        count_query = count_query.filter(Service.price <= max_price)
    if duration:
        count_query = count_query.filter(Service.duration_minutes == duration)
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": services, "total": total}

@router.get("/{service_id}", response_model=ServiceResponse)
async def read_service(service_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific service by ID.
    """
    result = await db.execute(select(Service).filter(Service.id == service_id))
    service = result.scalars().first()
    
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return service

@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int, 
    service: ServiceUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update a service.
    """
    result = await db.execute(select(Service).filter(Service.id == service_id))
    db_service = result.scalars().first()
    
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Verify category exists if provided
    if service.category_id is not None:
        category_result = await db.execute(select(ServiceCategory).filter(ServiceCategory.id == service.category_id))
        category = category_result.scalars().first()
        if not category:
            raise HTTPException(status_code=404, detail="Service category not found")
    
    # Update only the fields that are provided
    update_data = service.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    
    await db.commit()
    await db.refresh(db_service)
    return db_service

@router.delete("/{service_id}", response_model=dict)
async def delete_service(service_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a service.
    """
    result = await db.execute(select(Service).filter(Service.id == service_id))
    service = result.scalars().first()
    
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    await db.delete(service)
    await db.commit()
    
    return {"message": "Service deleted successfully"}

@router.get("/category/{category_id}", response_model=ServiceListResponse)
async def get_services_by_category(
    category_id: int, 
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all services in a specific category.
    """
    # Verify category exists
    category_result = await db.execute(select(ServiceCategory).filter(ServiceCategory.id == category_id))
    category = category_result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Service category not found")
    
    # Get services in category
    query = select(Service).filter(Service.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(query)
    services = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(Service).filter(Service.category_id == category_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": services, "total": total}
