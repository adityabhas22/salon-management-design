from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import Promotion, Service
from app.schemas import PromotionCreate, PromotionUpdate, PromotionResponse, PromotionListResponse

router = APIRouter(
    prefix="/promotions",
    tags=["promotions"]
)

@router.post("", response_model=PromotionResponse)
async def create_promotion(promotion: PromotionCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new promotion.
    """
    # Verify service exists if provided
    if promotion.service_id:
        service_result = await db.execute(select(Service).filter(Service.id == promotion.service_id))
        service = service_result.scalars().first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
    
    # Create promotion
    db_promotion = Promotion(**promotion.model_dump())
    db.add(db_promotion)
    await db.commit()
    await db.refresh(db_promotion)
    return db_promotion

@router.get("", response_model=PromotionListResponse)
async def read_promotions(
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
    service_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve promotions with optional filtering.
    """
    query = select(Promotion)
    
    # Apply filters if provided
    if name:
        query = query.filter(Promotion.name.ilike(f"%{name}%"))
    if is_active is not None:
        current_date = datetime.now().date()
        if is_active:
            query = query.filter(
                (Promotion.start_date <= current_date) & 
                ((Promotion.end_date >= current_date) | (Promotion.end_date.is_(None)))
            )
        else:
            query = query.filter(
                (Promotion.end_date < current_date) | 
                (Promotion.start_date > current_date)
            )
    if service_id:
        query = query.filter(Promotion.service_id == service_id)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    promotions = result.scalars().all()
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(Promotion)
    if name:
        count_query = count_query.filter(Promotion.name.ilike(f"%{name}%"))
    if is_active is not None:
        current_date = datetime.now().date()
        if is_active:
            count_query = count_query.filter(
                (Promotion.start_date <= current_date) & 
                ((Promotion.end_date >= current_date) | (Promotion.end_date.is_(None)))
            )
        else:
            count_query = count_query.filter(
                (Promotion.end_date < current_date) | 
                (Promotion.start_date > current_date)
            )
    if service_id:
        count_query = count_query.filter(Promotion.service_id == service_id)
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": promotions, "total": total}

@router.get("/{promotion_id}", response_model=PromotionResponse)
async def read_promotion(promotion_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific promotion by ID.
    """
    result = await db.execute(select(Promotion).filter(Promotion.id == promotion_id))
    promotion = result.scalars().first()
    
    if promotion is None:
        raise HTTPException(status_code=404, detail="Promotion not found")
    
    return promotion

@router.put("/{promotion_id}", response_model=PromotionResponse)
async def update_promotion(
    promotion_id: int, 
    promotion: PromotionUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update a promotion.
    """
    result = await db.execute(select(Promotion).filter(Promotion.id == promotion_id))
    db_promotion = result.scalars().first()
    
    if db_promotion is None:
        raise HTTPException(status_code=404, detail="Promotion not found")
    
    # Verify service exists if provided
    if promotion.service_id is not None:
        service_result = await db.execute(select(Service).filter(Service.id == promotion.service_id))
        service = service_result.scalars().first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
    
    # Update only the fields that are provided
    update_data = promotion.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_promotion, key, value)
    
    await db.commit()
    await db.refresh(db_promotion)
    return db_promotion

@router.delete("/{promotion_id}", response_model=dict)
async def delete_promotion(promotion_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a promotion.
    """
    result = await db.execute(select(Promotion).filter(Promotion.id == promotion_id))
    promotion = result.scalars().first()
    
    if promotion is None:
        raise HTTPException(status_code=404, detail="Promotion not found")
    
    await db.delete(promotion)
    await db.commit()
    
    return {"message": "Promotion deleted successfully"}

@router.get("/active/now", response_model=PromotionListResponse)
async def get_active_promotions(
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all currently active promotions.
    """
    current_date = datetime.now().date()
    query = select(Promotion).filter(
        (Promotion.start_date <= current_date) & 
        ((Promotion.end_date >= current_date) | (Promotion.end_date.is_(None)))
    ).offset(skip).limit(limit)
    
    result = await db.execute(query)
    promotions = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(Promotion).filter(
        (Promotion.start_date <= current_date) & 
        ((Promotion.end_date >= current_date) | (Promotion.end_date.is_(None)))
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": promotions, "total": total}
