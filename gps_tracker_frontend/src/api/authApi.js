import axiosInstance from './axiosConfig'

export const login = (phone, password) =>
  axiosInstance.post('/accounts/login/', { phone, password })

export const register = ({ phone, password, full_name, email }) =>
  axiosInstance.post('/accounts/register/', { phone, password, full_name, email })

export const changePassword = (oldPassword, newPassword) =>
  axiosInstance.post('/accounts/change-password/', {
    old_password: oldPassword,
    new_password: newPassword,
  })
