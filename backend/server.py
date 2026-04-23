from fastapi import FastAPI, APIRouter, HTTPException, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import random
import string
from bson import ObjectId
from admin_panel import ADMIN_HTML

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "bharggo-fashion-secret-key-2025")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

# Create the main app without a prefix
app = FastAPI(title="Bharggo Fashion API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# ========================
# MODELS
# ========================

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return str(v)

# User Models
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    mobile: str
    address: str
    pincode: str
    sponsor_referral_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    email: EmailStr
    name: str
    mobile: str
    address: str
    pincode: str
    referral_id: str
    sponsor_id: Optional[str] = None
    subscription_status: bool = False
    subscription_date: Optional[datetime] = None
    wallet_balance: float = 0.0
    total_commission_earned: float = 0.0
    level: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Product Models
class ProductVariant(BaseModel):
    size: str
    color: str
    stock: int

class Product(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: str
    category: str
    price: float
    discount: float = 0.0
    images: List[str] = []  # base64 encoded
    videos: List[str] = []  # base64 encoded
    sizes: List[str] = []
    colors: List[str] = []
    variants: List[ProductVariant] = []
    rating: float = 0.0
    review_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class ProductCreate(BaseModel):
    name: str
    description: str
    category: str
    price: float
    discount: float = 0.0
    images: List[str] = []
    videos: List[str] = []
    sizes: List[str] = []
    colors: List[str] = []
    variants: List[ProductVariant] = []

# Cart Models
class CartItem(BaseModel):
    product_id: str
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None

class Cart(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    items: List[CartItem] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class CartUpdate(BaseModel):
    product_id: str
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None

# Wishlist Models
class Wishlist(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    product_ids: List[str] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Order Models
class OrderItem(BaseModel):
    product_id: str
    product_name: Optional[str] = ""
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None
    price: float
    discount: float = 0.0

class Order(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    order_id: str
    user_id: str
    items: List[OrderItem]
    subtotal: float
    discount_amount: float = 0.0
    total: float
    payment_status: str = "pending"  # pending, completed, failed
    order_status: str = "placed"  # placed, confirmed, shipped, delivered, cancelled
    shipping_address: Dict[str, Any]
    tracking_info: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping_address: Dict[str, Any]
    use_wallet: bool = False

# Wallet Models
class WalletTransaction(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    amount: float
    type: str  # credit, debit
    source: str  # commission, purchase, payout, subscription
    description: str
    expiry_date: Optional[datetime] = None
    status: str = "active"  # active, expired, used
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Referral Models
class Referral(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    referrer_id: str
    referred_user_id: str
    level: int
    commission_rate: float = 0.01  # 1%
    total_commission_earned: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Subscription Models
class Subscription(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    amount: float = 111.0
    status: str = "active"  # active, expired
    benefits: List[str] = ["20% discount on purchases", "Faster delivery", "Referral earnings"]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# OTP Model
class OTP(BaseModel):
    email: EmailStr
    otp: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime

# ========================
# HELPER FUNCTIONS
# ========================

def generate_referral_id():
    """Generate 12-digit alphanumeric referral ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def send_email_otp(email: str, otp: str):
    """Mock email sending - replace with actual email service"""
    # TODO: Integrate with SendGrid/AWS SES when credentials are provided
    logger.info(f"OTP for {email}: {otp}")
    print(f"\n{'='*50}\nOTP for {email}: {otp}\n{'='*50}\n")
    return True

async def send_welcome_email(email: str, name: str):
    """Send welcome email to new users"""
    # TODO: Integrate with email service
    logger.info(f"Welcome email sent to {email}")
    print(f"\n{'='*50}\nWelcome to Bharggo Fashion, {name}!\nEmail: {email}\n{'='*50}\n")
    return True

# ========================
# AUTHENTICATION ROUTES
# ========================

@api_router.post("/auth/register")
async def register(user_data: UserCreate):
    """Register new user and send OTP"""
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Verify sponsor referral ID if provided
    sponsor = None
    if user_data.sponsor_referral_id:
        sponsor = await db.users.find_one({"referral_id": user_data.sponsor_referral_id})
        if not sponsor:
            raise HTTPException(status_code=400, detail="Invalid sponsor referral ID")
    
    # Generate and send OTP
    otp = generate_otp()
    otp_data = OTP(
        email=user_data.email,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    
    # Store OTP (delete existing OTPs for this email first)
    await db.otps.delete_many({"email": user_data.email})
    await db.otps.insert_one(otp_data.dict())
    
    # Send OTP email
    await send_email_otp(user_data.email, otp)
    
    # Store pending user data
    pending_user = {
        "email": user_data.email,
        "name": user_data.name,
        "mobile": user_data.mobile,
        "address": user_data.address,
        "pincode": user_data.pincode,
        "sponsor_referral_id": user_data.sponsor_referral_id,
        "created_at": datetime.utcnow()
    }
    await db.pending_users.delete_many({"email": user_data.email})
    await db.pending_users.insert_one(pending_user)
    
    return {"message": "OTP sent to your email", "email": user_data.email}

@api_router.post("/auth/login")
async def login(login_data: UserLogin):
    """Login user and send OTP"""
    # Check if user exists
    user = await db.users.find_one({"email": login_data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    
    # Check for existing permanent OTP (demo accounts)
    existing_otp = await db.otps.find_one({"email": login_data.email, "expires_at": {"$gt": datetime(2029, 1, 1)}})
    if existing_otp:
        # Demo account - don't overwrite the permanent OTP
        return {"message": "OTP sent to your email", "email": login_data.email}
    
    # Generate and send OTP
    otp = generate_otp()
    otp_data = OTP(
        email=login_data.email,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    
    # Store OTP
    await db.otps.delete_many({"email": login_data.email})
    await db.otps.insert_one(otp_data.dict())
    
    # Send OTP email
    await send_email_otp(login_data.email, otp)
    
    return {"message": "OTP sent to your email", "email": login_data.email}

@api_router.post("/auth/verify-otp")
async def verify_otp(otp_data: OTPVerify):
    """Verify OTP and complete registration or login"""
    # Find OTP
    stored_otp = await db.otps.find_one({"email": otp_data.email})
    if not stored_otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # Check if OTP matches and not expired
    if stored_otp["otp"] != otp_data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if datetime.utcnow() > stored_otp["expires_at"]:
        raise HTTPException(status_code=400, detail="OTP expired")
    
    # Delete used OTP (but keep permanent demo OTPs)
    if stored_otp.get("expires_at") and stored_otp["expires_at"] < datetime(2029, 1, 1):
        await db.otps.delete_one({"email": otp_data.email})
    
    # Check if this is registration or login
    existing_user = await db.users.find_one({"email": otp_data.email})
    
    if existing_user:
        # Login flow
        token = create_access_token({"email": existing_user["email"], "user_id": str(existing_user["_id"])})
        existing_user["_id"] = str(existing_user["_id"])
        return {
            "message": "Login successful",
            "token": token,
            "user": existing_user
        }
    else:
        # Registration flow - create user
        pending_user = await db.pending_users.find_one({"email": otp_data.email})
        if not pending_user:
            raise HTTPException(status_code=400, detail="Registration data not found")
        
        # Generate unique referral ID
        referral_id = generate_referral_id()
        while await db.users.find_one({"referral_id": referral_id}):
            referral_id = generate_referral_id()
        
        # Get sponsor info
        sponsor_id = None
        user_level = 0
        if pending_user.get("sponsor_referral_id"):
            sponsor = await db.users.find_one({"referral_id": pending_user["sponsor_referral_id"]})
            if sponsor:
                sponsor_id = str(sponsor["_id"])
                user_level = sponsor.get("level", 0) + 1
        
        # Create user
        new_user = User(
            email=pending_user["email"],
            name=pending_user["name"],
            mobile=pending_user["mobile"],
            address=pending_user["address"],
            pincode=pending_user["pincode"],
            referral_id=referral_id,
            sponsor_id=sponsor_id,
            level=user_level
        )
        
        result = await db.users.insert_one(new_user.dict(by_alias=True, exclude={"id"}))
        new_user.id = str(result.inserted_id)
        
        # Create referral relationships if sponsor exists
        if sponsor_id:
            await create_referral_chain(str(result.inserted_id), sponsor_id)
        
        # Delete pending user
        await db.pending_users.delete_one({"email": otp_data.email})
        
        # Send welcome email
        await send_welcome_email(new_user.email, new_user.name)
        
        # Create token
        token = create_access_token({"email": new_user.email, "user_id": str(result.inserted_id)})
        
        return {
            "message": "Registration successful",
            "token": token,
            "user": new_user.dict()
        }

async def create_referral_chain(new_user_id: str, sponsor_id: str):
    """Create referral relationships up to 9 levels"""
    current_sponsor_id = sponsor_id
    level = 1
    
    while current_sponsor_id and level <= 9:
        # Create referral record
        referral = Referral(
            referrer_id=current_sponsor_id,
            referred_user_id=new_user_id,
            level=level
        )
        await db.referrals.insert_one(referral.dict(by_alias=True, exclude={"id"}))
        
        # Get next level sponsor
        sponsor = await db.users.find_one({"_id": ObjectId(current_sponsor_id)})
        if sponsor and sponsor.get("sponsor_id"):
            current_sponsor_id = sponsor["sponsor_id"]
            level += 1
        else:
            break

@api_router.post("/auth/resend-otp")
async def resend_otp(login_data: UserLogin):
    """Resend OTP"""
    # Generate new OTP
    otp = generate_otp()
    otp_data = OTP(
        email=login_data.email,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    
    # Store OTP
    await db.otps.delete_many({"email": login_data.email})
    await db.otps.insert_one(otp_data.dict())
    
    # Send OTP email
    await send_email_otp(login_data.email, otp)
    
    return {"message": "OTP resent to your email"}

# ========================
# PRODUCT ROUTES
# ========================

@api_router.get("/products")
async def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
):
    """Get all products with optional filters"""
    query = {}
    if category:
        query["category"] = category
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    
    products = await db.products.find(query).skip(skip).limit(limit).to_list(limit)
    for product in products:
        product["_id"] = str(product["_id"])
    
    total = await db.products.count_documents(query)
    
    return {"products": products, "total": total, "skip": skip, "limit": limit}

@api_router.get("/products/{product_id}")
async def get_product(product_id: str):
    """Get single product by ID"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["_id"] = str(product["_id"])
    return product

@api_router.post("/products", response_model=Product)
async def create_product(product: ProductCreate):
    """Create new product (Admin only - will add auth later)"""
    product_dict = product.dict()
    product_dict["created_at"] = datetime.utcnow()
    result = await db.products.insert_one(product_dict)
    
    created_product = await db.products.find_one({"_id": result.inserted_id})
    created_product["_id"] = str(created_product["_id"])
    return created_product

@api_router.get("/categories")
async def get_categories():
    """Get all unique categories"""
    categories = await db.products.distinct("category")
    return {"categories": categories}

# ========================
# CART ROUTES
# ========================

@api_router.get("/cart/{user_id}")
async def get_cart(user_id: str):
    """Get user's cart"""
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart:
        # Create empty cart
        cart = Cart(user_id=user_id)
        await db.carts.insert_one(cart.dict(by_alias=True, exclude={"id"}))
        cart = await db.carts.find_one({"user_id": user_id})
    
    cart["_id"] = str(cart["_id"])
    
    # Fetch product details for each cart item
    cart_items_with_details = []
    for item in cart.get("items", []):
        if ObjectId.is_valid(item["product_id"]):
            product = await db.products.find_one({"_id": ObjectId(item["product_id"])})
            if product:
                product["_id"] = str(product["_id"])
                cart_items_with_details.append({
                    **item,
                    "product": product
                })
    
    cart["items"] = cart_items_with_details
    return cart

@api_router.post("/cart/{user_id}/add")
async def add_to_cart(user_id: str, item: CartUpdate):
    """Add item to cart"""
    # Get or create cart
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart:
        cart = Cart(user_id=user_id, items=[])
        await db.carts.insert_one(cart.dict(by_alias=True, exclude={"id"}))
        cart = await db.carts.find_one({"user_id": user_id})
    
    # Check if product exists
    if not ObjectId.is_valid(item.product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = await db.products.find_one({"_id": ObjectId(item.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already in cart
    items = cart.get("items", [])
    found = False
    for cart_item in items:
        if (cart_item["product_id"] == item.product_id and 
            cart_item.get("size") == item.size and 
            cart_item.get("color") == item.color):
            cart_item["quantity"] = item.quantity
            found = True
            break
    
    if not found:
        items.append(item.dict())
    
    # Update cart
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": items, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Item added to cart"}

@api_router.delete("/cart/{user_id}/remove/{product_id}")
async def remove_from_cart(user_id: str, product_id: str, size: Optional[str] = None, color: Optional[str] = None):
    """Remove item from cart"""
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    items = cart.get("items", [])
    items = [item for item in items if not (
        item["product_id"] == product_id and
        item.get("size") == size and
        item.get("color") == color
    )]
    
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": items, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Item removed from cart"}

@api_router.delete("/cart/{user_id}/clear")
async def clear_cart(user_id: str):
    """Clear entire cart"""
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": [], "updated_at": datetime.utcnow()}}
    )
    return {"message": "Cart cleared"}

# ========================
# WISHLIST ROUTES
# ========================

@api_router.get("/wishlist/{user_id}")
async def get_wishlist(user_id: str):
    """Get user's wishlist"""
    wishlist = await db.wishlists.find_one({"user_id": user_id})
    if not wishlist:
        wishlist = Wishlist(user_id=user_id)
        await db.wishlists.insert_one(wishlist.dict(by_alias=True, exclude={"id"}))
        wishlist = await db.wishlists.find_one({"user_id": user_id})
    
    wishlist["_id"] = str(wishlist["_id"])
    
    # Fetch product details
    products = []
    for product_id in wishlist.get("product_ids", []):
        if ObjectId.is_valid(product_id):
            product = await db.products.find_one({"_id": ObjectId(product_id)})
            if product:
                product["_id"] = str(product["_id"])
                products.append(product)
    
    wishlist["products"] = products
    return wishlist

@api_router.post("/wishlist/{user_id}/add/{product_id}")
async def add_to_wishlist(user_id: str, product_id: str):
    """Add product to wishlist"""
    # Verify product exists
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get or create wishlist
    wishlist = await db.wishlists.find_one({"user_id": user_id})
    if not wishlist:
        wishlist = Wishlist(user_id=user_id, product_ids=[product_id])
        await db.wishlists.insert_one(wishlist.dict(by_alias=True, exclude={"id"}))
    else:
        product_ids = wishlist.get("product_ids", [])
        if product_id not in product_ids:
            product_ids.append(product_id)
            await db.wishlists.update_one(
                {"user_id": user_id},
                {"$set": {"product_ids": product_ids, "updated_at": datetime.utcnow()}}
            )
    
    return {"message": "Product added to wishlist"}

@api_router.delete("/wishlist/{user_id}/remove/{product_id}")
async def remove_from_wishlist(user_id: str, product_id: str):
    """Remove product from wishlist"""
    wishlist = await db.wishlists.find_one({"user_id": user_id})
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    
    product_ids = wishlist.get("product_ids", [])
    if product_id in product_ids:
        product_ids.remove(product_id)
        await db.wishlists.update_one(
            {"user_id": user_id},
            {"$set": {"product_ids": product_ids, "updated_at": datetime.utcnow()}}
        )
    
    return {"message": "Product removed from wishlist"}

# ========================
# ORDER ROUTES
# ========================

@api_router.post("/orders/{user_id}")
async def create_order(user_id: str, order_data: OrderCreate):
    """Create new order"""
    # Get user
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate totals
    subtotal = sum(item.price * item.quantity for item in order_data.items)
    discount_amount = 0.0
    
    # Apply subscription discount if applicable
    if user.get("subscription_status"):
        discount_amount = subtotal * 0.20  # 20% discount for subscribers
    
    total = subtotal - discount_amount
    
    # Apply wallet balance if requested
    wallet_used = 0.0
    if order_data.use_wallet:
        wallet_balance = user.get("wallet_balance", 0.0)
        if wallet_balance > 0:
            wallet_used = min(wallet_balance, total)
            total -= wallet_used
            
            # Deduct from wallet
            await db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"wallet_balance": -wallet_used}}
            )
            
            # Record wallet transaction
            wallet_txn = WalletTransaction(
                user_id=user_id,
                amount=-wallet_used,
                type="debit",
                source="purchase",
                description=f"Used for order payment"
            )
            await db.wallet_transactions.insert_one(wallet_txn.dict(by_alias=True, exclude={"id"}))
    
    # Generate order ID
    order_id = f"BFF{datetime.utcnow().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
    
    # Create order
    order = Order(
        order_id=order_id,
        user_id=user_id,
        items=order_data.items,
        subtotal=subtotal,
        discount_amount=discount_amount,
        total=total,
        shipping_address=order_data.shipping_address,
        payment_status="pending" if total > 0 else "completed",
        order_status="placed"
    )
    
    result = await db.orders.insert_one(order.dict(by_alias=True, exclude={"id"}))
    
    # Process referral commissions if order is paid
    if total == 0 or wallet_used > 0:  # At least partial payment made
        await process_referral_commissions(user_id, subtotal)
    
    order.id = str(result.inserted_id)
    return order.dict()

async def process_referral_commissions(buyer_user_id: str, order_amount: float):
    """Process commission for referrers up to 9 levels"""
    # Get all referral relationships for this user
    referrals = await db.referrals.find({"referred_user_id": buyer_user_id}).to_list(9)
    
    for referral in referrals:
        if referral["level"] <= 9:
            commission_amount = order_amount * 0.01  # 1% commission
            
            # Add to referrer's wallet with 31-day expiry
            expiry_date = datetime.utcnow() + timedelta(days=31)
            
            wallet_txn = WalletTransaction(
                user_id=referral["referrer_id"],
                amount=commission_amount,
                type="credit",
                source="commission",
                description=f"Level {referral['level']} referral commission",
                expiry_date=expiry_date,
                status="active"
            )
            await db.wallet_transactions.insert_one(wallet_txn.dict(by_alias=True, exclude={"id"}))
            
            # Update user wallet balance
            await db.users.update_one(
                {"_id": ObjectId(referral["referrer_id"])},
                {"$inc": {"wallet_balance": commission_amount, "total_commission_earned": commission_amount}}
            )
            
            # Update referral record
            await db.referrals.update_one(
                {"_id": referral["_id"]},
                {"$inc": {"total_commission_earned": commission_amount}}
            )

@api_router.get("/orders/{user_id}")
async def get_user_orders(user_id: str):
    """Get all orders for a user"""
    orders = await db.orders.find({"user_id": user_id}).sort("created_at", -1).to_list(100)
    for order in orders:
        order["_id"] = str(order["_id"])
    return {"orders": orders}

@api_router.get("/orders/{user_id}/{order_id}")
async def get_order(user_id: str, order_id: str):
    """Get specific order"""
    order = await db.orders.find_one({"order_id": order_id, "user_id": user_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order["_id"] = str(order["_id"])
    return order

# ========================
# WALLET ROUTES
# ========================

@api_router.get("/wallet/{user_id}")
async def get_wallet(user_id: str):
    """Get wallet balance and transactions"""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get recent transactions
    transactions = await db.wallet_transactions.find({"user_id": user_id}).sort("created_at", -1).limit(50).to_list(50)
    for txn in transactions:
        txn["_id"] = str(txn["_id"])
    
    return {
        "balance": user.get("wallet_balance", 0.0),
        "total_commission_earned": user.get("total_commission_earned", 0.0),
        "transactions": transactions
    }

# ========================
# SUBSCRIPTION ROUTES
# ========================

@api_router.post("/subscription/{user_id}/subscribe")
async def subscribe_user(user_id: str):
    """Subscribe user for ₹111"""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.get("subscription_status"):
        raise HTTPException(status_code=400, detail="User already subscribed")
    
    # Create subscription
    subscription = Subscription(user_id=user_id)
    await db.subscriptions.insert_one(subscription.dict(by_alias=True, exclude={"id"}))
    
    # Update user
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"subscription_status": True, "subscription_date": datetime.utcnow()}}
    )
    
    # TODO: Process payment of ₹111 when payment gateway is integrated
    
    return {"message": "Subscription successful", "benefits": subscription.benefits}

# ========================
# USER/PROFILE ROUTES
# ========================

@api_router.get("/user/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile"""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["_id"] = str(user["_id"])
    return user

@api_router.get("/user/{user_id}/referrals")
async def get_user_referrals(user_id: str):
    """Get user's referral tree"""
    # Get direct referrals (level 1)
    referrals = await db.referrals.find({"referrer_id": user_id}).to_list(100)
    
    referral_tree = []
    for ref in referrals:
        referred_user = await db.users.find_one({"_id": ObjectId(ref["referred_user_id"])})
        if referred_user:
            referral_tree.append({
                "user_id": str(referred_user["_id"]),
                "name": referred_user["name"],
                "email": referred_user["email"],
                "level": ref["level"],
                "commission_earned": ref["total_commission_earned"],
                "joined_at": referred_user["created_at"]
            })
    
    return {"referrals": referral_tree}

# ========================
# ADMIN PANEL ROUTES
# ========================

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

@api_router.post("/admin/login")
async def admin_login(data: AdminLogin):
    """Admin login with email/password"""
    admin = await db.admins.find_one({"email": data.email})
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not pwd_context.verify(data.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"email": admin["email"], "role": admin["role"], "admin": True})
    return {
        "token": token,
        "admin": {
            "email": admin["email"],
            "name": admin["name"],
            "role": admin["role"],
        }
    }

@api_router.get("/admin/dashboard")
async def admin_dashboard():
    """Admin dashboard stats"""
    total_products = await db.products.count_documents({})
    total_users = await db.users.count_documents({})
    total_orders = await db.orders.count_documents({})
    total_subscribers = await db.users.count_documents({"subscription_status": True})
    
    # Revenue
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$total"}}}]
    revenue_result = await db.orders.aggregate(pipeline).to_list(1)
    total_revenue = revenue_result[0]["total"] if revenue_result else 0
    
    # Commission stats
    commission_pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
    commission_result = await db.wallet_transactions.aggregate(
        [{"$match": {"type": "credit", "source": "commission"}}, *commission_pipeline]
    ).to_list(1)
    total_commissions = commission_result[0]["total"] if commission_result else 0
    
    # Recent orders
    recent_orders = await db.orders.find().sort("created_at", -1).limit(10).to_list(10)
    for order in recent_orders:
        order["_id"] = str(order["_id"])
    
    return {
        "total_products": total_products,
        "total_users": total_users,
        "total_orders": total_orders,
        "total_subscribers": total_subscribers,
        "total_revenue": total_revenue,
        "total_commissions": total_commissions,
        "recent_orders": recent_orders,
    }

@api_router.get("/admin/users")
async def admin_get_users(skip: int = 0, limit: int = 50):
    """Get all users for admin"""
    users = await db.users.find().skip(skip).limit(limit).to_list(limit)
    for u in users:
        u["_id"] = str(u["_id"])
    total = await db.users.count_documents({})
    return {"users": users, "total": total}

@api_router.get("/admin/orders")
async def admin_get_orders(skip: int = 0, limit: int = 50):
    """Get all orders for admin"""
    orders = await db.orders.find().sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    for o in orders:
        o["_id"] = str(o["_id"])
    total = await db.orders.count_documents({})
    return {"orders": orders, "total": total}

@api_router.put("/admin/orders/{order_id}/status")
async def admin_update_order_status(order_id: str, status: str):
    """Update order status"""
    result = await db.orders.update_one(
        {"order_id": order_id},
        {"$set": {"order_status": status}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order status updated to {status}"}

@api_router.get("/admin/products")
async def admin_get_products(skip: int = 0, limit: int = 50):
    """Get all products for admin"""
    products = await db.products.find().skip(skip).limit(limit).to_list(limit)
    for p in products:
        p["_id"] = str(p["_id"])
    total = await db.products.count_documents({})
    return {"products": products, "total": total}

@api_router.delete("/admin/products/{product_id}")
async def admin_delete_product(product_id: str):
    """Delete a product"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}

@api_router.get("/admin/commissions")
async def admin_get_commissions(skip: int = 0, limit: int = 50):
    """Get all commission transactions"""
    txns = await db.wallet_transactions.find({"source": "commission"}).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    for t in txns:
        t["_id"] = str(t["_id"])
    return {"commissions": txns}

# Serve Admin Panel HTML
from fastapi.responses import HTMLResponse

@api_router.get("/admin-panel", response_class=HTMLResponse)
async def serve_admin_panel():
    """Serve the admin panel SPA"""
    return ADMIN_HTML

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
