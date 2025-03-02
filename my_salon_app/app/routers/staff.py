from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.database import get_db
from app.models import Staff
from app.schemas import StaffCreate, StaffUpdate, StaffResponse, StaffListResponse

router = APIRouter(
    prefix="/staff",
    tags=["staff"]
)

@router.post("", response_model=StaffResponse)
async def create_staff(staff: StaffCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new staff member.
    """
    db_staff = Staff(**staff.model_dump())
    db.add(db_staff)
    await db.commit()
    await db.refresh(db_staff)
    return db_staff

@router.get("", response_model=StaffListResponse)
async def read_staff_members(
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve staff members with optional filtering.
    """
    query = select(Staff)
    
    # Apply filters if provided
    if name:
        query = query.filter(Staff.name.ilike(f"%{name}%"))
    if role:
        query = query.filter(Staff.role.ilike(f"%{role}%"))
    if is_active is not None:
        query = query.filter(Staff.is_active == is_active)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    staff_members = result.scalars().all()
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(Staff)
    if name:
        count_query = count_query.filter(Staff.name.ilike(f"%{name}%"))
    if role:
        count_query = count_query.filter(Staff.role.ilike(f"%{role}%"))
    if is_active is not None:
        count_query = count_query.filter(Staff.is_active == is_active)
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": staff_members, "total": total}

@router.get("/{staff_id}", response_model=StaffResponse)
async def read_staff(staff_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific staff member by ID.
    """
    result = await db.execute(select(Staff).filter(Staff.id == staff_id))
    staff = result.scalars().first()
    
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    return staff

@router.put("/{staff_id}", response_model=StaffResponse)
async def update_staff(
    staff_id: int, 
    staff: StaffUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update a staff member.
    """
    result = await db.execute(select(Staff).filter(Staff.id == staff_id))
    db_staff = result.scalars().first()
    
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Update only the fields that are provided
    update_data = staff.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_staff, key, value)
    
    await db.commit()
    await db.refresh(db_staff)
    return db_staff

@router.delete("/{staff_id}", response_model=dict)
async def delete_staff(staff_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a staff member.
    """
    result = await db.execute(select(Staff).filter(Staff.id == staff_id))
    staff = result.scalars().first()
    
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    await db.delete(staff)
    await db.commit()
    
    return {"message": "Staff member deleted successfully"}

@router.get("/by-skill/{skill}", response_model=StaffListResponse)
async def get_staff_by_skill(
    skill: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get staff members by skill.
    """
    # Get all staff members first
    query = select(Staff)
    result = await db.execute(query)
    all_staff = result.scalars().all()
    
    # Filter staff members with the specified skill in Python
    staff_with_skill = [staff for staff in all_staff if skill in staff.skills]
    
    # Apply pagination in Python
    start = skip
    end = skip + limit
    paginated_staff = staff_with_skill[start:end]
    
    # Get total count
    total = len(staff_with_skill)
    
    return {"items": paginated_staff, "total": total}
