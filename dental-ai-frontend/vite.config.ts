import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/upload':          { target: 'http://localhost:8000', changeOrigin: true },
      '/analyze':         { target: 'http://localhost:8000', changeOrigin: true },
      '/stl':             { target: 'http://localhost:8000', changeOrigin: true },
      '/stl-region':      { target: 'http://localhost:8000', changeOrigin: true },
      '/export-dicom':    { target: 'http://localhost:8000', changeOrigin: true },
      '/login':           { target: 'http://localhost:8000', changeOrigin: true },
      '/signup':          { target: 'http://localhost:8000', changeOrigin: true },
      '/forgot-password': { target: 'http://localhost:8000', changeOrigin: true },
      '/reset-password':  { target: 'http://localhost:8000', changeOrigin: true },
      '/scans':           { target: 'http://localhost:8000', changeOrigin: true },
      '/health':          { target: 'http://localhost:8000', changeOrigin: true },
      '/results-img':     { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
  build: {
    outDir: '../Dental (1)/Dental/app/static/react',
    emptyOutDir: true,
  },
})
