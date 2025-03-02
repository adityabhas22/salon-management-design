# Salon Management API

A comprehensive API for managing a Spa/Salon business with features for appointments, customer relationship management, promotions, feedback, and more.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)

## Overview

This Salon Management API provides a complete backend solution for spa and salon businesses. It handles customer data, staff management, service offerings, appointment scheduling, feedback collection, promotions, and a knowledge base for frequently asked questions.

## Features

- Customer management with loyalty points
- Staff management with skills tracking
- Service categories and services
- Appointment scheduling and management
- Customer feedback with sentiment analysis
- Promotional campaigns
- Knowledge base for FAQs

## Database Schema

The application uses a PostgreSQL database with the following main entities:

### Customers
- `id`: Primary key
- `name`: Customer's full name
- `phone`: Unique phone number
- `email`: Optional unique email
- `type`: Customer type (STANDARD or VIP)
- `preferences`: JSON field for storing preferences
- `loyalty_points`: Integer for loyalty program
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Staff
- `id`: Primary key
- `name`: Staff member's name
- `role`: Job role
- `skills`: JSON array of skills
- `is_active`: Boolean indicating active status
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Service Categories
- `id`: Primary key
- `name`: Unique category name
- `description`: Optional description
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Services
- `id`: Primary key
- `name`: Unique service name
- `price`: Service price
- `duration_minutes`: Duration in minutes
- `description`: Optional description
- `category_id`: Foreign key to service_categories
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Appointments
- `id`: Primary key
- `customer_id`: Foreign key to customers
- `service_id`: Foreign key to services
- `staff_id`: Optional foreign key to staff
- `appointment_time`: Datetime of appointment
- `status`: Enum (UPCOMING, COMPLETED, CANCELLED)
- `notes`: Optional notes
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Feedback
- `id`: Primary key
- `appointment_id`: Foreign key to appointments (unique)
- `customer_id`: Foreign key to customers
- `rating`: Integer rating (1-5)
- `comments`: Optional comments
- `sentiment_score`: Optional sentiment analysis score
- `created_at`: Timestamp of creation

### Promotions
- `id`: Primary key
- `title`: Promotion title
- `description`: Optional description
- `discount_percent`: Discount percentage
- `start_date`: Start date of promotion
- `end_date`: Optional end date
- `service_id`: Optional foreign key to services
- `is_active`: Boolean indicating active status
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Knowledge Base
- `id`: Primary key
- `question`: Frequently asked question
- `answer`: Answer to the question
- `category`: Optional category
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## API Endpoints

### Customers

- `POST /api/customers`: Create a new customer
- `GET /api/customers`: List all customers with optional filtering
- `GET /api/customers/{customer_id}`: Get a specific customer
- `PUT /api/customers/{customer_id}`: Update a customer
- `DELETE /api/customers/{customer_id}`: Delete a customer
- `GET /api/customers/{customer_id}/appointments`: Get all appointments for a customer
- `GET /api/customers/search/phone/{phone}`: Find a customer by phone number

### Staff

- `POST /api/staff`: Create a new staff member
- `GET /api/staff`: List all staff members with optional filtering
- `GET /api/staff/{staff_id}`: Get a specific staff member
- `PUT /api/staff/{staff_id}`: Update a staff member
- `DELETE /api/staff/{staff_id}`: Delete a staff member
- `GET /api/staff/{staff_id}/appointments`: Get all appointments for a staff member

### Service Categories

- `POST /api/service_categories`: Create a new service category
- `GET /api/service_categories`: List all service categories
- `GET /api/service_categories/{category_id}`: Get a specific service category
- `PUT /api/service_categories/{category_id}`: Update a service category
- `DELETE /api/service_categories/{category_id}`: Delete a service category
- `GET /api/service_categories/{category_id}/services`: Get all services in a category

### Services

- `POST /api/services`: Create a new service
- `GET /api/services`: List all services with optional filtering
- `GET /api/services/{service_id}`: Get a specific service
- `PUT /api/services/{service_id}`: Update a service
- `DELETE /api/services/{service_id}`: Delete a service
- `GET /api/services/{service_id}/appointments`: Get all appointments for a service

### Appointments

- `POST /api/appointments`: Create a new appointment
- `GET /api/appointments`: List all appointments with optional filtering
- `GET /api/appointments/{appointment_id}`: Get a specific appointment
- `PUT /api/appointments/{appointment_id}`: Update an appointment
- `DELETE /api/appointments/{appointment_id}`: Delete an appointment
- `PUT /api/appointments/{appointment_id}/status`: Update appointment status
- `GET /api/appointments/date/{date}`: Get appointments for a specific date

### Feedback

- `POST /api/feedback`: Create new feedback
- `GET /api/feedback`: List all feedback with optional filtering
- `GET /api/feedback/{feedback_id}`: Get specific feedback
- `PUT /api/feedback/{feedback_id}`: Update feedback
- `DELETE /api/feedback/{feedback_id}`: Delete feedback
- `GET /api/feedback/appointment/{appointment_id}`: Get feedback for a specific appointment

### Promotions

- `POST /api/promotions`: Create a new promotion
- `GET /api/promotions`: List all promotions with optional filtering
- `GET /api/promotions/{promotion_id}`: Get a specific promotion
- `PUT /api/promotions/{promotion_id}`: Update a promotion
- `DELETE /api/promotions/{promotion_id}`: Delete a promotion
- `GET /api/promotions/active`: Get all currently active promotions

### Knowledge Base

- `POST /api/knowledge_base`: Add a new knowledge base entry
- `GET /api/knowledge_base`: List all knowledge base entries with optional filtering
- `GET /api/knowledge_base/{entry_id}`: Get a specific knowledge base entry
- `PUT /api/knowledge_base/{entry_id}`: Update a knowledge base entry
- `DELETE /api/knowledge_base/{entry_id}`: Delete a knowledge base entry
- `GET /api/knowledge_base/search`: Search knowledge base by query

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AI-Spa-agent-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd my_salon_app
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env` (if not already present)
   - Update the database connection string and other settings

## Running the Application

1. Make sure your PostgreSQL database is running and accessible

2. Run the application:
   ```bash
   python run.py
   ```

3. The application will start on the configured port (default: 8000)
   - API will be available at: http://localhost:8000
   - API documentation will be available at: http://localhost:8000/docs

## Environment Variables

The application uses the following environment variables:

- `PORT`: The port to run the application on (default: 8000)
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `ALGORITHM`: Algorithm for JWT token (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time in minutes (default: 30)

## API Documentation

The API documentation is automatically generated using Swagger UI and is available at:
- http://localhost:8000/docs

For a more detailed API reference, you can also use ReDoc at:
- http://localhost:8000/redoc # salon-management-design
