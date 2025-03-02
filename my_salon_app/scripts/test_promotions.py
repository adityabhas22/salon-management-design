import asyncio
import httpx
import json
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0  # 30 seconds timeout

# Test data
test_data = {
    "promotion": {
        "create": {
            "title": "Summer Special",
            "description": "Special discount for summer season",
            "discount_percent": 15.0,
            "start_date": (datetime.now()).isoformat(),
            "end_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "is_active": True
        },
        "update": {
            "description": "Updated summer special discount",
            "discount_percent": 20.0
        }
    }
}

# Store created resource IDs
resource_ids = {}

async def test_health():
    """Test the health endpoint"""
    print("\n🔍 Testing health endpoint...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("✅ Health check passed")
            return True
        else:
            print("❌ Health check failed")
            return False

async def create_promotion():
    """Create a new promotion"""
    print("\n🔍 Creating a new promotion...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.post(
            f"{BASE_URL}/api/promotions/",
            json=test_data["promotion"]["create"]
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"Created promotion with ID: {result['id']}")
            resource_ids["promotion_id"] = result["id"]
            return True
        else:
            print(f"Failed to create promotion: {response.text}")
            return False

async def get_promotion():
    """Get the created promotion"""
    if "promotion_id" not in resource_ids:
        print("❌ No promotion ID available")
        return False
    
    print(f"\n🔍 Getting promotion with ID {resource_ids['promotion_id']}...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(
            f"{BASE_URL}/api/promotions/{resource_ids['promotion_id']}"
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Retrieved promotion: {result['title']}")
            return True
        else:
            print(f"Failed to get promotion: {response.text}")
            return False

async def update_promotion():
    """Update the created promotion"""
    if "promotion_id" not in resource_ids:
        print("❌ No promotion ID available")
        return False
    
    print(f"\n🔍 Updating promotion with ID {resource_ids['promotion_id']}...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.put(
            f"{BASE_URL}/api/promotions/{resource_ids['promotion_id']}",
            json=test_data["promotion"]["update"]
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Updated promotion: {result['title']} with discount {result['discount_percent']}%")
            return True
        else:
            print(f"Failed to update promotion: {response.text}")
            return False

async def delete_promotion():
    """Delete the created promotion"""
    if "promotion_id" not in resource_ids:
        print("❌ No promotion ID available")
        return False
    
    print(f"\n🔍 Deleting promotion with ID {resource_ids['promotion_id']}...")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.delete(
            f"{BASE_URL}/api/promotions/{resource_ids['promotion_id']}"
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Deleted promotion with ID: {resource_ids['promotion_id']}")
            return True
        else:
            print(f"Failed to delete promotion: {response.text}")
            return False

async def main():
    """Main test function"""
    try:
        print("🚀 Starting promotions API test...")
        
        # Test health endpoint
        if not await test_health():
            print("❌ Health check failed, aborting tests")
            return
        
        # Test create promotion
        if not await create_promotion():
            print("❌ Promotion creation failed, aborting tests")
            return
        
        # Test get promotion
        if not await get_promotion():
            print("❌ Promotion retrieval failed, continuing with other tests")
        
        # Test update promotion
        if not await update_promotion():
            print("❌ Promotion update failed, continuing with other tests")
        
        # Test delete promotion
        if not await delete_promotion():
            print("❌ Promotion deletion failed")
        
        print("\n✅ Promotions API test completed")
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 