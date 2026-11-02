import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import DeviceDetail from './pages/DeviceDetail'
import ProtectedRoute from './components/ProtectedRoute'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/devices/:deviceId" element={<DeviceDetail />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
