import { configureStore } from '@reduxjs/toolkit'
import authReducer from './authSlice'
import trackingReducer from './trackingSlice'

const store = configureStore({
  reducer: {
    auth: authReducer,
    tracking: trackingReducer,
  },
})

export default store
