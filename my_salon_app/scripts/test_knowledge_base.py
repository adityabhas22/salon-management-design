import asyncio
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0  # 30 seconds timeout

# Test data
test_data = {
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

async def make_request(method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, api_prefix: bool = True):
    """Make an HTTP request to the API."""
    # Add /api prefix for API endpoints, but not for root endpoints like /health
    url = f"{BASE_URL}{'/api' if api_prefix else ''}{endpoint}"
    
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
            
            if response.status_code >= 400:
                print(f"Error {response.status_code} for {method} {url}: {response.text}")
                return {"error": response.text, "status_code": response.status_code}
            
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"status_code": response.status_code}
            
    except httpx.TimeoutException:
        print(f"Timeout error for {method} {url}")
        return {"error": "Request timed out", "status_code": 408}
    except Exception as e:
        print(f"Error for {method} {url}: {str(e)}")
        return {"error": str(e), "status_code": 500}

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
        print(f"✅ Found {len(result['items'])} knowledge base entries matching search")
    else:
        print("❌ Failed to search knowledge base")
    
    # Get by category
    print(f"Getting knowledge base entries by category '{create_data['category']}'...")
    result = await make_request("get", f"/knowledge-base/category/{create_data['category']}")
    if "items" in result:
        print(f"✅ Found {len(result['items'])} knowledge base entries in category")
    else:
        print("❌ Failed to retrieve knowledge base entries by category")
    
    # Clean up
    print(f"Deleting knowledge base entry with ID {resource_ids['knowledge_base']}...")
    result = await make_request("delete", f"/knowledge-base/{resource_ids['knowledge_base']}")
    if "message" in result:
        print("✅ Deleted knowledge base entry")
    else:
        print("❌ Failed to delete knowledge base entry")

async def main():
    """Run the test."""
    print("=== Starting Knowledge Base API Test ===")
    
    # Test health endpoint
    print("\n--- Testing Health Endpoint ---")
    result = await make_request("get", "/health", api_prefix=False)  # The health endpoint doesn't have /api prefix
    if "status" in result and result["status"] == "healthy":
        print(f"✅ API is healthy: {result}")
    else:
        print(f"❌ API health check failed: {result}")
        return
    
    # Run knowledge base test
    await test_knowledge_base()
    
    print("\n=== Knowledge Base API Test Completed ===")

if __name__ == "__main__":
    asyncio.run(main()) 