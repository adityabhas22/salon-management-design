import asyncio
from datetime import datetime, timedelta
from sqlalchemy import text
from app.database import AsyncSessionLocal
from app.models import Customer, Staff, Service, Appointment, Feedback, Promotion, KnowledgeBase
from app.models import CustomerType, AppointmentStatus

async def seed_data():
    async with AsyncSessionLocal() as session:
        try:
            # Add customers
            customers = [
                Customer(
                    name="John Doe",
                    phone="+1234567890",
                    email="john.doe@example.com",
                    type=CustomerType.STANDARD,
                    preferences={"preferred_day": "Saturday", "preferred_time": "morning"},
                    loyalty_points=100
                ),
                Customer(
                    name="Jane Smith",
                    phone="+1987654321",
                    email="jane.smith@example.com",
                    type=CustomerType.VIP,
                    preferences={"preferred_day": "Sunday", "preferred_time": "afternoon"},
                    loyalty_points=250
                ),
                Customer(
                    name="Alice Johnson",
                    phone="+1122334455",
                    email="alice.johnson@example.com",
                    type=CustomerType.STANDARD,
                    preferences={"preferred_day": "Friday", "preferred_time": "evening"},
                    loyalty_points=50
                )
            ]
            session.add_all(customers)
            await session.commit()
            
            # Add staff
            staff = [
                Staff(
                    name="Michael Brown",
                    role="Hair Stylist",
                    skills=["haircut", "coloring", "styling"],
                    is_active=True
                ),
                Staff(
                    name="Sarah Wilson",
                    role="Massage Therapist",
                    skills=["swedish", "deep tissue", "hot stone"],
                    is_active=True
                ),
                Staff(
                    name="David Lee",
                    role="Nail Technician",
                    skills=["manicure", "pedicure", "nail art"],
                    is_active=True
                )
            ]
            session.add_all(staff)
            await session.commit()
            
            # Add services
            services = [
                Service(
                    name="Haircut",
                    price=50.0,
                    duration=45,
                    description="Professional haircut with wash and style"
                ),
                Service(
                    name="Swedish Massage",
                    price=80.0,
                    duration=60,
                    description="Relaxing full-body massage"
                ),
                Service(
                    name="Manicure",
                    price=35.0,
                    duration=30,
                    description="Basic manicure with polish"
                ),
                Service(
                    name="Facial",
                    price=65.0,
                    duration=45,
                    description="Deep cleansing facial treatment"
                ),
                Service(
                    name="Pedicure",
                    price=45.0,
                    duration=45,
                    description="Relaxing pedicure with polish"
                )
            ]
            session.add_all(services)
            await session.commit()
            
            # Add appointments
            now = datetime.now()
            appointments = [
                Appointment(
                    customer_id=1,
                    service_id=1,
                    staff_id=1,
                    appointment_time=now + timedelta(days=1, hours=10),
                    status=AppointmentStatus.UPCOMING,
                    notes="First time client"
                ),
                Appointment(
                    customer_id=2,
                    service_id=2,
                    staff_id=2,
                    appointment_time=now + timedelta(days=2, hours=14),
                    status=AppointmentStatus.UPCOMING,
                    notes="Prefers extra pressure"
                ),
                Appointment(
                    customer_id=3,
                    service_id=3,
                    staff_id=3,
                    appointment_time=now - timedelta(days=2, hours=11),
                    status=AppointmentStatus.COMPLETED,
                    notes="Regular client"
                )
            ]
            session.add_all(appointments)
            await session.commit()
            
            # Add feedback
            feedback = [
                Feedback(
                    appointment_id=3,
                    customer_id=3,
                    rating=5,
                    comments="Great service, very satisfied!",
                    sentiment_score=0.9
                )
            ]
            session.add_all(feedback)
            await session.commit()
            
            # Add promotions
            promotions = [
                Promotion(
                    title="Summer Special",
                    description="20% off all massages",
                    discount_percent=20.0,
                    valid_from=now,
                    valid_till=now + timedelta(days=30),
                    is_active=True
                ),
                Promotion(
                    title="New Client Discount",
                    description="15% off first visit",
                    discount_percent=15.0,
                    valid_from=now,
                    valid_till=now + timedelta(days=90),
                    is_active=True
                )
            ]
            session.add_all(promotions)
            await session.commit()
            
            # Add knowledge base entries
            kb_entries = [
                KnowledgeBase(
                    question="What are your opening hours?",
                    answer="We are open Monday to Friday from 9 AM to 8 PM, and on weekends from 10 AM to 6 PM."
                ),
                KnowledgeBase(
                    question="Do you offer gift cards?",
                    answer="Yes, we offer gift cards in any denomination. They can be purchased in-store or online."
                ),
                KnowledgeBase(
                    question="What is your cancellation policy?",
                    answer="Please cancel at least 24 hours in advance to avoid a cancellation fee of 50% of the service price."
                )
            ]
            session.add_all(kb_entries)
            await session.commit()
            
            print("Database seeded successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"Error seeding database: {e}")
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(seed_data()) 