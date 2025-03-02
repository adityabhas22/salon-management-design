import asyncio
import httpx
import json
import traceback

BASE_URL = "http://localhost:8000/api"
TIMEOUT = 10.0  # 10 seconds timeout

async def test_customer_with_email():
    """Test creating a customer with email."""
    print("\n--- Testing Customer Creation With Email ---")
    
    data = {
        "name": "Customer With Email",
        "phone": "555-123-0001",
        "email": "customer.with.email@example.com",
        "type": "standard"
    }
    
    try:
        timeout = httpx.Timeout(TIMEOUT)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{BASE_URL}/customers", json=data)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Successfully created customer with email")
            else:
                print("❌ Failed to create customer with email")
    except httpx.TimeoutException:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

async def test_customer_without_email():
    """Test creating a customer without email."""
    print("\n--- Testing Customer Creation Without Email ---")
    
    data = {
        "name": "Customer Without Email",
        "phone": "555-123-0002",
        "type": "standard"
    }
    
    try:
        timeout = httpx.Timeout(TIMEOUT)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{BASE_URL}/customers", json=data)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Successfully created customer without email")
            else:
                print("❌ Failed to create customer without email")
    except httpx.TimeoutException:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

async def test_customer_with_null_email():
    """Test creating a customer with null email."""
    print("\n--- Testing Customer Creation With Null Email ---")
    
    data = {
        "name": "Customer With Null Email",
        "phone": "555-123-0003",
        "email": None,
        "type": "standard"
    }
    
    try:
        timeout = httpx.Timeout(TIMEOUT)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{BASE_URL}/customers", json=data)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Successfully created customer with null email")
            else:
                print("❌ Failed to create customer with null email")
    except httpx.TimeoutException:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

async def main():
    """Run all tests."""
    print("=== Starting Email Optional Tests ===")
    
    await test_customer_with_email()
    await test_customer_without_email()
    await test_customer_with_null_email()
    
    print("\n=== Email Optional Tests Completed ===")

if __name__ == "__main__":
    asyncio.run(main()) 