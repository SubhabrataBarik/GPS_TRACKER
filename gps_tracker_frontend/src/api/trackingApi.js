import axiosInstance from './axiosConfig'

export const getLocationHistory = (deviceId) =>
  axiosInstance.get(`/tracking/${deviceId}/history/`)
