# LocalConnect Mobile

React Native (Expo) mobile app for LocalConnect.

## Setup

```bash
cd apps/mobile
npm install
```

## Running

```bash
npm start
```

Scan QR code with Expo app (iOS/Android)

## Building

```bash
eas build --platform ios
eas build --platform android
```

## Environment Variables

Create `.env`:
```
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY=...
```
