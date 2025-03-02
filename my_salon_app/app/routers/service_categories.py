from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.database import get_db
from app.models import ServiceCategory
from app.schemas import ServiceCategoryCreate, ServiceCategoryUpdate, ServiceCategoryResponse, ServiceCategoryListResponse

router = APIRouter(
    prefix="/service-categories",
    tags=["service categories"]
)

@router.post("", response_model=ServiceCategoryResponse)
async def create_service_category(category: ServiceCategoryCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new service category.
    """
    # Check if category with same name already exists
    existing_result = await db.execute(select(ServiceCategory).filter(ServiceCategory.name == category.name))
    existing_category = existing_result.scalars().first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Service category with this name already exists")
    
    # Create category
    db_category = ServiceCategory(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.get("", response_model=ServiceCategoryListResponse)
async def read_service_categories(
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve service categories with optional filtering.
    """
    query = select(ServiceCategory)
    
    # Apply filters if provided
    if name:
        query = query.filter(ServiceCategory.name.ilike(f"%{name}%"))
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    categories = result.scalars().all()
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(ServiceCategory)
    if name:
        count_query = count_query.filter(ServiceCategory.name.ilike(f"%{name}%"))
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": categories, "total": total}

@router.get("/{category_id}", response_model=ServiceCategoryResponse)
async def read_service_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific service category by ID.
    """
    result = await db.execute(select(ServiceCategory).filter(ServiceCategory.id == category_id))
    category = result.scalars().first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="Service category not found")
    
    return category

@router.put("/{category_id}", response_model=ServiceCategoryResponse)
async def update_service_category(
    category_id: int, 
    category: ServiceCategoryUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update a service category.
    """
    result = await db.execute(select(ServiceCategory).filter(ServiceCategory.id == category_id))
    db_category = result.scalars().first()
    
    if db_category is None:
        raise HTTPException(status_code=404, detail="Service category not found")
    
    # Check if updating to a name that already exists
    if category.name is not None and category.name != db_category.name:
        existing_result = await db.execute(select(ServiceCategory).filter(ServiceCategory.name == category.name))
        existing_category = existing_result.scalars().first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Service category with this name already exists")
    
    # Update only the fields that are provided
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", response_model=dict)
async def delete_service_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a service category.
    """
    result = await db.execute(select(ServiceCategory).filter(ServiceCategory.id == category_id))
    category = result.scalars().first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="Service category not found")
    
    await db.delete(category)
    await db.commit()
    
    return {"message": "Service category deleted successfully"} 