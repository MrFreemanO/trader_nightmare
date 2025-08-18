// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    emptyOutDir: true,
    rollupOptions: {
      external: ['lucide-react'], // ✅ добавлено для устранения ошибки импорта
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: [
      '3000-i929sy2oru5yitghw5g3i-6532622b.e2b.dev',
      'localhost',
      '127.0.0.1',
      '.e2b.dev'
    ],
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  preview: {
    port: 3000,
  },
})
