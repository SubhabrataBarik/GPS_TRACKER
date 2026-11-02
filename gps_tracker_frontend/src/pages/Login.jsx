import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'

import { login } from '../api/authApi'
import { setCredentials } from '../store/authSlice'

function Login() {
  const [countryCode, setCountryCode] = useState('+91')
  const [phone, setPhone] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleCountryCodeChange = (event) => {
    const digits = event.target.value.replace(/\D/g, '')
    setCountryCode(digits ? `+${digits}` : '')
  }

  const handlePhoneChange = (event) => {
    setPhone(event.target.value.replace(/\D/g, ''))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const { data } = await login(`${countryCode}${phone}`, password)
      dispatch(setCredentials({ user: data.user, tokens: data.tokens }))
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-brand">
          <h1>GPS Tracker</h1>
          <p className="auth-subtitle">Sign in to track your children</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {error && <p className="auth-error">{error}</p>}

          <label>
            Phone number
            <div className="phone-input-group">
              <input
                className="country-code-input"
                type="text"
                inputMode="numeric"
                value={countryCode}
                onChange={handleCountryCodeChange}
                aria-label="Country code"
                maxLength={4}
                required
              />
              <input
                className="phone-number-input"
                type="tel"
                inputMode="numeric"
                value={phone}
                onChange={handlePhoneChange}
                placeholder="9876543210"
                aria-label="Phone number"
                required
              />
            </div>
          </label>

          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? 'Logging in…' : 'Log in'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default Login
