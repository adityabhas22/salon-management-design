from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.database import get_db
from app.models import Feedback, Appointment, Customer
from app.schemas import FeedbackCreate, FeedbackUpdate, FeedbackResponse, FeedbackListResponse

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"]
)

@router.post("", response_model=FeedbackResponse)
async def create_feedback(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new feedback entry.
    """
    # Verify appointment exists
    appointment_result = await db.execute(select(Appointment).filter(Appointment.id == feedback.appointment_id))
    appointment = appointment_result.scalars().first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Verify customer exists
    customer_result = await db.execute(select(Customer).filter(Customer.id == feedback.customer_id))
    customer = customer_result.scalars().first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if feedback already exists for this appointment
    existing_feedback = await db.execute(
        select(Feedback).filter(Feedback.appointment_id == feedback.appointment_id)
    )
    if existing_feedback.scalars().first():
        raise HTTPException(status_code=400, detail="Feedback already exists for this appointment")
    
    # Create feedback
    db_feedback = Feedback(**feedback.model_dump())
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

@router.get("", response_model=FeedbackListResponse)
async def read_feedback(
    skip: int = 0, 
    limit: int = 100,
    customer_id: Optional[int] = None,
    appointment_id: Optional[int] = None,
    min_rating: Optional[int] = None,
    max_rating: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve feedback entries with optional filtering.
    """
    query = select(Feedback)
    
    # Apply filters if provided
    if customer_id:
        query = query.filter(Feedback.customer_id == customer_id)
    if appointment_id:
        query = query.filter(Feedback.appointment_id == appointment_id)
    if min_rating is not None:
        query = query.filter(Feedback.rating >= min_rating)
    if max_rating is not None:
        query = query.filter(Feedback.rating <= max_rating)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    feedback_entries = result.scalars().all()
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(Feedback)
    if customer_id:
        count_query = count_query.filter(Feedback.customer_id == customer_id)
    if appointment_id:
        count_query = count_query.filter(Feedback.appointment_id == appointment_id)
    if min_rating is not None:
        count_query = count_query.filter(Feedback.rating >= min_rating)
    if max_rating is not None:
        count_query = count_query.filter(Feedback.rating <= max_rating)
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": feedback_entries, "total": total}

@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def read_feedback_by_id(feedback_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific feedback entry by ID.
    """
    result = await db.execute(select(Feedback).filter(Feedback.id == feedback_id))
    feedback = result.scalars().first()
    
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: int, 
    feedback: FeedbackUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update a feedback entry.
    """
    result = await db.execute(select(Feedback).filter(Feedback.id == feedback_id))
    db_feedback = result.scalars().first()
    
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Update only the fields that are provided
    update_data = feedback.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_feedback, key, value)
    
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

@router.delete("/{feedback_id}", response_model=dict)
async def delete_feedback(feedback_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a feedback entry.
    """
    result = await db.execute(select(Feedback).filter(Feedback.id == feedback_id))
    feedback = result.scalars().first()
    
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    await db.delete(feedback)
    await db.commit()
    
    return {"message": "Feedback deleted successfully"}

@router.get("/appointment/{appointment_id}", response_model=FeedbackResponse)
async def get_feedback_by_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get feedback for a specific appointment.
    """
    result = await db.execute(select(Feedback).filter(Feedback.appointment_id == appointment_id))
    feedback = result.scalars().first()
    
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found for this appointment")
    
    return feedback

@router.get("/stats/average", response_model=dict)
async def get_average_rating(db: AsyncSession = Depends(get_db)):
    """
    Get the average rating across all feedback.
    """
    result = await db.execute(select(func.avg(Feedback.rating)))
    average_rating = result.scalar()
    
    if average_rating is None:
        average_rating = 0
    
    return {"average_rating": float(average_rating)}
