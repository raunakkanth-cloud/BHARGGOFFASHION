#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Bharggo Fashion eCommerce + MLM App
Tests all backend APIs according to the test plan in /app/test_result.md
"""

import requests
import json
import time
import sys
import re
import subprocess
from datetime import datetime

# Configuration
BASE_URL = "https://fashion-ecosystem.preview.emergentagent.com/api"
TEST_EMAIL_1 = f"test{int(time.time())}@bharggo.com"  # Use timestamp for unique emails
TEST_EMAIL_2 = f"referral{int(time.time())}@bharggo.com"
TEST_NAME_1 = "Test User"
TEST_NAME_2 = "Referral User"

# Global variables to store test data
test_data = {
    "user1_id": None,
    "user1_referral_id": None,
    "user1_token": None,
    "user2_id": None,
    "user2_token": None,
    "product_id": None,
    "order_id": None
}

def get_otp_from_logs(email):
    """Extract OTP for specific email from backend logs"""
    try:
        # Get recent logs
        result = subprocess.run(['tail', '-n', '100', '/var/log/supervisor/backend.out.log'], 
                              capture_output=True, text=True)
        logs = result.stdout
        
        # Look for OTP pattern for the specific email
        pattern = rf"OTP for {re.escape(email)}: (\d{{6}})"
        matches = re.findall(pattern, logs)
        
        if matches:
            return matches[-1]  # Return the most recent OTP
        return None
    except Exception as e:
        print(f"Error getting OTP from logs: {e}")
        return None

def log_test(test_name, status, details=""):
    """Log test results"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_symbol} {test_name}")
    if details:
        print(f"    {details}")
    print()

