from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from typing import List, Optional
from app.database import get_db
from app.models import Customer, Appointment
from app.schemas import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerListResponse, AppointmentListResponse

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

@router.post("", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new customer.
    """
    # Check if customer with same phone already exists
    existing_result = await db.execute(select(Customer).filter(Customer.phone == customer.phone))
    existing_customer = existing_result.scalars().first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer with this phone number already exists")
    
    # Check if customer with same email already exists (only if email is provided)
    if customer.email:
        existing_result = await db.execute(select(Customer).filter(Customer.email == customer.email))
        existing_customer = existing_result.scalars().first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Customer with this email already exists")
    
    # Create customer
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

@router.get("", response_model=CustomerListResponse)
async def read_customers(
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve customers with optional filtering.
    """
    query = select(Customer)
    
    # Apply filters if provided
    if name:
        query = query.filter(Customer.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Customer.email.ilike(f"%{email}%"))
    if phone:
        query = query.filter(Customer.phone.ilike(f"%{phone}%"))
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    customers = result.scalars().all()
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(Customer)
    if name:
        count_query = count_query.filter(Customer.name.ilike(f"%{name}%"))
    if email:
        count_query = count_query.filter(Customer.email.ilike(f"%{email}%"))
    if phone:
        count_query = count_query.filter(Customer.phone.ilike(f"%{phone}%"))
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": customers, "total": total}

@router.get("/{customer_id}", response_model=CustomerResponse)
async def read_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific customer by ID.
    """
    result = await db.execute(select(Customer).filter(Customer.id == customer_id))
    customer = result.scalars().first()
    
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int, 
    customer: CustomerUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update a customer.
    """
    result = await db.execute(select(Customer).filter(Customer.id == customer_id))
    db_customer = result.scalars().first()
    
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if updating to a phone that already exists
    if customer.phone is not None and customer.phone != db_customer.phone:
        existing_result = await db.execute(select(Customer).filter(Customer.phone == customer.phone))
        existing_customer = existing_result.scalars().first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Customer with this phone number already exists")
    
    # Check if updating to an email that already exists (only if email is provided)
    if customer.email is not None and customer.email != db_customer.email:
        existing_result = await db.execute(select(Customer).filter(Customer.email == customer.email))
        existing_customer = existing_result.scalars().first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Customer with this email already exists")
    
    # Update only the fields that are provided
    update_data = customer.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}", response_model=dict)
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a customer.
    """
    result = await db.execute(select(Customer).filter(Customer.id == customer_id))
    customer = result.scalars().first()
    
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    await db.delete(customer)
    await db.commit()
    
    return {"message": "Customer deleted successfully"}

@router.get("/{customer_id}/appointments", response_model=AppointmentListResponse)
async def get_customer_appointments(
    customer_id: int, 
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all appointments for a specific customer.
    """
    # Verify customer exists
    customer_result = await db.execute(select(Customer).filter(Customer.id == customer_id))
    customer = customer_result.scalars().first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get appointments for customer
    query = select(Appointment).filter(Appointment.customer_id == customer_id).offset(skip).limit(limit)
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(Appointment).filter(Appointment.customer_id == customer_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": appointments, "total": total}

@router.get("/search/phone/{phone}", response_model=CustomerResponse)
async def find_customer_by_phone(phone: str, db: AsyncSession = Depends(get_db)):
    """
    Find a customer by phone number.
    """
    result = await db.execute(select(Customer).filter(Customer.phone == phone))
    customer = result.scalars().first()
    
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer
