from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.database import get_db
from app.models import KnowledgeBase
from app.schemas import KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse, KnowledgeBaseListResponse

router = APIRouter(
    prefix="/knowledge-base",
    tags=["knowledge_base"]
)

@router.post("", response_model=KnowledgeBaseResponse)
async def create_knowledge_entry(entry: KnowledgeBaseCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new knowledge base entry.
    """
    # Create entry
    db_entry = KnowledgeBase(**entry.model_dump())
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

@router.get("", response_model=KnowledgeBaseListResponse)
async def read_knowledge_entries(
    skip: int = 0, 
    limit: int = 100,
    question: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve knowledge base entries with optional filtering.
    """
    query = select(KnowledgeBase)
    
    # Apply filters if provided
    if question:
        query = query.filter(KnowledgeBase.question.ilike(f"%{question}%"))
    if category:
        query = query.filter(KnowledgeBase.category == category)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    entries = result.scalars().all()
    
    # Get total count for pagination
    count_query = select(func.count()).select_from(KnowledgeBase)
    if question:
        count_query = count_query.filter(KnowledgeBase.question.ilike(f"%{question}%"))
    if category:
        count_query = count_query.filter(KnowledgeBase.category == category)
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": entries, "total": total}

@router.get("/{entry_id}", response_model=KnowledgeBaseResponse)
async def read_knowledge_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific knowledge base entry by ID.
    """
    result = await db.execute(select(KnowledgeBase).filter(KnowledgeBase.id == entry_id))
    entry = result.scalars().first()
    
    if entry is None:
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    
    return entry

@router.put("/{entry_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge_entry(
    entry_id: int, 
    entry: KnowledgeBaseUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update a knowledge base entry.
    """
    result = await db.execute(select(KnowledgeBase).filter(KnowledgeBase.id == entry_id))
    db_entry = result.scalars().first()
    
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    
    # Update only the fields that are provided
    update_data = entry.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_entry, key, value)
    
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}", response_model=dict)
async def delete_knowledge_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a knowledge base entry.
    """
    result = await db.execute(select(KnowledgeBase).filter(KnowledgeBase.id == entry_id))
    entry = result.scalars().first()
    
    if entry is None:
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    
    await db.delete(entry)
    await db.commit()
    
    return {"message": "Knowledge base entry deleted successfully"}

@router.get("/search/", response_model=KnowledgeBaseListResponse)
async def search_knowledge_base(
    query: str = Query(..., min_length=1),
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Search knowledge base by question or answer.
    """
    search_query = select(KnowledgeBase).filter(
        (KnowledgeBase.question.ilike(f"%{query}%")) | 
        (KnowledgeBase.answer.ilike(f"%{query}%"))
    ).offset(skip).limit(limit)
    
    result = await db.execute(search_query)
    entries = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(KnowledgeBase).filter(
        (KnowledgeBase.question.ilike(f"%{query}%")) | 
        (KnowledgeBase.answer.ilike(f"%{query}%"))
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": entries, "total": total}

@router.get("/category/{category}", response_model=KnowledgeBaseListResponse)
async def get_entries_by_category(
    category: str,
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all knowledge base entries in a specific category.
    """
    query = select(KnowledgeBase).filter(KnowledgeBase.category == category).offset(skip).limit(limit)
    result = await db.execute(query)
    entries = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(KnowledgeBase).filter(KnowledgeBase.category == category)
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return {"items": entries, "total": total} 