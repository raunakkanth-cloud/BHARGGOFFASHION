#!/usr/bin/env python3
"""
Script to create permanent OTP for demo@bharggo.com
This OTP (111111) should never expire and work unlimited times.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

async def create_permanent_otp():
    """Create permanent OTP record in database"""
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Connected to MongoDB")
    
    # Check if permanent OTP already exists
    existing_otp = await db.otps.find_one({
        "email": "demo@bharggo.com",
        "expires_at": {"$gt": datetime(2029, 1, 1)}
    })
    
    if existing_otp:
        print(f"✓ Permanent OTP already exists for demo@bharggo.com")
        print(f"  OTP: {existing_otp['otp']}")
        print(f"  Expires: {existing_otp['expires_at']}")
    else:
        print("Creating permanent OTP for demo@bharggo.com...")
        
        # Delete any existing OTPs for this email
        result = await db.otps.delete_many({"email": "demo@bharggo.com"})
        print(f"  Deleted {result.deleted_count} existing OTP(s)")
        
        # Create permanent OTP
        permanent_otp = {
            "email": "demo@bharggo.com",
            "otp": "111111",
            "created_at": datetime.utcnow(),
            "expires_at": datetime(2030, 1, 1)  # Expires in 2030 (far future)
        }
        
        await db.otps.insert_one(permanent_otp)
        print(f"✓ Created permanent OTP for demo@bharggo.com")
        print(f"  OTP: 111111")
        print(f"  Expires: 2030-01-01")
    
    # Verify demo user exists
    demo_user = await db.users.find_one({"email": "demo@bharggo.com"})
    if demo_user:
        print(f"\n✓ Demo user exists:")
        print(f"  Name: {demo_user.get('name')}")
        print(f"  Email: {demo_user.get('email')}")
        print(f"  Subscription: {demo_user.get('subscription_status')}")
        print(f"  Wallet: ₹{demo_user.get('wallet_balance', 0)}")
    else:
        print("\n⚠ Demo user does not exist in database")
        print("  User should be created during first registration")
    
    client.close()
    print("\n✓ Script completed successfully")

if __name__ == "__main__":
    asyncio.run(create_permanent_otp())
