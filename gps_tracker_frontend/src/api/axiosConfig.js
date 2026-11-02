import axios from 'axios'
import store from '../store'
import { setCredentials, logout } from '../store/authSlice'

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
})

axiosInstance.interceptors.request.use((config) => {
  const token = store.getState().auth.accessToken

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

let isRefreshing = false
let pendingRequests = []

const resolvePending = (token) => {
  pendingRequests.forEach(({ resolve }) => resolve(token))
  pendingRequests = []
}

const rejectPending = (error) => {
  pendingRequests.forEach(({ reject }) => reject(error))
  pendingRequests = []
}

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config: originalRequest, response } = error

    const isAuthEndpoint =
      originalRequest?.url?.includes('/accounts/login/') ||
      originalRequest?.url?.includes('/accounts/token/refresh/')

    if (response?.status !== 401 || isAuthEndpoint || originalRequest._retry) {
      return Promise.reject(error)
    }

    const refreshToken = store.getState().auth.refreshToken

    if (!refreshToken) {
      store.dispatch(logout())
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        pendingRequests.push({ resolve, reject })
      }).then((newAccessToken) => {
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return axiosInstance(originalRequest)
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    try {
      const { data } = await axios.post(
        `${import.meta.env.VITE_API_BASE}/accounts/token/refresh/`,
        { refresh: refreshToken },
      )

      store.dispatch(
        setCredentials({
          user: store.getState().auth.user,
          tokens: { access: data.access, refresh: data.refresh },
        }),
      )

      resolvePending(data.access)

      originalRequest.headers.Authorization = `Bearer ${data.access}`
      return axiosInstance(originalRequest)
    } catch (refreshError) {
      rejectPending(refreshError)
      store.dispatch(logout())
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  },
)

export default axiosInstance
