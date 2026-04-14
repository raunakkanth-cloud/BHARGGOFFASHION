# Bharggo FFashion India Pvt. Ltd. - Mobile App PRD

## Product Overview
Full-stack eCommerce + MLM (Multi-Level Marketing) mobile application built with Expo/React Native and FastAPI/MongoDB.

## Brand
- **Company**: Bharggo FFashion India Pvt. Ltd.
- **Theme Colors**: Saffron (#FF9933), Green (#138808)
- **Design**: Premium, Minimal, Fast-loading

## App Flow
- **Splash** → Home (guest browsing allowed)
- **Guest users** can browse products, categories, search/filter
- **Registration required** only when placing an order (cart checkout)
- **Subscription (₹111) is OPTIONAL** - not required for purchases
- **Logo** displayed on every screen (splash, home, products, cart, profile, login, register)
- **Frontend**: Expo (React Native), Expo Router, Zustand, Axios
- **Backend**: FastAPI, Motor (async MongoDB), JWT
- **Database**: MongoDB
- **Payment**: CCAvenue (to be integrated - user will provide credentials)
- **Email**: MOCKED (to be integrated with SendGrid/AWS SES)

## Features Implemented

### Phase 1: Core eCommerce
- [x] Email OTP Authentication (register, login, verify, resend)
- [x] Registration with name, email, mobile, address, pincode, referral code
- [x] Product catalog with search & category filters
- [x] Product images (Unsplash)
- [x] Cart management (add, remove, clear)
- [x] Wishlist management
- [x] Order creation with wallet support
- [x] User profiles

### Phase 2: MLM + Advanced Features
- [x] Splash screen with animated Bharggo logo
- [x] 9-level MLM referral system (1% commission per level)
- [x] 12-digit alphanumeric referral ID auto-generation
- [x] Wallet system with 31-day expiry tracking
- [x] Subscription system (₹111, 20% discount)
- [x] Digital Shopping Card (premium credit card UI, share)
- [x] Order tracking with status visualization
- [x] Legal pages (T&C, Privacy, Refund, Shipping)

### Pending Features
- [ ] CCAvenue payment integration (awaiting credentials)
- [ ] SendGrid/AWS SES email integration (awaiting credentials)
- [ ] Web Admin Panel
- [ ] Payout system (UPI/Bank transfer)
- [ ] Push notifications
- [ ] Product detail page with zoom/video
- [ ] Reviews & ratings

## API Endpoints
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/verify-otp
- POST /api/auth/resend-otp
- GET /api/products
- GET /api/products/{id}
- POST /api/products
- GET /api/categories
- GET /api/cart/{user_id}
- POST /api/cart/{user_id}/add
- DELETE /api/cart/{user_id}/remove/{product_id}
- DELETE /api/cart/{user_id}/clear
- GET /api/wishlist/{user_id}
- POST /api/wishlist/{user_id}/add/{product_id}
- DELETE /api/wishlist/{user_id}/remove/{product_id}
- POST /api/orders/{user_id}
- GET /api/orders/{user_id}
- GET /api/orders/{user_id}/{order_id}
- GET /api/wallet/{user_id}
- POST /api/subscription/{user_id}/subscribe
- GET /api/user/{user_id}
- GET /api/user/{user_id}/referrals

## Database Collections
- users, products, carts, wishlists, orders, wallet_transactions, referrals, subscriptions, otps, pending_users
