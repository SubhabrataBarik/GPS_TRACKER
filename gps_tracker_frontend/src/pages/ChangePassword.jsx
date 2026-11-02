import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { changePassword } from '../api/authApi'

function extractErrorMessage(err) {
  const data = err.response?.data

  if (!data) return 'Something went wrong'
  if (data.error) return data.error

  const firstField = Object.keys(data)[0]
  if (firstField && Array.isArray(data[firstField])) {
    return data[firstField][0]
  }

  return 'Something went wrong'
}

function ChangePassword() {
  const [oldPassword, setOldPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)

  const navigate = useNavigate()

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess(false)

    if (newPassword !== confirmPassword) {
      setError('New password and confirmation do not match')
      return
    }

    setLoading(true)

    try {
      await changePassword(oldPassword, newPassword)
      setSuccess(true)
      setOldPassword('')
      setNewPassword('')
      setConfirmPassword('')
    } catch (err) {
      setError(extractErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-brand">
          <h1>Change Password</h1>
          <p className="auth-subtitle">Confirm your current password to set a new one</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {error && <p className="auth-error">{error}</p>}
          {success && <p className="auth-success">Password changed successfully.</p>}

          <label>
            Current password
            <input
              type="password"
              value={oldPassword}
              onChange={(event) => setOldPassword(event.target.value)}
              required
            />
          </label>

          <label>
            New password
            <input
              type="password"
              value={newPassword}
              onChange={(event) => setNewPassword(event.target.value)}
              minLength={8}
              required
            />
          </label>

          <label>
            Confirm new password
            <input
              type="password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              minLength={8}
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? 'Updating…' : 'Update password'}
          </button>
        </form>

        <button className="auth-link-button" onClick={() => navigate('/')}>
          ← Back to Dashboard
        </button>
      </div>
    </div>
  )
}

export default ChangePassword
