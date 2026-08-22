# DentAI Mobile — React Native

Mobile companion app for the DentAI CBCT AI Segmentation Platform.
Same dark medical theme as the web UI. Connects to your local FastAPI backend.

## Screens
- **Login** — JWT authentication
- **Signup** — Doctor registration
- **Forgot Password** — Reset via email
- **Dashboard** — KPI cards, recent scans, system status
- **Upload** — Document picker, upload progress, step indicator
- **History** — Searchable, filterable scan list
- **Results** — Per-region STL/DICOM exports
- **Profile** — Edit profile, change password, sign out

## Setup

### 1. Install dependencies
```bash
cd DentAI-Mobile
npm install
```

### 2. Configure backend URL
Edit `src/api/client.ts`:
```typescript
// Android emulator  → 10.0.2.2:8000  (default)
// Physical device   → your LAN IP, e.g. 192.168.1.5:8000
// Production        → https://your-domain.com
export const BASE_URL = 'http://10.0.2.2:8000';
```

### 3. Start the backend
```bash
cd "Dental (1)/Dental"
copy .env.example .env   # fill in DB_PASSWORD and JWT_SECRET_KEY
pip install -r requirements.txt
python setup_db.py
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Run on Android
```bash
# Start Metro bundler
npx react-native start

# In a new terminal
npx react-native run-android
```

### 5. Run on iOS (macOS only)
```bash
cd ios && pod install && cd ..
npx react-native run-ios
```

## Android Network Permission
The app needs internet permission. Add to `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
```
For physical device HTTP (not HTTPS), also add in `<application>`:
```xml
android:usesCleartextTraffic="true"
```

## Theme
All colours match the web CSS variables exactly:
- Background: `#080c18`
- Cards: `#111827`
- Accent: `#3b82f6` → `#06b6d4` gradient
- Text: `#e8edf5`

## Dependencies
- React Native 0.76.5
- React Navigation (Stack + Bottom Tabs)
- AsyncStorage (JWT token persistence)
- Axios (API calls)
- react-native-document-picker (file upload)
- react-native-linear-gradient (accent gradient)
- react-native-vector-icons
- react-native-toast-message
