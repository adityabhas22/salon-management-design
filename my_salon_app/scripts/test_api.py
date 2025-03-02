import asyncio
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0  # 30 seconds timeout

# Test data
test_data = {
    "service_category": {
        "create": {"name": "Massage", "description": "Relaxing massage treatments"},
        "update": {"description": "Luxurious massage treatments for relaxation"}
    },
    "service": {
        "create": {"name": "Swedish Massage", "price": 85.0, "duration_minutes": 60, "description": "Classic relaxation massage"},
        "update": {"price": 90.0, "description": "Premium relaxation massage"}
    },
    "staff": {
        "create": {"name": "Jane Smith", "role": "Massage Therapist", "skills": ["Swedish", "Deep Tissue"]},
        "update": {"skills": ["Swedish", "Deep Tissue", "Hot Stone"]}
    },
    "customer": {
        "create": {"name": "John Doe", "phone": "555-123-4567", "email": "john.doe@example.com", "type": "standard"},
        "create_no_email": {"name": "Jane No Email", "phone": "555-987-6543", "type": "standard"},
        "update": {"loyalty_points": 100}
    },
    "appointment": {
        "create": {
            "appointment_time": (datetime.now() + timedelta(days=1)).isoformat(),
            "notes": "First time client"
        },
        "update": {"notes": "First time client, prefers gentle pressure"}
    },
    "feedback": {
        "create": {"rating": 5, "comments": "Excellent service!"},
        "update": {"sentiment_score": 0.9}
    },
    "promotion": {
        "create": {
            "title": "Summer Special", 
            "description": "20% off all massages", 
            "discount_percent": 20.0,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "is_active": True
        },
        "update": {"discount_percent": 25.0}
    },
    "knowledge_base": {
        "create": {
            "question": "What are the benefits of massage?",
            "answer": "Regular massages can help reduce stress and improve circulation.",
            "category": "wellness"
        },
        "update": {"answer": "Regular massages can help reduce stress, improve circulation, and promote better sleep."}
    }
}

# Store created resource IDs
resource_ids = {}

