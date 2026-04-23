#!/usr/bin/env python3
"""
Test script to verify the admin dashboard features work correctly.
This script tests the new API endpoints and functionality.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_menu_crud():
    """Test menu CRUD operations."""
    print("\nTesting menu CRUD operations...")
    
    # Test GET menu (should work even if empty)
    try:
        response = requests.get(f"{BASE_URL}/menu")
        if response.status_code == 200:
            menu = response.json()
            print(f"✅ GET menu successful, found {len(menu)} items")
        else:
            print(f"❌ GET menu failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GET menu error: {e}")
        return False
    
    # Test POST menu item
    test_item = {
        "name": "Test Coffee",
        "price": 150.0,
        "image": "https://example.com/coffee.jpg",
        "description": "Test coffee for admin dashboard"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/menu", json=test_item)
        if response.status_code == 200:
            created_item = response.json()
            item_id = created_item.get('id')
            print(f"✅ POST menu item successful, ID: {item_id}")
        else:
            print(f"❌ POST menu item failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ POST menu item error: {e}")
        return False
    
    # Test PUT menu item
    if 'item_id' in locals():
        update_data = {
            "name": "Updated Test Coffee",
            "price": 180.0,
            "image": "https://example.com/updated-coffee.jpg",
            "description": "Updated test coffee"
        }
        
        try:
            response = requests.put(f"{BASE_URL}/menu/{item_id}", json=update_data)
            if response.status_code == 200:
                print("✅ PUT menu item successful")
            else:
                print(f"❌ PUT menu item failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ PUT menu item error: {e}")
            return False
        
        # Test DELETE menu item
        try:
            response = requests.delete(f"{BASE_URL}/menu/{item_id}")
            if response.status_code == 200:
                print("✅ DELETE menu item successful")
            else:
                print(f"❌ DELETE menu item failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ DELETE menu item error: {e}")
            return False
    
    return True

def test_order_creation():
    """Test order creation with quick order functionality."""
    print("\nTesting order creation...")
    
    # First, let's add a test menu item
    test_item = {
        "name": "Quick Test Coffee",
        "price": 120.0,
        "image": "https://example.com/quick-coffee.jpg",
        "description": "Quick test coffee"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/menu", json=test_item)
        if response.status_code == 200:
            created_item = response.json()
            item_id = created_item.get('id')
            print(f"✅ Created test item for order: {item_id}")
        else:
            print(f"❌ Failed to create test item: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error creating test item: {e}")
        return False
    
    # Test order creation
    order_data = {
        "customer_name": "Test Customer",
        "customer_email": "test@example.com",
        "customer_phone": "1234567890",
        "order_type": "dine-in",
        "address": "Test Address",
        "seat_number": "A12",
        "items": [
            {
                "item_id": item_id,
                "quantity": 2
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        if response.status_code == 200:
            order = response.json()
            order_id = order.get('id')
            print(f"✅ Order creation successful, Order ID: {order_id}")
            
            # Clean up - delete the test item
            requests.delete(f"{BASE_URL}/menu/{item_id}")
            print("✅ Cleaned up test data")
            
            return True
        else:
            print(f"❌ Order creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Order creation error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Aura Cafe Admin Dashboard Features")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    tests = [
        test_health_check,
        test_menu_crud,
        test_order_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Admin dashboard features are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API endpoints.")
    
    return passed == total

if __name__ == "__main__":
    main()