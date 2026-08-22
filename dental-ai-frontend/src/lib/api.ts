import axios from 'axios'

const BASE = ''  // same origin via Vite proxy

export const api = axios.create({ baseURL: BASE })

/* ── Auth ── */
export const login = (email: string, password: string) =>
  api.post('/login', new URLSearchParams({ email, password }))

export const signup = (name: string, license: string, email: string, password: string) =>
  api.post('/signup', new URLSearchParams({ name, license, email, password }))

export const forgotPassword = (email: string) =>
  api.post('/forgot-password', new URLSearchParams({ email }))

export const resetPassword = (token: string, new_password: string) =>
  api.post('/reset-password', new URLSearchParams({ token, new_password }))

/* ── Scans ── */
export const getScans = () => api.get('/scans')
export const uploadScan = (file: File) => {
  const fd = new FormData(); fd.append('file', file)
  return api.post('/upload', fd)
}
export const analyzeScan = (scanId: number) =>
  api.post(`/analyze/${scanId}`)

/* ── Exports ── */
export const getStlUrl    = (scanId: number, region = 'full') => `/stl-region/${scanId}/${region}`
export const getDicomUrl  = (scanId: number, region = 'full') => `/export-dicom/${scanId}/${region}`
export const getSegImgUrl = (path: string) => `/results-img?path=${encodeURIComponent(path)}`

/* ── Health ── */
export const getHealth = () => api.get('/health')
