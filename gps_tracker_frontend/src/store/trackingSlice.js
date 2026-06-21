import { createSlice } from '@reduxjs/toolkit'

const trackingSlice = createSlice({
  name: 'tracking',
  initialState: {
    devices: [],
    locations: {},
  },
  reducers: {
    setDevices(state, action) {
      state.devices = action.payload
    },
    updateLocation(state, action) {
      const { device_id, lat, lon, battery, timestamp } = action.payload
      state.locations[device_id] = { lat, lon, battery, timestamp }
    },
  },
})

export const { setDevices, updateLocation } = trackingSlice.actions
export default trackingSlice.reducer
