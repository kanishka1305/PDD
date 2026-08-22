// ═══════════════════════════════════════════════════════════
// DentAI Mobile — API Client
// Connects to the same FastAPI backend as the web app.
// Change BASE_URL to your server IP when testing on a device.
// ═══════════════════════════════════════════════════════════
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Physical device — PC LAN IP
// 10.0.2.2 = emulator only
// For physical phone on same WiFi: use PC LAN IP
export const BASE_URL = 'http://172.23.51.65:8000';

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
});

// ── Request interceptor — attach JWT token ────────────────
client.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Response interceptor — handle 401 ────────────────────
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await AsyncStorage.multiRemove(['access_token', 'user']);
    }
    return Promise.reject(error);
  }
);

export default client;

// ── API helpers ───────────────────────────────────────────
export const api = {
  // Auth
  login: (email: string, password: string) =>
    client.post('/login', new URLSearchParams({ email, password }).toString()),

  signup: (name: string, license: string, email: string, password: string) =>
    client.post('/signup', new URLSearchParams({ name, license, email, password }).toString()),

  forgotPassword: (email: string) =>
    client.post('/forgot-password', new URLSearchParams({ email }).toString()),

  resetPassword: (token: string, new_password: string) =>
    client.post('/reset-password', new URLSearchParams({ token, new_password }).toString()),

  // Profile
  fetchProfile: (id: number) =>
    client.post('/fetch_profile', new URLSearchParams({ id: String(id) }).toString()),

  updateProfile: (id: number, data: Record<string, string>) =>
    client.post('/update_profile', new URLSearchParams({ id: String(id), ...data }).toString()),

  changePassword: (id: number, current_password: string, new_password: string) =>
    client.post('/change_password', new URLSearchParams({
      id: String(id), current_password, new_password,
    }).toString()),

  fetchCredentials: (doctor_id: number) =>
    client.post('/fetch_credentials', new URLSearchParams({ doctor_id: String(doctor_id) }).toString()),

  // Scans
  getScans: () => client.get('/scans'),

  // Upload — multipart
  uploadScan: (fileUri: string, fileName: string, mimeType: string) => {
    const fd = new FormData();
    fd.append('file', { uri: fileUri, name: fileName, type: mimeType } as any);
    return client.post('/upload', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    });
  },

  // Analysis
  analyze: (scan_id: number) =>
    client.post(`/analyze/${scan_id}`),

  // Download
  getStlUrl:    (scan_id: number) => `${BASE_URL}/stl/${scan_id}`,
  getRegionStlUrl: (scan_id: number, region: string) => `${BASE_URL}/stl-region/${scan_id}/${region}`,
  getDicomUrl:  (scan_id: number, region: string) => `${BASE_URL}/export-dicom/${scan_id}/${region}`,

  // Health
  health: () => client.get('/health'),
};
