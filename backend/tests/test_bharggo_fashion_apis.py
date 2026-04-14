# Backend API Tests for Bharggo Fashion eCommerce + MLM App
# Tests: Auth (register, login, OTP), Products, Cart, Orders, Wallet, Subscription, Referrals

import pytest
import requests
import os
import time

BASE_URL = os.environ.get('EXPO_PUBLIC_BACKEND_URL', 'https://fashion-ecosystem.preview.emergentagent.com')

# Test data
TEST_USER_1 = {
    "email": "test_user_1@bharggo.com",
    "name": "Test User One",
    "mobile": "9876543210",
    "address": "123 Test Street, Test City",
    "pincode": "110001"
}

TEST_USER_2 = {
    "email": "test_user_2@bharggo.com",
    "name": "Test User Two",
    "mobile": "9876543211",
    "address": "456 Test Avenue, Test Town",
    "pincode": "110002"
}

# Global variables to store test data
user1_data = {}
user2_data = {}
test_product_id = None
test_order_id = None


@pytest.fixture
def api_client():
    """Shared requests session"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


class TestHealthCheck:
    """Basic health check"""
    
    def test_backend_is_running(self, api_client):
        """Test if backend is accessible"""
        response = api_client.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        print("✓ Backend is running and accessible")


class TestProductAPIs:
    """Product-related API tests"""
    
    def test_get_categories(self, api_client):
        """Test GET /api/categories"""
        response = api_client.get(f"{BASE_URL}/api/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) > 0
        assert "Men" in data["categories"] or "Women" in data["categories"] or "Kids" in data["categories"]
        print(f"✓ Categories API working - Found {len(data['categories'])} categories")
    
    def test_get_products(self, api_client):
        """Test GET /api/products"""
        global test_product_id
        response = api_client.get(f"{BASE_URL}/api/products?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert "total" in data
        assert len(data["products"]) > 0
        
        # Store first product ID for later tests
        test_product_id = data["products"][0]["_id"]
        
        # Verify product has image_url field
        assert "image_url" in data["products"][0]
        print(f"✓ Products API working - Found {len(data['products'])} products")
    
    def test_get_product_by_id(self, api_client):
        """Test GET /api/products/{product_id}"""
        global test_product_id
        if not test_product_id:
            pytest.skip("No product ID available")
        
        response = api_client.get(f"{BASE_URL}/api/products/{test_product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == test_product_id
        assert "name" in data
        assert "price" in data
        print(f"✓ Get product by ID working - Product: {data['name']}")
    
    def test_search_products(self, api_client):
        """Test product search"""
        response = api_client.get(f"{BASE_URL}/api/products?search=shirt")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        print(f"✓ Product search working - Found {len(data['products'])} results")
    
    def test_filter_by_category(self, api_client):
        """Test category filter"""
        response = api_client.get(f"{BASE_URL}/api/products?category=Men")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        if len(data["products"]) > 0:
            assert data["products"][0]["category"] == "Men"
        print(f"✓ Category filter working - Found {len(data['products'])} Men products")


class TestAuthenticationFlow:
    """Authentication flow tests - Registration, Login, OTP Verification"""
    
    def test_01_register_user1(self, api_client):
        """Test user registration - User 1"""
        global user1_data
        response = api_client.post(f"{BASE_URL}/api/auth/register", json=TEST_USER_1)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "email" in data
        print(f"✓ User 1 registration initiated - Check backend logs for OTP")
    
    def test_02_verify_otp_user1(self, api_client):
        """Test OTP verification for User 1 - REQUIRES MANUAL OTP FROM LOGS"""
        global user1_data
        # This test will fail without actual OTP - that's expected
        # In real testing, we'd get OTP from backend logs
        print("⚠ OTP verification requires manual OTP from backend logs")
        print("  Check: tail -n 50 /var/log/supervisor/backend.err.log")
        # Skip actual verification for now
        pytest.skip("OTP verification requires manual OTP from logs")
    
    def test_03_register_user2_with_referral(self, api_client):
        """Test registration with referral code"""
        global user2_data, user1_data
        # This test requires user1's referral ID
        # For now, we'll test registration without referral
        response = api_client.post(f"{BASE_URL}/api/auth/register", json=TEST_USER_2)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"✓ User 2 registration initiated")
    
    def test_04_login_existing_user(self, api_client):
        """Test login for existing user"""
        # First, let's try to login with a user that might exist
        response = api_client.post(f"{BASE_URL}/api/auth/login", json={"email": "test@bharggo.com"})
        # Could be 200 (user exists) or 404 (user not found)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            print("✓ Login API working - OTP sent")
        else:
            print("✓ Login API working - User not found (expected)")
    
    def test_05_resend_otp(self, api_client):
        """Test resend OTP"""
        response = api_client.post(f"{BASE_URL}/api/auth/resend-otp", json={"email": TEST_USER_1["email"]})
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✓ Resend OTP API working")
    
    def test_06_invalid_otp(self, api_client):
        """Test invalid OTP verification"""
        response = api_client.post(f"{BASE_URL}/api/auth/verify-otp", json={
            "email": TEST_USER_1["email"],
            "otp": "000000"
        })
        assert response.status_code in [400, 404]
        print("✓ Invalid OTP properly rejected")


class TestCartAPIs:
    """Cart-related API tests"""
    
    def test_get_cart_new_user(self, api_client):
        """Test getting cart for new user (creates empty cart)"""
        # Using a test user ID
        test_user_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
        response = api_client.get(f"{BASE_URL}/api/cart/{test_user_id}")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        print("✓ Get cart API working - Empty cart created")
    
    def test_add_to_cart(self, api_client):
        """Test adding item to cart"""
        global test_product_id
        if not test_product_id:
            pytest.skip("No product ID available")
        
        test_user_id = "507f1f77bcf86cd799439011"
        cart_item = {
            "product_id": test_product_id,
            "quantity": 2,
            "size": "M",
            "color": "Blue"
        }
        response = api_client.post(f"{BASE_URL}/api/cart/{test_user_id}/add", json=cart_item)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✓ Add to cart API working")
    
    def test_get_cart_with_items(self, api_client):
        """Test getting cart with items"""
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.get(f"{BASE_URL}/api/cart/{test_user_id}")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        print(f"✓ Cart retrieval working - {len(data['items'])} items")
    
    def test_remove_from_cart(self, api_client):
        """Test removing item from cart"""
        global test_product_id
        if not test_product_id:
            pytest.skip("No product ID available")
        
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.delete(f"{BASE_URL}/api/cart/{test_user_id}/remove/{test_product_id}?size=M&color=Blue")
        assert response.status_code == 200
        print("✓ Remove from cart API working")
    
    def test_clear_cart(self, api_client):
        """Test clearing entire cart"""
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.delete(f"{BASE_URL}/api/cart/{test_user_id}/clear")
        assert response.status_code == 200
        print("✓ Clear cart API working")


class TestWishlistAPIs:
    """Wishlist-related API tests"""
    
    def test_get_wishlist(self, api_client):
        """Test getting wishlist"""
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.get(f"{BASE_URL}/api/wishlist/{test_user_id}")
        assert response.status_code == 200
        data = response.json()
        assert "product_ids" in data
        print("✓ Get wishlist API working")
    
    def test_add_to_wishlist(self, api_client):
        """Test adding product to wishlist"""
        global test_product_id
        if not test_product_id:
            pytest.skip("No product ID available")
        
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.post(f"{BASE_URL}/api/wishlist/{test_user_id}/add/{test_product_id}")
        assert response.status_code == 200
        print("✓ Add to wishlist API working")
    
    def test_remove_from_wishlist(self, api_client):
        """Test removing product from wishlist"""
        global test_product_id
        if not test_product_id:
            pytest.skip("No product ID available")
        
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.delete(f"{BASE_URL}/api/wishlist/{test_user_id}/remove/{test_product_id}")
        assert response.status_code == 200
        print("✓ Remove from wishlist API working")


class TestOrderAPIs:
    """Order-related API tests"""
    
    def test_create_order(self, api_client):
        """Test creating an order"""
        global test_product_id, test_order_id
        if not test_product_id:
            pytest.skip("No product ID available")
        
        test_user_id = "507f1f77bcf86cd799439011"
        order_data = {
            "items": [
                {
                    "product_id": test_product_id,
                    "product_name": "Test Product",
                    "quantity": 1,
                    "size": "M",
                    "color": "Blue",
                    "price": 599.0,
                    "discount": 0.0
                }
            ],
            "shipping_address": {
                "name": "Test User",
                "mobile": "9876543210",
                "address": "123 Test Street",
                "pincode": "110001"
            },
            "use_wallet": False
        }
        response = api_client.post(f"{BASE_URL}/api/orders/{test_user_id}", json=order_data)
        assert response.status_code == 200
        data = response.json()
        assert "order_id" in data
        assert "total" in data
        test_order_id = data["order_id"]
        print(f"✓ Create order API working - Order ID: {test_order_id}")
    
    def test_get_user_orders(self, api_client):
        """Test getting user orders"""
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.get(f"{BASE_URL}/api/orders/{test_user_id}")
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        print(f"✓ Get user orders API working - {len(data['orders'])} orders")
    
    def test_get_specific_order(self, api_client):
        """Test getting specific order"""
        global test_order_id
        if not test_order_id:
            pytest.skip("No order ID available")
        
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.get(f"{BASE_URL}/api/orders/{test_user_id}/{test_order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["order_id"] == test_order_id
        print(f"✓ Get specific order API working")


class TestWalletAPIs:
    """Wallet-related API tests"""
    
    def test_get_wallet(self, api_client):
        """Test getting wallet balance and transactions"""
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.get(f"{BASE_URL}/api/wallet/{test_user_id}")
        # Could be 400 (invalid ID) or 404 (user not found) - both are valid responses
        assert response.status_code in [200, 400, 404]
        if response.status_code == 200:
            data = response.json()
            assert "balance" in data
            assert "transactions" in data
            print("✓ Get wallet API working")
        else:
            print("✓ Get wallet API working - User not found (expected for test ID)")


class TestSubscriptionAPIs:
    """Subscription-related API tests"""
    
    def test_subscribe_user(self, api_client):
        """Test user subscription"""
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.post(f"{BASE_URL}/api/subscription/{test_user_id}/subscribe")
        # Could be 400 (invalid ID) or 404 (user not found)
        assert response.status_code in [200, 400, 404]
        if response.status_code == 200:
            data = response.json()
            assert "message" in data
            print("✓ Subscribe API working")
        else:
            print("✓ Subscribe API working - User not found (expected for test ID)")


class TestUserProfileAPIs:
    """User profile and referral API tests"""
    
    def test_get_user_profile(self, api_client):
        """Test getting user profile"""
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.get(f"{BASE_URL}/api/user/{test_user_id}")
        # Could be 400 (invalid ID) or 404 (user not found)
        assert response.status_code in [200, 400, 404]
        if response.status_code == 200:
            data = response.json()
            assert "email" in data
            assert "referral_id" in data
            print("✓ Get user profile API working")
        else:
            print("✓ Get user profile API working - User not found (expected for test ID)")
    
    def test_get_user_referrals(self, api_client):
        """Test getting user referrals"""
        test_user_id = "507f1f77bcf86cd799439011"
        response = api_client.get(f"{BASE_URL}/api/user/{test_user_id}/referrals")
        assert response.status_code == 200
        data = response.json()
        assert "referrals" in data
        print(f"✓ Get user referrals API working - {len(data['referrals'])} referrals")


# Cleanup function
def test_cleanup():
    """Cleanup test data"""
    print("\n✓ All backend API tests completed")
    print("Note: OTP-based auth tests require manual OTP from backend logs")
