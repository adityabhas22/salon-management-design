import asyncio
import httpx
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0  # 30 seconds timeout

# Test data
test_data = {
    "service_category": {
        "create": {"name": "Facial", "description": "Rejuvenating facial treatments"},
        "update": {"description": "Luxurious facial treatments for skin rejuvenation"}
    }
}

# Store created resource IDs
resource_ids = {}

async def make_request(method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, api_prefix: bool = True):
    """Make an HTTP request to the API with detailed error logging."""
    # Add /api prefix for API endpoints, but not for root endpoints like /health
    url = f"{BASE_URL}{'/api' if api_prefix else ''}{endpoint}"
    
    print(f"\nMaking {method.upper()} request to {url}")
    if data:
        print(f"Request data: {json.dumps(data, indent=2)}")
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
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
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code >= 400:
                print(f"Error {response.status_code} for {method} {url}")
                print(f"Response body: {response.text}")
                return {"error": response.text, "status_code": response.status_code}
            
            try:
                result = response.json()
                print(f"Response data: {json.dumps(result, indent=2, default=str)}")
                return result
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text}")
                return {"status_code": response.status_code, "text": response.text}
            
    except httpx.TimeoutException:
        print(f"Timeout error for {method} {url}")
        return {"error": "Request timed out", "status_code": 408}
    except Exception as e:
        print(f"Error for {method} {url}: {str(e)}")
        print(traceback.format_exc())
        return {"error": str(e), "status_code": 500}

async def test_service_categories():
    """Test service category endpoints with detailed error logging."""
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
    
    # Clean up
    print(f"Deleting service category with ID {resource_ids['service_category']}...")
    result = await make_request("delete", f"/service-categories/{resource_ids['service_category']}")
    if "message" in result and "successfully" in result["message"].lower():
        print(f"✅ Deleted service category")
    else:
        print(f"❌ Failed to delete service category")

async def main():
    """Run the test."""
    print("=== Starting Service Category API Test ===")
    
    # Test health endpoint
    print("\n--- Testing Health Endpoint ---")
    result = await make_request("get", "/health", api_prefix=False)  # The health endpoint doesn't have /api prefix
    if "status" in result and result["status"] == "healthy":
        print(f"✅ API is healthy: {result}")
    else:
        print(f"❌ API health check failed: {result}")
        return
    
    # Run service category test
    await test_service_categories()
    
    print("\n=== Service Category API Test Completed ===")

if __name__ == "__main__":
    asyncio.run(main()) 