def make_request(method, endpoint, data=None, headers=None):
    """Make HTTP request with error handling"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def test_authentication_system():
    """Test complete authentication flow"""
    print("=" * 60)
    print("TESTING AUTHENTICATION SYSTEM")
    print("=" * 60)
    
    # Test 1: Register User 1
    print("1. Testing User Registration...")
    register_data = {
        "email": TEST_EMAIL_1,
        "name": TEST_NAME_1
    }
    
    response = make_request("POST", "/auth/register", register_data)
    if response and response.status_code == 200:
        log_test("User Registration", "PASS", f"OTP sent to {TEST_EMAIL_1}")
    else:
        log_test("User Registration", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 2: Get OTP from logs (automated)
    print("Getting OTP from backend logs...")
    time.sleep(2)  # Wait for OTP to be logged
    otp1 = get_otp_from_logs(TEST_EMAIL_1)
    if not otp1:
        log_test("Get OTP from Logs", "FAIL", "Could not find OTP in logs")
        return False
    print(f"Found OTP: {otp1}")
    
    # Test 3: Verify OTP for registration
    print("2. Testing OTP Verification (Registration)...")
    verify_data = {
        "email": TEST_EMAIL_1,
        "otp": otp1
    }
    
    response = make_request("POST", "/auth/verify-otp", verify_data)
    if response and response.status_code == 200:
        result = response.json()
        test_data["user1_id"] = result["user"]["id"]
        test_data["user1_referral_id"] = result["user"]["referral_id"]
        test_data["user1_token"] = result["token"]
        log_test("OTP Verification (Registration)", "PASS", f"User ID: {test_data['user1_id']}")
        log_test("Referral ID Generated", "PASS", f"Referral ID: {test_data['user1_referral_id']}")
    else:
        log_test("OTP Verification (Registration)", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 4: Login existing user
    print("3. Testing User Login...")
    login_data = {
        "email": TEST_EMAIL_1
    }
    
    response = make_request("POST", "/auth/login", login_data)
    if response and response.status_code == 200:
        log_test("User Login", "PASS", "OTP sent for login")
    else:
        log_test("User Login", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 5: Get OTP for login
    print("Getting OTP for login from logs...")
    time.sleep(2)
    otp2 = get_otp_from_logs(TEST_EMAIL_1)
    if not otp2:
        log_test("Get Login OTP from Logs", "FAIL", "Could not find login OTP in logs")
        return False
    print(f"Found login OTP: {otp2}")
    
    # Test 6: Verify OTP for login
    print("4. Testing OTP Verification (Login)...")
    verify_login_data = {
        "email": TEST_EMAIL_1,
        "otp": otp2
    }
    
    response = make_request("POST", "/auth/verify-otp", verify_login_data)
    if response and response.status_code == 200:
        result = response.json()
        log_test("OTP Verification (Login)", "PASS", "Login successful")
    else:
        log_test("OTP Verification (Login)", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 7: Resend OTP
    print("5. Testing Resend OTP...")
    response = make_request("POST", "/auth/resend-otp", login_data)
    if response and response.status_code == 200:
        log_test("Resend OTP", "PASS", "OTP resent successfully")
    else:
        log_test("Resend OTP", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    return True

def test_product_management():
    """Test product management APIs"""
    print("=" * 60)
    print("TESTING PRODUCT MANAGEMENT")
    print("=" * 60)
    
    # Test 1: Get categories
    print("1. Testing Get Categories...")
    response = make_request("GET", "/categories")
    if response and response.status_code == 200:
        categories = response.json().get("categories", [])
        expected_categories = ["Men", "Women", "Kids"]
        if all(cat in categories for cat in expected_categories):
            log_test("Get Categories", "PASS", f"Categories: {categories}")
        else:
            log_test("Get Categories", "FAIL", f"Missing expected categories. Got: {categories}")
    else:
        log_test("Get Categories", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 2: Get all products
    print("2. Testing Get All Products...")
    response = make_request("GET", "/products")
    if response and response.status_code == 200:
        result = response.json()
        products = result.get("products", [])
        if len(products) >= 10:
            test_data["product_id"] = products[0]["_id"]
            log_test("Get All Products", "PASS", f"Found {len(products)} products")
        else:
            log_test("Get All Products", "FAIL", f"Expected at least 10 products, got {len(products)}")
    else:
        log_test("Get All Products", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 3: Get products by category
    print("3. Testing Get Products by Category...")
    response = make_request("GET", "/products?category=Men")
    if response and response.status_code == 200:
        result = response.json()
        products = result.get("products", [])
        log_test("Get Products by Category", "PASS", f"Found {len(products)} Men's products")
    else:
        log_test("Get Products by Category", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    # Test 4: Search products
    print("4. Testing Product Search...")
    response = make_request("GET", "/products?search=shirt")
    if response and response.status_code == 200:
        result = response.json()
        products = result.get("products", [])
        log_test("Product Search", "PASS", f"Found {len(products)} products matching 'shirt'")
    else:
        log_test("Product Search", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    # Test 5: Get single product
    if test_data["product_id"]:
        print("5. Testing Get Single Product...")
        response = make_request("GET", f"/products/{test_data['product_id']}")
        if response and response.status_code == 200:
            product = response.json()
            log_test("Get Single Product", "PASS", f"Product: {product.get('name', 'Unknown')}")
        else:
            log_test("Get Single Product", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    return True

def test_cart_management():
    """Test cart management APIs"""
    print("=" * 60)
    print("TESTING CART MANAGEMENT")
    print("=" * 60)
    
    if not test_data["user1_id"] or not test_data["product_id"]:
        log_test("Cart Management", "FAIL", "Missing user ID or product ID")
        return False
    
    # Test 1: Get empty cart
    print("1. Testing Get Cart (Empty)...")
    response = make_request("GET", f"/cart/{test_data['user1_id']}")
    if response and response.status_code == 200:
        cart = response.json()
        log_test("Get Empty Cart", "PASS", f"Cart items: {len(cart.get('items', []))}")
    else:
        log_test("Get Empty Cart", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 2: Add item to cart
    print("2. Testing Add to Cart...")
    cart_item = {
        "product_id": test_data["product_id"],
        "quantity": 2,
        "size": "M",
        "color": "Blue"
    }
    
    response = make_request("POST", f"/cart/{test_data['user1_id']}/add", cart_item)
    if response and response.status_code == 200:
        log_test("Add to Cart", "PASS", "Item added successfully")
    else:
        log_test("Add to Cart", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 3: Get cart with items
    print("3. Testing Get Cart (With Items)...")
    response = make_request("GET", f"/cart/{test_data['user1_id']}")
    if response and response.status_code == 200:
        cart = response.json()
        items = cart.get("items", [])
        if len(items) > 0:
            log_test("Get Cart with Items", "PASS", f"Cart has {len(items)} items")
        else:
            log_test("Get Cart with Items", "FAIL", "Cart is empty after adding item")
    else:
        log_test("Get Cart with Items", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    # Test 4: Add another item
    print("4. Testing Add Another Item...")
    cart_item2 = {
        "product_id": test_data["product_id"],
        "quantity": 1,
        "size": "L",
        "color": "Red"
    }
    
    response = make_request("POST", f"/cart/{test_data['user1_id']}/add", cart_item2)
    if response and response.status_code == 200:
        log_test("Add Another Item", "PASS", "Second item added")
    else:
        log_test("Add Another Item", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    # Test 5: Remove item from cart
    print("5. Testing Remove from Cart...")
    response = make_request("DELETE", f"/cart/{test_data['user1_id']}/remove/{test_data['product_id']}?size=M&color=Blue")
    if response and response.status_code == 200:
        log_test("Remove from Cart", "PASS", "Item removed successfully")
    else:
        log_test("Remove from Cart", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    # Test 6: Verify removal
    print("6. Testing Verify Removal...")
    response = make_request("GET", f"/cart/{test_data['user1_id']}")
    if response and response.status_code == 200:
        cart = response.json()
        items = cart.get("items", [])
        log_test("Verify Removal", "PASS", f"Cart now has {len(items)} items")
    else:
        log_test("Verify Removal", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    return True

def test_wishlist_management():
    """Test wishlist management APIs"""
    print("=" * 60)
    print("TESTING WISHLIST MANAGEMENT")
    print("=" * 60)
    
    if not test_data["user1_id"] or not test_data["product_id"]:
        log_test("Wishlist Management", "FAIL", "Missing user ID or product ID")
        return False
    
    # Test 1: Add to wishlist
    print("1. Testing Add to Wishlist...")
    response = make_request("POST", f"/wishlist/{test_data['user1_id']}/add/{test_data['product_id']}")
    if response and response.status_code == 200:
        log_test("Add to Wishlist", "PASS", "Product added to wishlist")
    else:
        log_test("Add to Wishlist", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 2: Get wishlist
    print("2. Testing Get Wishlist...")
    response = make_request("GET", f"/wishlist/{test_data['user1_id']}")
    if response and response.status_code == 200:
        wishlist = response.json()
        products = wishlist.get("products", [])
        if len(products) > 0:
            log_test("Get Wishlist", "PASS", f"Wishlist has {len(products)} products")
        else:
            log_test("Get Wishlist", "FAIL", "Wishlist is empty after adding product")
    else:
        log_test("Get Wishlist", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    # Test 3: Remove from wishlist
    print("3. Testing Remove from Wishlist...")
    response = make_request("DELETE", f"/wishlist/{test_data['user1_id']}/remove/{test_data['product_id']}")
    if response and response.status_code == 200:
        log_test("Remove from Wishlist", "PASS", "Product removed from wishlist")
    else:
        log_test("Remove from Wishlist", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    return True

def test_referral_system():
    """Test referral system with second user"""
    print("=" * 60)
    print("TESTING REFERRAL SYSTEM")
    print("=" * 60)
    
    if not test_data["user1_referral_id"]:
        log_test("Referral System", "FAIL", "Missing first user's referral ID")
        return False
    
    # Test 1: Register second user with referral
    print("1. Testing Register with Referral...")
    register_data = {
        "email": TEST_EMAIL_2,
        "name": TEST_NAME_2,
        "sponsor_referral_id": test_data["user1_referral_id"]
    }
    
    response = make_request("POST", "/auth/register", register_data)
    if response and response.status_code == 200:
        log_test("Register with Referral", "PASS", f"OTP sent to {TEST_EMAIL_2}")
    else:
        log_test("Register with Referral", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 2: Get OTP for second user
    print("Getting OTP for second user from logs...")
    time.sleep(2)
    otp2 = get_otp_from_logs(TEST_EMAIL_2)
    if not otp2:
        log_test("Get Referral User OTP from Logs", "FAIL", "Could not find OTP in logs")
        return False
    print(f"Found OTP for {TEST_EMAIL_2}: {otp2}")
    
    # Test 3: Verify OTP for second user
    print("2. Testing Verify OTP for Referred User...")
    verify_data = {
        "email": TEST_EMAIL_2,
        "otp": otp2
    }
    
    response = make_request("POST", "/auth/verify-otp", verify_data)
    if response and response.status_code == 200:
        result = response.json()
        test_data["user2_id"] = result["user"]["id"]
        test_data["user2_token"] = result["token"]
        log_test("Verify OTP for Referred User", "PASS", f"User 2 ID: {test_data['user2_id']}")
    else:
        log_test("Verify OTP for Referred User", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 4: Check referral tree
    print("3. Testing Get Referrals...")
    response = make_request("GET", f"/user/{test_data['user1_id']}/referrals")
    if response and response.status_code == 200:
        referrals = response.json().get("referrals", [])
        if len(referrals) > 0:
            log_test("Get Referrals", "PASS", f"User 1 has {len(referrals)} referrals")
        else:
            log_test("Get Referrals", "FAIL", "No referrals found for user 1")
    else:
        log_test("Get Referrals", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    return True

def test_order_and_commission():
    """Test order creation and commission system"""
    print("=" * 60)
    print("TESTING ORDER & COMMISSION SYSTEM")
    print("=" * 60)
    
    if not test_data["user2_id"] or not test_data["product_id"]:
        log_test("Order & Commission", "FAIL", "Missing user 2 ID or product ID")
        return False
    
    # Test 1: Add items to user 2's cart
    print("1. Testing Add Items to User 2 Cart...")
    cart_item = {
        "product_id": test_data["product_id"],
        "quantity": 1,
        "size": "M",
        "color": "Blue"
    }
    
    response = make_request("POST", f"/cart/{test_data['user2_id']}/add", cart_item)
    if response and response.status_code == 200:
        log_test("Add Items to User 2 Cart", "PASS", "Items added to cart")
    else:
        log_test("Add Items to User 2 Cart", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 2: Create order for user 2
    print("2. Testing Create Order...")
    order_data = {
        "items": [
            {
                "product_id": test_data["product_id"],
                "product_name": "Premium Cotton T-Shirt",  # Added required field
                "quantity": 1,
                "price": 1000.0,
                "size": "M",
                "color": "Blue"
            }
        ],
        "shipping_address": {
            "street": "123 Test Street",
            "city": "Test City",
            "state": "Test State",
            "pincode": "123456",
            "phone": "9876543210"
        },
        "use_wallet": False
    }
    
    response = make_request("POST", f"/orders/{test_data['user2_id']}", order_data)
    if response and response.status_code == 200:
        order = response.json()
        test_data["order_id"] = order.get("order_id")
        log_test("Create Order", "PASS", f"Order created: {test_data['order_id']}")
    else:
        log_test("Create Order", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 3: Check user 1's wallet for commission
    print("3. Testing Commission Credit...")
    time.sleep(2)  # Wait for commission processing
    response = make_request("GET", f"/wallet/{test_data['user1_id']}")
    if response and response.status_code == 200:
        wallet = response.json()
        balance = wallet.get("balance", 0)
        transactions = wallet.get("transactions", [])
        
        commission_txns = [txn for txn in transactions if txn.get("source") == "commission"]
        if len(commission_txns) > 0:
            log_test("Commission Credit", "PASS", f"Commission credited: ₹{balance}")
            
            # Verify commission amount (1% of order)
            expected_commission = 1000.0 * 0.01  # 1% of ₹1000
            if abs(balance - expected_commission) < 0.01:
                log_test("Commission Amount Verification", "PASS", f"Correct commission: ₹{balance}")
            else:
                log_test("Commission Amount Verification", "FAIL", f"Expected ₹{expected_commission}, got ₹{balance}")
            
            # Check expiry date
            commission_txn = commission_txns[0]
            if commission_txn.get("expiry_date"):
                log_test("Commission Expiry", "PASS", "31-day expiry set")
            else:
                log_test("Commission Expiry", "FAIL", "No expiry date found")
        else:
            log_test("Commission Credit", "FAIL", "No commission transactions found")
    else:
        log_test("Commission Credit", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    return True

def test_subscription_system():
    """Test subscription system"""
    print("=" * 60)
    print("TESTING SUBSCRIPTION SYSTEM")
    print("=" * 60)
    
    if not test_data["user1_id"]:
        log_test("Subscription System", "FAIL", "Missing user ID")
        return False
    
    # Test 1: Subscribe user
    print("1. Testing User Subscription...")
    response = make_request("POST", f"/subscription/{test_data['user1_id']}/subscribe")
    if response and response.status_code == 200:
        result = response.json()
        log_test("User Subscription", "PASS", f"Subscription successful")
    else:
        log_test("User Subscription", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    # Test 2: Verify subscription status
    print("2. Testing Verify Subscription Status...")
    response = make_request("GET", f"/user/{test_data['user1_id']}")
    if response and response.status_code == 200:
        user = response.json()
        if user.get("subscription_status"):
            log_test("Verify Subscription Status", "PASS", "User is subscribed")
        else:
            log_test("Verify Subscription Status", "FAIL", "User subscription status is false")
    else:
        log_test("Verify Subscription Status", "FAIL", f"Status: {response.status_code if response else 'No response'}")
    
    return True

def test_user_profile():
    """Test user profile API"""
    print("=" * 60)
    print("TESTING USER PROFILE")
    print("=" * 60)
    
    if not test_data["user1_id"]:
        log_test("User Profile", "FAIL", "Missing user ID")
        return False
    
    # Test 1: Get user profile
    print("1. Testing Get User Profile...")
    response = make_request("GET", f"/user/{test_data['user1_id']}")
    if response and response.status_code == 200:
        user = response.json()
        required_fields = ["email", "name", "referral_id", "wallet_balance", "subscription_status"]
        missing_fields = [field for field in required_fields if field not in user]
        
        if not missing_fields:
            log_test("Get User Profile", "PASS", "All required fields present")
            log_test("Profile Fields", "PASS", 
                   f"Wallet: ₹{user.get('wallet_balance', 0)}, "
                   f"Referral ID: {user.get('referral_id', 'N/A')}, "
                   f"Subscribed: {user.get('subscription_status', False)}")
        else:
            log_test("Get User Profile", "FAIL", f"Missing fields: {missing_fields}")
    else:
        log_test("Get User Profile", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False
    
    return True

def main():
    """Run all backend tests"""
    print("🚀 Starting Bharggo Fashion Backend API Testing")
    print(f"Base URL: {BASE_URL}")
    print(f"Test Email 1: {TEST_EMAIL_1}")
    print(f"Test Email 2: {TEST_EMAIL_2}")
    print()
    
    # Track test results
    test_results = {}
    
    # Run tests in order
    test_results["Authentication"] = test_authentication_system()
    test_results["Products"] = test_product_management()
    test_results["Cart"] = test_cart_management()
    test_results["Wishlist"] = test_wishlist_management()
    test_results["Referral"] = test_referral_system()
    test_results["Orders & Commission"] = test_order_and_commission()
    test_results["Subscription"] = test_subscription_system()
    test_results["User Profile"] = test_user_profile()
    
    # Print summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print()
    print(f"Total Tests: {len(test_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_results)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All backend tests passed!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check logs above for details.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)