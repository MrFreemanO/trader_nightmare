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
    host: true,
    port: 3000,
  },
  preview: {
    port: 3000,
  },
})
