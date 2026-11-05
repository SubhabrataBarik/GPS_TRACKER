import axiosInstance from './axiosConfig'

export const getDevices = () => axiosInstance.get('/devices/')

export const getTrackingSchedule = (deviceId) =>
  axiosInstance.get(`/devices/${deviceId}/schedule/`)

export const updateTrackingSchedule = (deviceId, { start_time, end_time, ping_mode }) =>
  axiosInstance.patch(`/devices/${deviceId}/schedule/`, { start_time, end_time, ping_mode })
