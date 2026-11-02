import { useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'

import { logout } from '../store/authSlice'

function Navbar() {
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <span className="navbar-title">GPS Tracker</span>
      <button className="navbar-logout" onClick={handleLogout}>
        Logout
      </button>
    </nav>
  )
}

export default Navbar
