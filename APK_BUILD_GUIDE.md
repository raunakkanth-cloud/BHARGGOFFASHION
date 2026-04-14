# Bharggo Fashion - APK Build Guide

## Option 1: Test on Phone NOW (Expo Go - Fastest)
1. Download **Expo Go** app from Google Play Store
2. Open the app preview URL on your phone's browser
3. Scan the QR code shown on the Expo dev server

## Option 2: Build APK using EAS Build (Recommended for Production)

### Prerequisites
1. Install EAS CLI globally:
```bash
npm install -g eas-cli
```

2. Create an Expo account at https://expo.dev/signup

3. Login to EAS:
```bash
eas login
```

### Build APK (Android)
```bash
cd frontend

# Build APK for testing (internal distribution)
eas build --platform android --profile preview

# This will:
# - Upload your code to Expo servers
# - Build the APK in the cloud (~15-20 minutes)
# - Provide a download link for the APK
```

### Build for Production (Google Play Store)
```bash
# Build AAB (App Bundle) for Play Store
eas build --platform android --profile production
```

### Build iOS (Apple App Store)
```bash
# Requires Apple Developer Account ($99/year)
eas build --platform ios --profile production
```

## Option 3: Local APK Build (Advanced)
```bash
# Install Android SDK and configure ANDROID_HOME
# Then run:
npx expo run:android
```

## Important Notes
- The `eas.json` file is already configured in the project
- `app.json` has Android package name: `com.bharggo.fashion`
- For production, update the backend URL in `.env` to your production server
- APK builds require an Expo account (free tier available)

## Backend Deployment
For the APK to work, you'll need to deploy the backend to a production server:
1. Deploy FastAPI backend to AWS/GCP/Railway
2. Deploy MongoDB to MongoDB Atlas
3. Update `EXPO_PUBLIC_BACKEND_URL` in `.env` to production URL
4. Rebuild the APK with production config
