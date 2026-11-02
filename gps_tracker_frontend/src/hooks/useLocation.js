import { useSelector } from 'react-redux'

export function useLocation(deviceId) {
  return useSelector((state) => state.tracking.locations[deviceId])
}
