import asyncio
import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import text, select

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal
from app.models import Appointment, Feedback, Promotion, KnowledgeBase
from app.models import AppointmentStatus

async def add_missing_data():
    async with AsyncSessionLocal() as session:
        try:
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
            print("Added appointments")
            
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
            print("Added feedback")
            
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
            print("Added promotions")
            
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
            print("Added knowledge base entries")
            
            print("Missing data added successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"Error adding missing data: {e}")
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(add_missing_data()) 