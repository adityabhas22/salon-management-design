from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.database import get_db
from app.models import Appointment, Customer, Service, Staff, AppointmentStatus
from app.schemas import (
    AppointmentCreate, 
    AppointmentUpdate, 
    AppointmentResponse, 
    AppointmentDetailResponse,
    AppointmentListResponse
)

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)

@router.post("", response_model=AppointmentResponse)
async def create_appointment(appointment: AppointmentCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new appointment.
    """
    # Verify customer exists
    customer_result = await db.execute(select(Customer).filter(Customer.id == appointment.customer_id))
    customer = customer_result.scalars().first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Verify service exists
    service_result = await db.execute(select(Service).filter(Service.id == appointment.service_id))
    service = service_result.scalars().first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Verify staff exists if provided
    if appointment.staff_id:
        staff_result = await db.execute(select(Staff).filter(Staff.id == appointment.staff_id))
        staff = staff_result.scalars().first()
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Create appointment
    db_appointment = Appointment(
        customer_id=appointment.customer_id,
        service_id=appointment.service_id,
        staff_id=appointment.staff_id,
        appointment_time=appointment.appointment_time,
        status=AppointmentStatus.UPCOMING,
        notes=appointment.notes
    )
    
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment

@router.get("", response_model=AppointmentListResponse)
async def read_appointments(
    skip: int = 0, 
    limit: int = 100,
    customer_id: Optional[int] = None,
    service_id: Optional[int] = None,
    staff_id: Optional[int] = None,
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve appointments with optional filtering.
    """
    query = select(Appointment)
    
    # Apply filters if provided
    if customer_id:
        query = query.filter(Appointment.customer_id == customer_id)
    if service_id:
        query = query.filter(Appointment.service_id == service_id)
    if staff_id:
        query = query.filter(Appointment.staff_id == staff_id)
    if status:
        query = query.filter(Appointment.status == status)
    if date_from:
        date_from_dt = datetime.combine(date_from, datetime.min.time())
        query = query.filter(Appointment.appointment_time >= date_from_dt)
    if date_to:
        date_to_dt = datetime.combine(date_to, datetime.max.time())
        query = query.filter(Appointment.appointment_time <= date_to_dt)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(Appointment)
    if customer_id:
        count_query = count_query.filter(Appointment.customer_id == customer_id)
    if service_id:
        count_query = count_query.filter(Appointment.service_id == service_id)
    if staff_id:
        count_query = count_query.filter(Appointment.staff_id == staff_id)
    if status:
        count_query = count_query.filter(Appointment.status == status)
    if date_from:
        date_from_dt = datetime.combine(date_from, datetime.min.time())
        count_query = count_query.filter(Appointment.appointment_time >= date_from_dt)
    if date_to:
        date_to_dt = datetime.combine(date_to, datetime.max.time())
        count_query = count_query.filter(Appointment.appointment_time <= date_to_dt)
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": appointments, "total": total}

@router.get("/{appointment_id}", response_model=AppointmentDetailResponse)
async def read_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific appointment by ID with detailed information.
    """
    # Use joinedload to load related entities in a single query
    query = (
        select(Appointment)
        .options(
            joinedload(Appointment.customer),
            joinedload(Appointment.service),
            joinedload(Appointment.staff),
            joinedload(Appointment.feedback)
        )
        .filter(Appointment.id == appointment_id)
    )
    
    result = await db.execute(query)
    appointment = result.scalars().first()
    
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return appointment

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int, 
    appointment: AppointmentUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update an appointment.
    """
    result = await db.execute(select(Appointment).filter(Appointment.id == appointment_id))
    db_appointment = result.scalars().first()
    
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Verify service exists if provided
    if appointment.service_id is not None:
        service_result = await db.execute(select(Service).filter(Service.id == appointment.service_id))
        service = service_result.scalars().first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
    
    # Verify staff exists if provided
    if appointment.staff_id is not None:
        staff_result = await db.execute(select(Staff).filter(Staff.id == appointment.staff_id))
        staff = staff_result.scalars().first()
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Update only the fields that are provided
    update_data = appointment.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_appointment, key, value)
    
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment

@router.delete("/{appointment_id}", response_model=dict)
async def delete_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an appointment.
    """
    result = await db.execute(select(Appointment).filter(Appointment.id == appointment_id))
    appointment = result.scalars().first()
    
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    await db.delete(appointment)
    await db.commit()
    
    return {"message": "Appointment deleted successfully"}

@router.get("/today/", response_model=AppointmentListResponse)
async def get_today_appointments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all appointments for today.
    """
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    query = (
        select(Appointment)
        .filter(
            and_(
                Appointment.appointment_time >= today_start,
                Appointment.appointment_time <= today_end
            )
        )
        .offset(skip)
        .limit(limit)
    )
    
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    # Get total count
    count_query = (
        select(func.count())
        .select_from(Appointment)
        .filter(
            and_(
                Appointment.appointment_time >= today_start,
                Appointment.appointment_time <= today_end
            )
        )
    )
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": appointments, "total": total}

@router.put("/{appointment_id}/status", response_model=AppointmentResponse)
async def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    db: AsyncSession = Depends(get_db)
):
    """
    Update the status of an appointment.
    """
    result = await db.execute(select(Appointment).filter(Appointment.id == appointment_id))
    appointment = result.scalars().first()
    
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = status
    await db.commit()
    await db.refresh(appointment)
    
    return appointment
