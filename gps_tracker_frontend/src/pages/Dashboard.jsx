import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'

import { logout } from '../store/authSlice'

function Dashboard() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const user = useSelector((state) => state.auth.user)

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  return (
    <div className="dashboard-page">
      <h1>Dashboard</h1>
      {user && <p>Welcome, {user.full_name}</p>}
      <button onClick={handleLogout}>Logout</button>
    </div>
  )
}

export default Dashboard
