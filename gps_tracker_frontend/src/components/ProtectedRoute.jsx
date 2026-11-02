import { Navigate, Outlet } from 'react-router-dom'

function ProtectedRoute() {
  const hasToken = Boolean(localStorage.getItem('access'))

  if (!hasToken) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}

export default ProtectedRoute
