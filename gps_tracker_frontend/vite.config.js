import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const dirname = path.dirname(fileURLToPath(import.meta.url))
const certDir = path.resolve(dirname, '../certs')
const keyPath = path.join(certDir, 'dev-key.pem')
const certPath = path.join(certDir, 'dev-cert.pem')
const hasDevCert = fs.existsSync(keyPath) && fs.existsSync(certPath)

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    https: hasDevCert
      ? { key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) }
      : undefined,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
})
