import { useWebSocket } from '../hooks/useWebSocket'

function DeviceTracker({ deviceId }) {
  useWebSocket(deviceId)
  return null
}

export default DeviceTracker
