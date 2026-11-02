import axiosInstance from './axiosConfig'

export const getDevices = () => axiosInstance.get('/devices/')
