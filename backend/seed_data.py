"""
Seed script to populate the database with test data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Sample products data
products = [
    {
        "name": "Premium Cotton T-Shirt",
        "description": "Soft and comfortable premium cotton t-shirt perfect for everyday wear",
        "category": "Men",
        "price": 599.00,
        "discount": 20.0,
        "images": [],
        "videos": [],
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": ["White", "Black", "Navy", "Grey"],
        "variants": [],
        "rating": 4.5,
        "review_count": 150,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Women's Floral Kurti",
        "description": "Beautiful floral printed kurti with elegant design",
        "category": "Women",
        "price": 899.00,
        "discount": 30.0,
        "images": [],
        "videos": [],
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Pink", "Blue", "Green"],
        "variants": [],
        "rating": 4.7,
        "review_count": 200,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Denim Jeans - Men",
        "description": "Classic fit denim jeans with premium quality fabric",
        "category": "Men",
        "price": 1299.00,
        "discount": 15.0,
        "images": [],
        "videos": [],
        "sizes": ["28", "30", "32", "34", "36"],
        "colors": ["Blue", "Black"],
        "variants": [],
        "rating": 4.3,
        "review_count": 180,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Kids Cartoon T-Shirt",
        "description": "Fun cartoon printed t-shirt for kids",
        "category": "Kids",
        "price": 399.00,
        "discount": 25.0,
        "images": [],
        "videos": [],
        "sizes": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"],
        "colors": ["Red", "Yellow", "Blue"],
        "variants": [],
        "rating": 4.6,
        "review_count": 120,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Women's Palazzo Pants",
        "description": "Comfortable palazzo pants with modern design",
        "category": "Women",
        "price": 799.00,
        "discount": 20.0,
        "images": [],
        "videos": [],
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black", "Navy", "Maroon"],
        "variants": [],
        "rating": 4.4,
        "review_count": 95,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Men's Formal Shirt",
        "description": "Premium formal shirt perfect for office wear",
        "category": "Men",
        "price": 999.00,
        "discount": 25.0,
        "images": [],
        "videos": [],
        "sizes": ["38", "40", "42", "44"],
        "colors": ["White", "Light Blue", "Pink"],
        "variants": [],
        "rating": 4.5,
        "review_count": 160,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Ethnic Saree",
        "description": "Traditional saree with beautiful embroidery",
        "category": "Women",
        "price": 1899.00,
        "discount": 35.0,
        "images": [],
        "videos": [],
        "sizes": ["Free Size"],
        "colors": ["Red", "Green", "Blue", "Pink"],
        "variants": [],
        "rating": 4.8,
        "review_count": 250,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Kids Party Dress",
        "description": "Adorable party dress for special occasions",
        "category": "Kids",
        "price": 699.00,
        "discount": 30.0,
        "images": [],
        "videos": [],
        "sizes": ["2-3Y", "4-5Y", "6-7Y"],
        "colors": ["Pink", "Purple", "White"],
        "variants": [],
        "rating": 4.7,
        "review_count": 85,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Sports Track Pants",
        "description": "Comfortable track pants for sports and fitness",
        "category": "Men",
        "price": 699.00,
        "discount": 15.0,
        "images": [],
        "videos": [],
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black", "Grey", "Navy"],
        "variants": [],
        "rating": 4.2,
        "review_count": 140,
        "created_at": datetime.utcnow()
    },
    {
        "name": "Women's Leggings",
        "description": "Stretchable and comfortable leggings",
        "category": "Women",
        "price": 449.00,
        "discount": 20.0,
        "images": [],
        "videos": [],
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black", "Grey", "Navy", "Brown"],
        "variants": [],
        "rating": 4.3,
        "review_count": 175,
        "created_at": datetime.utcnow()
    }
]


async def seed_database():
    print("Starting database seeding...")
    
    # Clear existing products (optional - comment out if you want to keep existing data)
    # await db.products.delete_many({})
    # print("Cleared existing products")
    
    # Check if products already exist
    existing_count = await db.products.count_documents({})
    if existing_count > 0:
        print(f"Database already has {existing_count} products. Skipping seed.")
        return
    
    # Insert products
    result = await db.products.insert_many(products)
    print(f"Inserted {len(result.inserted_ids)} products")
    
    # Create indexes for better performance
    await db.products.create_index("category")
    await db.products.create_index("name")
    await db.users.create_index("email", unique=True)
    await db.users.create_index("referral_id", unique=True)
    print("Created indexes")
    
    print("✓ Database seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
    client.close()