async def make_request(
    method: str, 
    endpoint: str, 
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make an HTTP request to the API."""
    # Add /api prefix for all endpoints except health check
    if not endpoint.startswith("/health"):
        endpoint = f"/api{endpoint}"
    
    url = f"{BASE_URL}{endpoint}"
    
    try:
        timeout = httpx.Timeout(TIMEOUT)
        async with httpx.AsyncClient(timeout=timeout) as client:
            if method.lower() == "get":
                response = await client.get(url, params=params)
            elif method.lower() == "post":
                response = await client.post(url, json=data)
            elif method.lower() == "put":
                response = await client.put(url, json=data)
            elif method.lower() == "delete":
                response = await client.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code >= 400:
                print(f"Error {response.status_code} for {method} {endpoint}: {response.text}")
                return {"error": response.text, "status_code": response.status_code}
            
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"status_code": response.status_code, "text": response.text}
    except httpx.TimeoutException:
        print(f"Timeout error for {method} {endpoint}")
        return {"error": "Request timed out", "status_code": 408}
    except Exception as e:
        print(f"Error for {method} {endpoint}: {str(e)}")
        return {"error": str(e), "status_code": 500}

async def test_service_categories():
    """Test service category endpoints."""
    print("\n--- Testing Service Categories ---")
    
    # Create
    print("Creating service category...")
    create_data = test_data["service_category"]["create"]
    result = await make_request("post", "/service-categories", data=create_data)
    if "id" in result:
        resource_ids["service_category"] = result["id"]
        print(f"✅ Created service category with ID: {result['id']}")
    else:
        print("❌ Failed to create service category")
        return
    
    # Get all
    print("Getting all service categories...")
    result = await make_request("get", "/service-categories")
    if "items" in result and "total" in result:
        print(f"✅ Retrieved {result['total']} service categories")
    else:
        print("❌ Failed to retrieve service categories")
    
    # Get by ID
    print(f"Getting service category with ID {resource_ids['service_category']}...")
    result = await make_request("get", f"/service-categories/{resource_ids['service_category']}")
    if "id" in result and result["id"] == resource_ids["service_category"]:
        print(f"✅ Retrieved service category: {result['name']}")
    else:
        print("❌ Failed to retrieve service category by ID")
    
    # Update
    print(f"Updating service category with ID {resource_ids['service_category']}...")
    update_data = test_data["service_category"]["update"]
    result = await make_request("put", f"/service-categories/{resource_ids['service_category']}", data=update_data)
    if "id" in result and result["description"] == update_data["description"]:
        print(f"✅ Updated service category: {result['name']}")
    else:
        print("❌ Failed to update service category")

async def test_services():
    """Test service endpoints."""
    print("\n--- Testing Services ---")
    
    # Create
    print("Creating service...")
    create_data = test_data["service"]["create"]
    if "service_category" in resource_ids:
        create_data["category_id"] = resource_ids["service_category"]
    result = await make_request("post", "/services", data=create_data)
    if "id" in result:
        resource_ids["service"] = result["id"]
        print(f"✅ Created service with ID: {result['id']}")
    else:
        print("❌ Failed to create service")
        return
    
    # Get all
    print("Getting all services...")
    result = await make_request("get", "/services")
    if "items" in result and "total" in result:
        print(f"✅ Retrieved {result['total']} services")
    else:
        print("❌ Failed to retrieve services")
    
    # Get by ID
    print(f"Getting service with ID {resource_ids['service']}...")
    result = await make_request("get", f"/services/{resource_ids['service']}")
    if "id" in result and result["id"] == resource_ids["service"]:
        print(f"✅ Retrieved service: {result['name']}")
    else:
        print("❌ Failed to retrieve service by ID")
    
    # Update
    print(f"Updating service with ID {resource_ids['service']}...")
    update_data = test_data["service"]["update"]
    result = await make_request("put", f"/services/{resource_ids['service']}", data=update_data)
    if "id" in result and result["price"] == update_data["price"]:
        print(f"✅ Updated service: {result['name']}")
    else:
        print("❌ Failed to update service")
    
    # Get by category
    if "service_category" in resource_ids:
        print(f"Getting services by category ID {resource_ids['service_category']}...")
        result = await make_request("get", f"/services/category/{resource_ids['service_category']}")
        if "items" in result:
            print(f"✅ Retrieved {result['total']} services in category")
        else:
            print("❌ Failed to retrieve services by category")

async def test_staff():
    """Test staff endpoints."""
    print("\n--- Testing Staff ---")
    
    # Create
    print("Creating staff member...")
    create_data = test_data["staff"]["create"]
    result = await make_request("post", "/staff", data=create_data)
    if "id" in result:
        resource_ids["staff"] = result["id"]
        print(f"✅ Created staff member with ID: {result['id']}")
    else:
        print("❌ Failed to create staff member")
        return
    
    # Get all
    print("Getting all staff members...")
    result = await make_request("get", "/staff")
    if "items" in result and "total" in result:
        print(f"✅ Retrieved {result['total']} staff members")
    else:
        print("❌ Failed to retrieve staff members")
    
    # Get by ID
    print(f"Getting staff member with ID {resource_ids['staff']}...")
    result = await make_request("get", f"/staff/{resource_ids['staff']}")
    if "id" in result and result["id"] == resource_ids["staff"]:
        print(f"✅ Retrieved staff member: {result['name']}")
    else:
        print("❌ Failed to retrieve staff member by ID")
    
    # Update
    print(f"Updating staff member with ID {resource_ids['staff']}...")
    update_data = test_data["staff"]["update"]
    result = await make_request("put", f"/staff/{resource_ids['staff']}", data=update_data)
    if "id" in result and "skills" in result and len(result["skills"]) == 3:
        print(f"✅ Updated staff member: {result['name']}")
    else:
        print("❌ Failed to update staff member")
    
    # Get by skill
    print("Getting staff members by skill 'Swedish'...")
    result = await make_request("get", "/staff/by-skill/Swedish")
    if "items" in result:
        print(f"✅ Retrieved {result['total']} staff members with skill")
    else:
        print("❌ Failed to retrieve staff members by skill")

async def test_customers():
    """Test customer endpoints."""
    print("\n--- Testing Customers ---")
    
    # Create
    print("Creating customer...")
    create_data = test_data["customer"]["create"]
    result = await make_request("post", "/customers", data=create_data)
    if "id" in result:
        resource_ids["customer"] = result["id"]
        print(f"✅ Created customer with ID: {result['id']}")
    else:
        print("❌ Failed to create customer")
        return
    
    # Get all
    print("Getting all customers...")
    result = await make_request("get", "/customers")
    if "items" in result and "total" in result:
        print(f"✅ Retrieved {result['total']} customers")
    else:
        print("❌ Failed to retrieve customers")
    
    # Get by ID
    print(f"Getting customer with ID {resource_ids['customer']}...")
    result = await make_request("get", f"/customers/{resource_ids['customer']}")
    if "id" in result and result["id"] == resource_ids["customer"]:
        print(f"✅ Retrieved customer: {result['name']}")
    else:
        print("❌ Failed to retrieve customer by ID")
    
    # Update
    print(f"Updating customer with ID {resource_ids['customer']}...")
    update_data = test_data["customer"]["update"]
    result = await make_request("put", f"/customers/{resource_ids['customer']}", data=update_data)
    if "id" in result and result["loyalty_points"] == update_data["loyalty_points"]:
        print(f"✅ Updated customer: {result['name']}")
    else:
        print("❌ Failed to update customer")
    
    # Get by phone
    print(f"Getting customer by phone {create_data['phone']}...")
    result = await make_request("get", f"/customers/search/phone/{create_data['phone']}")
    if "id" in result and result["id"] == resource_ids["customer"]:
        print(f"✅ Retrieved customer by phone: {result['name']}")
    else:
        print("❌ Failed to retrieve customer by phone")

async def test_appointments():
    """Test appointment endpoints."""
    print("\n--- Testing Appointments ---")
    
    # Create
    print("Creating appointment...")
    create_data = test_data["appointment"]["create"]
    create_data["customer_id"] = resource_ids.get("customer")
    create_data["service_id"] = resource_ids.get("service")
    create_data["staff_id"] = resource_ids.get("staff")
    
    result = await make_request("post", "/appointments", data=create_data)
    if "id" in result:
        resource_ids["appointment"] = result["id"]
        print(f"✅ Created appointment with ID: {result['id']}")
    else:
        print("❌ Failed to create appointment")
        return
    
    # Get all
    print("Getting all appointments...")
    result = await make_request("get", "/appointments")
    if "items" in result and "total" in result:
        print(f"✅ Retrieved {result['total']} appointments")
    else:
        print("❌ Failed to retrieve appointments")
    
    # Get by ID
    print(f"Getting appointment with ID {resource_ids['appointment']}...")
    result = await make_request("get", f"/appointments/{resource_ids['appointment']}")
    if "id" in result and result["id"] == resource_ids["appointment"]:
        print(f"✅ Retrieved appointment for customer ID: {result['customer_id']}")
    else:
        print("❌ Failed to retrieve appointment by ID")
    
    # Update
    print(f"Updating appointment with ID {resource_ids['appointment']}...")
    update_data = test_data["appointment"]["update"]
    result = await make_request("put", f"/appointments/{resource_ids['appointment']}", data=update_data)
    if "id" in result and result["notes"] == update_data["notes"]:
        print(f"✅ Updated appointment for customer ID: {result['customer_id']}")
    else:
        print("❌ Failed to update appointment")
    
    # Get today's appointments
    print("Getting today's appointments...")
    result = await make_request("get", "/appointments/today/")
    if "items" in result:
        print(f"✅ Retrieved {result['total']} appointments for today")
    else:
        print("❌ Failed to retrieve today's appointments")
    
    # Update status
    print(f"Updating appointment status to 'completed'...")
    result = await make_request("put", f"/appointments/{resource_ids['appointment']}/status", data={"status": "completed"})
    if "id" in result and result["status"] == "completed":
        print(f"✅ Updated appointment status to: {result['status']}")
    else:
        print("❌ Failed to update appointment status")
    
    # Get customer appointments
    print(f"Getting appointments for customer ID {resource_ids['customer']}...")
    result = await make_request("get", f"/customers/{resource_ids['customer']}/appointments")
    if "appointments" in result:
        print(f"✅ Retrieved {result['total']} appointments for customer")
    else:
        print("❌ Failed to retrieve customer appointments")

async def test_feedback():
    """Test feedback endpoints."""
    print("\n--- Testing Feedback ---")
    
    # Create
    print("Creating feedback...")
    create_data = test_data["feedback"]["create"]
    create_data["appointment_id"] = resource_ids.get("appointment")
    create_data["customer_id"] = resource_ids.get("customer")
    
    result = await make_request("post", "/feedback", data=create_data)
    if "id" in result:
        resource_ids["feedback"] = result["id"]
        print(f"✅ Created feedback with ID: {result['id']}")
    else:
        print("❌ Failed to create feedback")
        return
    
    # Get all
    print("Getting all feedback entries...")
    result = await make_request("get", "/feedback")
    if "items" in result and "total" in result:
        print(f"✅ Retrieved {result['total']} feedback entries")
    else:
        print("❌ Failed to retrieve feedback entries")
    
    # Get by ID
    print(f"Getting feedback with ID {resource_ids['feedback']}...")
    result = await make_request("get", f"/feedback/{resource_ids['feedback']}")
    if "id" in result and result["id"] == resource_ids['feedback']:
        print(f"✅ Retrieved feedback with rating: {result['rating']}")
    else:
        print("❌ Failed to retrieve feedback by ID")
    
    # Update
    print(f"Updating feedback with ID {resource_ids['feedback']}...")
    update_data = test_data["feedback"]["update"]
    result = await make_request("put", f"/feedback/{resource_ids['feedback']}", data=update_data)
    if "id" in result and result["sentiment_score"] == update_data["sentiment_score"]:
        print(f"✅ Updated feedback with rating: {result['rating']}")
    else:
        print("❌ Failed to update feedback")
    
    # Get by appointment
    print(f"Getting feedback for appointment ID {resource_ids['appointment']}...")
    result = await make_request("get", f"/feedback/appointment/{resource_ids['appointment']}")
    if "id" in result and result["appointment_id"] == resource_ids['appointment']:
        print(f"✅ Retrieved feedback for appointment with rating: {result['rating']}")
    else:
        print("❌ Failed to retrieve feedback by appointment")
    
    # Get average rating
    print("Getting average rating...")
    result = await make_request("get", "/feedback/stats/average")
    if "average_rating" in result:
        print(f"✅ Retrieved average rating: {result['average_rating']}")
    else:
        print("❌ Failed to retrieve average rating")

async def test_promotions():
    """Test promotion endpoints."""
    print("\n--- Testing Promotions ---")
    
    # Create
    print("Creating promotion...")
    create_data = test_data["promotion"]["create"]
    create_data["service_id"] = resource_ids.get("service")
    
    result = await make_request("post", "/promotions", data=create_data)
    if "id" in result:
        resource_ids["promotion"] = result["id"]
        print(f"✅ Created promotion with ID: {result['id']}")
    else:
        print("❌ Failed to create promotion")
        return
    
    # Get all
    print("Getting all promotions...")
    result = await make_request("get", "/promotions")
    if "items" in result and "total" in result:
        print(f"✅ Retrieved {result['total']} promotions")
    else:
        print("❌ Failed to retrieve promotions")
    
    # Get by ID
    print(f"Getting promotion with ID {resource_ids['promotion']}...")
    result = await make_request("get", f"/promotions/{resource_ids['promotion']}")
    if "id" in result and result["id"] == resource_ids['promotion']:
        print(f"✅ Retrieved promotion: {result['title']}")
    else:
        print("❌ Failed to retrieve promotion by ID")
    
    # Update
    print(f"Updating promotion with ID {resource_ids['promotion']}...")
    update_data = test_data["promotion"]["update"]
    result = await make_request("put", f"/promotions/{resource_ids['promotion']}", data=update_data)
    if "id" in result and result["discount_percent"] == update_data["discount_percent"]:
        print(f"✅ Updated promotion: {result['title']}")
    else:
        print("❌ Failed to update promotion")
    
    # Get active promotions
    print("Getting active promotions...")
    result = await make_request("get", "/promotions/active/now")
    if "items" in result:
        print(f"✅ Retrieved {result['total']} active promotions")
    else:
        print("❌ Failed to retrieve active promotions")

async def test_knowledge_base():
    """Test knowledge base endpoints."""
    print("\n--- Testing Knowledge Base ---")
    
    # Create
    print("Creating knowledge base entry...")
    create_data = test_data["knowledge_base"]["create"]
    
    result = await make_request("post", "/knowledge-base", data=create_data)
    if "id" in result:
        resource_ids["knowledge_base"] = result["id"]
        print(f"✅ Created knowledge base entry with ID: {result['id']}")
    else:
        print("❌ Failed to create knowledge base entry")
        return
    
    # Get all
    print("Getting all knowledge base entries...")
    result = await make_request("get", "/knowledge-base")
    if "items" in result and "total" in result:
        print(f"✅ Retrieved {result['total']} knowledge base entries")
    else:
        print("❌ Failed to retrieve knowledge base entries")
    
    # Get by ID
    print(f"Getting knowledge base entry with ID {resource_ids['knowledge_base']}...")
    result = await make_request("get", f"/knowledge-base/{resource_ids['knowledge_base']}")
    if "id" in result and result["id"] == resource_ids['knowledge_base']:
        print(f"✅ Retrieved knowledge base entry: {result['question']}")
    else:
        print("❌ Failed to retrieve knowledge base entry by ID")
    
    # Update
    print(f"Updating knowledge base entry with ID {resource_ids['knowledge_base']}...")
    update_data = test_data["knowledge_base"]["update"]
    result = await make_request("put", f"/knowledge-base/{resource_ids['knowledge_base']}", data=update_data)
    if "id" in result and result["answer"] == update_data["answer"]:
        print(f"✅ Updated knowledge base entry: {result['question']}")
    else:
        print("❌ Failed to update knowledge base entry")
    
    # Search
    print("Searching knowledge base for 'massage'...")
    result = await make_request("get", "/knowledge-base/search/", params={"query": "massage"})
    if "items" in result:
        print(f"✅ Found {result['total']} knowledge base entries matching search")
    else:
        print("❌ Failed to search knowledge base")
    
    # Get by category
    print(f"Getting knowledge base entries by category '{create_data['category']}'...")
    result = await make_request("get", f"/knowledge-base/category/{create_data['category']}")
    if "items" in result:
        print(f"✅ Retrieved {result['total']} knowledge base entries in category")
    else:
        print("❌ Failed to retrieve knowledge base entries by category")

async def cleanup():
    """Clean up created resources."""
    print("\n--- Cleaning Up Resources ---")
    
    # Delete in reverse order of dependencies
    resources_to_delete = [
        ("knowledge_base", "/knowledge-base"),
        ("feedback", "/feedback"),
        ("promotion", "/promotions"),
        ("appointment", "/appointments"),
        ("customer", "/customers"),
        ("staff", "/staff"),
        ("service", "/services"),
        ("service_category", "/service-categories")
    ]
    
    for resource_type, endpoint in resources_to_delete:
        if resource_type in resource_ids:
            resource_id = resource_ids[resource_type]
            print(f"Deleting {resource_type} with ID {resource_id}...")
            result = await make_request("delete", f"{endpoint}/{resource_id}")
            if "message" in result and "successfully" in result["message"].lower():
                print(f"✅ Deleted {resource_type}")
            else:
                print(f"❌ Failed to delete {resource_type}")

async def main():
    """Run all tests."""
    print("=== Starting API Tests ===")
    
    # Test health endpoint
    print("\n--- Testing Health Endpoint ---")
    result = await make_request("get", "/health")
    if "status" in result and result["status"] == "healthy":
        print(f"✅ API is healthy: {result}")
    else:
        print(f"❌ API health check failed: {result}")
        return
    
    # Run tests in order of dependencies
    await test_service_categories()
    await test_services()
    await test_staff()
    await test_customers()
    await test_appointments()
    await test_feedback()
    await test_promotions()
    await test_knowledge_base()
    
    # Clean up
    await cleanup()
    
    print("\n=== API Tests Completed ===")

if __name__ == "__main__":
    asyncio.run(main()) 