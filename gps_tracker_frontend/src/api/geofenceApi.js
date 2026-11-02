import axiosInstance from './axiosConfig'

export const getGeofences = (childId) =>
  axiosInstance.get(`/alerts/geofences/${childId}/`)
