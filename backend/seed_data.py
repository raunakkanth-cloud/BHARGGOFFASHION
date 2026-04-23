"""
Seed script with demo account and 30+ products
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
import random
import string
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def generate_referral_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

products = [
    {"name": "Premium Cotton T-Shirt", "description": "Soft and comfortable premium cotton t-shirt perfect for everyday wear. Made with 100% organic cotton.", "category": "Men", "price": 599.0, "discount": 20.0, "sizes": ["S", "M", "L", "XL", "XXL"], "colors": ["White", "Black", "Navy", "Grey"], "rating": 4.5, "review_count": 150, "image_url": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400"},
    {"name": "Women's Floral Kurti", "description": "Beautiful floral printed kurti with elegant design. Perfect for casual and festive occasions.", "category": "Women", "price": 899.0, "discount": 30.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Pink", "Blue", "Green"], "rating": 4.7, "review_count": 200, "image_url": "https://images.unsplash.com/photo-1769063382706-8156b3b33eac?w=400"},
    {"name": "Denim Jeans - Slim Fit", "description": "Classic slim fit denim jeans with premium quality fabric and comfortable stretch.", "category": "Men", "price": 1299.0, "discount": 15.0, "sizes": ["28", "30", "32", "34", "36"], "colors": ["Blue", "Black", "Dark Wash"], "rating": 4.3, "review_count": 180, "image_url": "https://images.unsplash.com/photo-1775226236498-969b38fe7032?w=400"},
    {"name": "Kids Cartoon T-Shirt", "description": "Fun cartoon printed t-shirt for kids. Soft fabric, vibrant colors, machine washable.", "category": "Kids", "price": 399.0, "discount": 25.0, "sizes": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"], "colors": ["Red", "Yellow", "Blue"], "rating": 4.6, "review_count": 120, "image_url": "https://images.unsplash.com/photo-1652330310284-b8bd67f716e3?w=400"},
    {"name": "Women's Palazzo Pants", "description": "Comfortable palazzo pants with modern design. Breathable fabric for all-day comfort.", "category": "Women", "price": 799.0, "discount": 20.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Black", "Navy", "Maroon"], "rating": 4.4, "review_count": 95, "image_url": "https://images.unsplash.com/photo-1759840278471-462cf3fcebd3?w=400"},
    {"name": "Men's Formal Shirt", "description": "Premium formal shirt perfect for office wear. Wrinkle-resistant, easy iron fabric.", "category": "Men", "price": 999.0, "discount": 25.0, "sizes": ["38", "40", "42", "44"], "colors": ["White", "Light Blue", "Pink"], "rating": 4.5, "review_count": 160, "image_url": "https://images.unsplash.com/photo-1662011858094-fd9b363ed708?w=400"},
    {"name": "Ethnic Saree", "description": "Traditional saree with beautiful embroidery. Perfect for weddings and celebrations.", "category": "Women", "price": 1899.0, "discount": 35.0, "sizes": ["Free Size"], "colors": ["Red", "Green", "Blue", "Pink"], "rating": 4.8, "review_count": 250, "image_url": "https://images.unsplash.com/photo-1759840278862-ef629e9b0f64?w=400"},
    {"name": "Kids Party Dress", "description": "Adorable party dress for special occasions. Premium fabric with beautiful design.", "category": "Kids", "price": 699.0, "discount": 30.0, "sizes": ["2-3Y", "4-5Y", "6-7Y"], "colors": ["Pink", "Purple", "White"], "rating": 4.7, "review_count": 85, "image_url": "https://images.unsplash.com/photo-1759840278478-826c0d0f110e?w=400"},
    {"name": "Sports Track Pants", "description": "Comfortable track pants for sports and fitness. Quick-dry, moisture-wicking fabric.", "category": "Men", "price": 699.0, "discount": 15.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Black", "Grey", "Navy"], "rating": 4.2, "review_count": 140, "image_url": "https://images.unsplash.com/photo-1747321754748-6a19b9592d53?w=400"},
    {"name": "Women's Leggings", "description": "Stretchable and comfortable leggings. Perfect for workouts and casual wear.", "category": "Women", "price": 449.0, "discount": 20.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Black", "Grey", "Navy", "Brown"], "rating": 4.3, "review_count": 175, "image_url": "https://images.unsplash.com/photo-1657042760573-93f8e73faeeb?w=400"},
    # Additional products
    {"name": "Men's Polo T-Shirt", "description": "Classic polo t-shirt with collar. Premium cotton blend, perfect for casual outings.", "category": "Men", "price": 799.0, "discount": 18.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Red", "Green", "Blue", "White"], "rating": 4.4, "review_count": 130, "image_url": "https://images.unsplash.com/photo-1625910513413-5fc421e0d7cd?w=400"},
    {"name": "Women's Anarkali Suit", "description": "Stunning Anarkali suit with intricate embroidery. Perfect for festivals and parties.", "category": "Women", "price": 2499.0, "discount": 40.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Maroon", "Navy", "Teal"], "rating": 4.9, "review_count": 320, "image_url": "https://images.unsplash.com/photo-1759840278862-ef629e9b0f64?w=400"},
    {"name": "Kids School Uniform", "description": "Durable school uniform set. Comfortable, easy to wash, long-lasting fabric.", "category": "Kids", "price": 599.0, "discount": 10.0, "sizes": ["4-5Y", "6-7Y", "8-9Y", "10-11Y"], "colors": ["White/Blue", "White/Grey"], "rating": 4.1, "review_count": 90, "image_url": "https://images.unsplash.com/photo-1652330310284-b8bd67f716e3?w=400"},
    {"name": "Men's Casual Blazer", "description": "Lightweight casual blazer perfect for semi-formal events. Modern slim fit design.", "category": "Men", "price": 2999.0, "discount": 30.0, "sizes": ["38", "40", "42", "44"], "colors": ["Black", "Navy", "Grey"], "rating": 4.6, "review_count": 110, "image_url": "https://images.unsplash.com/photo-1662011858094-fd9b363ed708?w=400"},
    {"name": "Women's Silk Dupatta", "description": "Pure silk dupatta with beautiful prints. Adds elegance to any outfit.", "category": "Women", "price": 699.0, "discount": 22.0, "sizes": ["Free Size"], "colors": ["Red", "Orange", "Pink", "Green"], "rating": 4.5, "review_count": 145, "image_url": "https://images.unsplash.com/photo-1759840278471-462cf3fcebd3?w=400"},
    {"name": "Kids Winter Jacket", "description": "Warm and cozy winter jacket for kids. Water-resistant outer shell, fleece inner lining.", "category": "Kids", "price": 1299.0, "discount": 28.0, "sizes": ["4-5Y", "6-7Y", "8-9Y", "10-11Y"], "colors": ["Red", "Blue", "Black"], "rating": 4.7, "review_count": 78, "image_url": "https://images.unsplash.com/photo-1652330310284-b8bd67f716e3?w=400"},
    {"name": "Men's Kurta Pajama", "description": "Traditional kurta pajama set. Premium cotton fabric, comfortable for festive wear.", "category": "Men", "price": 1499.0, "discount": 20.0, "sizes": ["38", "40", "42", "44"], "colors": ["White", "Cream", "Light Blue"], "rating": 4.6, "review_count": 200, "image_url": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400"},
    {"name": "Women's Churidar Set", "description": "Elegant churidar set with matching dupatta. Perfect for daily and festive wear.", "category": "Women", "price": 1199.0, "discount": 25.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Pink", "Blue", "Green", "Yellow"], "rating": 4.5, "review_count": 165, "image_url": "https://images.unsplash.com/photo-1769063382706-8156b3b33eac?w=400"},
    {"name": "Kids Denim Shorts", "description": "Stylish denim shorts for active kids. Durable fabric with comfortable elastic waist.", "category": "Kids", "price": 449.0, "discount": 15.0, "sizes": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"], "colors": ["Blue", "Light Blue"], "rating": 4.3, "review_count": 65, "image_url": "https://images.unsplash.com/photo-1775226236498-969b38fe7032?w=400"},
    {"name": "Men's Chino Trousers", "description": "Smart casual chino trousers. Slim fit, comfortable stretch fabric for all-day wear.", "category": "Men", "price": 1099.0, "discount": 20.0, "sizes": ["28", "30", "32", "34", "36"], "colors": ["Khaki", "Navy", "Olive", "Black"], "rating": 4.4, "review_count": 155, "image_url": "https://images.unsplash.com/photo-1747321754748-6a19b9592d53?w=400"},
    {"name": "Women's Crop Top", "description": "Trendy crop top for young fashion lovers. Soft cotton, stylish prints.", "category": "Women", "price": 499.0, "discount": 30.0, "sizes": ["XS", "S", "M", "L"], "colors": ["White", "Black", "Pink", "Yellow"], "rating": 4.2, "review_count": 88, "image_url": "https://images.unsplash.com/photo-1657042760573-93f8e73faeeb?w=400"},
    {"name": "Men's Leather Belt", "description": "Genuine leather belt with premium buckle. Perfect accessory for formal and casual wear.", "category": "Accessories", "price": 599.0, "discount": 10.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Black", "Brown", "Tan"], "rating": 4.5, "review_count": 210, "image_url": "https://images.unsplash.com/photo-1625910513413-5fc421e0d7cd?w=400"},
    {"name": "Women's Handbag", "description": "Stylish handbag with multiple compartments. Premium PU leather, adjustable strap.", "category": "Accessories", "price": 1299.0, "discount": 35.0, "sizes": ["One Size"], "colors": ["Black", "Brown", "Red", "Beige"], "rating": 4.6, "review_count": 180, "image_url": "https://images.unsplash.com/photo-1659887347330-5bd7d335edaa?w=400"},
    {"name": "Kids Sneakers", "description": "Comfortable sneakers for active kids. Lightweight, non-slip sole, easy velcro closure.", "category": "Kids", "price": 899.0, "discount": 20.0, "sizes": ["8", "9", "10", "11", "12", "13"], "colors": ["White/Blue", "Black/Red", "Grey/Green"], "rating": 4.4, "review_count": 95, "image_url": "https://images.unsplash.com/photo-1652330310284-b8bd67f716e3?w=400"},
    {"name": "Men's Hoodie", "description": "Warm fleece hoodie with kangaroo pocket. Perfect for winter and casual outings.", "category": "Men", "price": 1199.0, "discount": 22.0, "sizes": ["S", "M", "L", "XL", "XXL"], "colors": ["Black", "Grey", "Navy", "Maroon"], "rating": 4.5, "review_count": 170, "image_url": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400"},
    {"name": "Women's Maxi Dress", "description": "Elegant floor-length maxi dress. Flowy fabric, perfect for summer and evening wear.", "category": "Women", "price": 1599.0, "discount": 28.0, "sizes": ["S", "M", "L", "XL"], "colors": ["Floral Print", "Solid Black", "Blue"], "rating": 4.7, "review_count": 135, "image_url": "https://images.unsplash.com/photo-1769063382706-8156b3b33eac?w=400"},
    {"name": "Unisex Sunglasses", "description": "Stylish UV400 protection sunglasses. Lightweight frame, polarized lenses.", "category": "Accessories", "price": 799.0, "discount": 15.0, "sizes": ["One Size"], "colors": ["Black", "Brown", "Blue Mirror"], "rating": 4.3, "review_count": 220, "image_url": "https://images.unsplash.com/photo-1625910513413-5fc421e0d7cd?w=400"},
    {"name": "Women's Ethnic Jhumkas", "description": "Beautiful traditional jhumka earrings. Gold plated, lightweight, hypoallergenic.", "category": "Accessories", "price": 349.0, "discount": 20.0, "sizes": ["One Size"], "colors": ["Gold", "Silver", "Oxidized"], "rating": 4.8, "review_count": 300, "image_url": "https://images.unsplash.com/photo-1759840278478-826c0d0f110e?w=400"},
    {"name": "Men's Running Shoes", "description": "Lightweight running shoes with cushioned sole. Breathable mesh upper, arch support.", "category": "Men", "price": 1999.0, "discount": 25.0, "sizes": ["7", "8", "9", "10", "11"], "colors": ["Black/White", "Grey/Blue", "Red/Black"], "rating": 4.5, "review_count": 190, "image_url": "https://images.unsplash.com/photo-1747321754748-6a19b9592d53?w=400"},
    {"name": "Kids Ethnic Wear Set", "description": "Traditional ethnic wear set for kids. Perfect for festivals and family functions.", "category": "Kids", "price": 999.0, "discount": 30.0, "sizes": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"], "colors": ["Gold/Red", "Blue/Gold", "Green/Gold"], "rating": 4.6, "review_count": 72, "image_url": "https://images.unsplash.com/photo-1759840278478-826c0d0f110e?w=400"},
]

# Demo user and admin
DEMO_USER_EMAIL = "demo@bharggo.com"
DEMO_USER_NAME = "Demo User"
ADMIN_EMAIL = "admin@bharggo.com"
ADMIN_PASSWORD = "admin123"

async def seed_database():
    print("Starting database seeding...")
    
    # Clear existing data
    await db.products.delete_many({})
    await db.users.delete_many({})
    await db.otps.delete_many({})
    await db.pending_users.delete_many({})
    await db.carts.delete_many({})
    await db.wishlists.delete_many({})
    await db.orders.delete_many({})
    await db.wallet_transactions.delete_many({})
    await db.referrals.delete_many({})
    await db.subscriptions.delete_many({})
    await db.admins.delete_many({})
    print("Cleared existing data")
    
    # Insert products
    for p in products:
        p["created_at"] = datetime.utcnow()
        p["images"] = []
        p["videos"] = []
        p["variants"] = []
    result = await db.products.insert_many(products)
    print(f"Inserted {len(result.inserted_ids)} products")
    
    # Create demo user (pre-registered, no OTP needed)
    demo_referral = generate_referral_id()
    demo_user = {
        "email": DEMO_USER_EMAIL,
        "name": DEMO_USER_NAME,
        "mobile": "9876543210",
        "address": "123 Fashion Street, Mumbai",
        "pincode": "400001",
        "referral_id": demo_referral,
        "sponsor_id": None,
        "subscription_status": True,
        "subscription_date": datetime.utcnow(),
        "wallet_balance": 500.0,
        "total_commission_earned": 500.0,
        "level": 0,
        "created_at": datetime.utcnow(),
    }
    demo_result = await db.users.insert_one(demo_user)
    print(f"Created demo user: {DEMO_USER_EMAIL} (ID: {demo_result.inserted_id}, Referral: {demo_referral})")
    
    # Create admin accounts
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    admin1 = {
        "email": ADMIN_EMAIL,
        "password_hash": pwd_context.hash(ADMIN_PASSWORD),
        "name": "Super Admin",
        "role": "super_admin",
        "created_at": datetime.utcnow(),
    }
    admin2 = {
        "email": "admin2@bharggo.com",
        "password_hash": pwd_context.hash("admin123"),
        "name": "Super Admin 2",
        "role": "super_admin",
        "created_at": datetime.utcnow(),
    }
    await db.admins.insert_many([admin1, admin2])
    print(f"Created admin accounts: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    
    # Create indexes
    await db.products.create_index("category")
    await db.products.create_index("name")
    await db.users.create_index("email", unique=True)
    await db.users.create_index("referral_id", unique=True)
    await db.admins.create_index("email", unique=True)
    print("Created indexes")
    
    # Pre-create a fixed OTP for demo user so they can login easily
    await db.otps.insert_one({
        "email": DEMO_USER_EMAIL,
        "otp": "111111",
        "created_at": datetime.utcnow(),
        "expires_at": datetime(2030, 12, 31),  # Never expires for demo
    })
    print(f"Demo OTP set: 111111 (never expires)")
    
    print("\n" + "="*60)
    print("DEMO CREDENTIALS:")
    print(f"  Mobile App: {DEMO_USER_EMAIL} / OTP: 111111")
    print(f"  Admin Panel: {ADMIN_EMAIL} / Password: {ADMIN_PASSWORD}")
    print("="*60)
    print("\n✓ Database seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_database())
    client.close()
