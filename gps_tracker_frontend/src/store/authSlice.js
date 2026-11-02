import { createSlice } from '@reduxjs/toolkit'

const loadStoredUser = () => {
  try {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: loadStoredUser(),
    accessToken: localStorage.getItem('access') || null,
    refreshToken: localStorage.getItem('refresh') || null,
  },
  reducers: {
    setCredentials(state, action) {
      const { user, tokens } = action.payload
      state.user = user
      state.accessToken = tokens.access
      state.refreshToken = tokens.refresh
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('access', tokens.access)
      localStorage.setItem('refresh', tokens.refresh)
    },
    logout(state) {
      state.user = null
      state.accessToken = null
      state.refreshToken = null
      localStorage.removeItem('user')
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    },
  },
})

export const { setCredentials, logout } = authSlice.actions
export default authSlice.reducer
