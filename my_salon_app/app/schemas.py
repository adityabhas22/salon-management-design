from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Enums
class AppointmentStatus(str, Enum):
    UPCOMING = "upcoming"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CustomerType(str, Enum):
    STANDARD = "standard"
    VIP = "vip"

# Base schemas
class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    type: CustomerType = CustomerType.STANDARD
    preferences: Optional[Dict[str, Any]] = None
    loyalty_points: int = 0

class StaffBase(BaseModel):
    name: str
    role: str
    skills: Optional[List[str]] = None
    is_active: bool = True

class ServiceCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class ServiceBase(BaseModel):
    name: str
    price: float = Field(gt=0)
    duration_minutes: int = Field(gt=0)  # in minutes
    description: Optional[str] = None
    category_id: Optional[int] = None

class AppointmentBase(BaseModel):
    customer_id: int
    service_id: int
    staff_id: Optional[int] = None
    appointment_time: datetime
    notes: Optional[str] = None

class FeedbackBase(BaseModel):
    appointment_id: int
    customer_id: int
    rating: int = Field(ge=1, le=5)
    comments: Optional[str] = None

class PromotionBase(BaseModel):
    title: str
    description: Optional[str] = None
    discount_percent: float = Field(gt=0, le=100)
    start_date: datetime
    end_date: Optional[datetime] = None
    service_id: Optional[int] = None
    is_active: bool = True

class KnowledgeBaseBase(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None

# Create schemas
class CustomerCreate(CustomerBase):
    pass

class StaffCreate(StaffBase):
    pass

class ServiceCategoryCreate(ServiceCategoryBase):
    pass

class ServiceCreate(ServiceBase):
    pass

class AppointmentCreate(AppointmentBase):
    pass

class FeedbackCreate(FeedbackBase):
    pass

class PromotionCreate(PromotionBase):
    pass

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

# Update schemas
class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    type: Optional[CustomerType] = None
    preferences: Optional[Dict[str, Any]] = None
    loyalty_points: Optional[int] = None

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    skills: Optional[List[str]] = None
    is_active: Optional[bool] = None

class ServiceCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    duration_minutes: Optional[int] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class AppointmentUpdate(BaseModel):
    customer_id: Optional[int] = None
    service_id: Optional[int] = None
    staff_id: Optional[int] = None
    appointment_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None

class FeedbackUpdate(BaseModel):
    rating: Optional[int] = None
    comments: Optional[str] = None
    sentiment_score: Optional[float] = None

class PromotionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percent: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    service_id: Optional[int] = None
    is_active: Optional[bool] = None

class KnowledgeBaseUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None

# Response schemas
class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class StaffResponse(StaffBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ServiceCategoryResponse(ServiceCategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AppointmentResponse(AppointmentBase):
    id: int
    status: AppointmentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class FeedbackResponse(FeedbackBase):
    id: int
    sentiment_score: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PromotionResponse(PromotionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class KnowledgeBaseResponse(KnowledgeBaseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Detailed response schemas with relationships
class ServiceWithCategoryResponse(ServiceResponse):
    category: Optional[ServiceCategoryResponse] = None

class AppointmentDetailResponse(AppointmentResponse):
    customer: CustomerResponse
    service: ServiceResponse
    staff: Optional[StaffResponse] = None
    feedback: Optional[FeedbackResponse] = None

class CustomerDetailResponse(CustomerResponse):
    appointments: List[AppointmentResponse] = []
    feedback: List[FeedbackResponse] = []

# List response schemas
class CustomerListResponse(BaseModel):
    items: List[CustomerResponse]
    total: int

class StaffListResponse(BaseModel):
    items: List[StaffResponse]
    total: int

class ServiceCategoryListResponse(BaseModel):
    items: List[ServiceCategoryResponse]
    total: int

class ServiceListResponse(BaseModel):
    items: List[ServiceResponse]
    total: int

class AppointmentListResponse(BaseModel):
    items: List[AppointmentResponse]
    total: int

class FeedbackListResponse(BaseModel):
    items: List[FeedbackResponse]
    total: int

class PromotionListResponse(BaseModel):
    items: List[PromotionResponse]
    total: int

class KnowledgeBaseListResponse(BaseModel):
    items: List[KnowledgeBaseResponse]
    total: int
