import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

images = {
    'Premium Cotton T-Shirt': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400',
    "Women's Floral Kurti": 'https://images.unsplash.com/photo-1769063382706-8156b3b33eac?w=400',
    'Denim Jeans - Men': 'https://images.unsplash.com/photo-1775226236498-969b38fe7032?w=400',
    'Kids Cartoon T-Shirt': 'https://images.unsplash.com/photo-1652330310284-b8bd67f716e3?w=400',
    "Women's Palazzo Pants": 'https://images.unsplash.com/photo-1759840278471-462cf3fcebd3?w=400',
    "Men's Formal Shirt": 'https://images.unsplash.com/photo-1662011858094-fd9b363ed708?w=400',
    'Ethnic Saree': 'https://images.unsplash.com/photo-1759840278862-ef629e9b0f64?w=400',
    'Kids Party Dress': 'https://images.unsplash.com/photo-1759840278478-826c0d0f110e?w=400',
    'Sports Track Pants': 'https://images.unsplash.com/photo-1747321754748-6a19b9592d53?w=400',
    "Women's Leggings": 'https://images.unsplash.com/photo-1657042760573-93f8e73faeeb?w=400',
}

async def update():
    for name, img_url in images.items():
        result = await db.products.update_one(
            {'name': name},
            {'$set': {'image_url': img_url}}
        )
        print(f'Updated {name}: {result.modified_count}')
    client.close()

asyncio.run(update())
