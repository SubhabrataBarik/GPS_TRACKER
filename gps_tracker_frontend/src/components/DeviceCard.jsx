import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'

import { useLocation as useDeviceLocation } from '../hooks/useLocation'

function DeviceCard({ deviceId }) {
  const device = useSelector((state) =>
    state.tracking.devices.find((d) => d.device_id === deviceId),
  )
  const location = useDeviceLocation(deviceId)

  if (!device) return null

  const battery = location?.battery ?? device.battery
  const lastSeen = location?.timestamp ?? device.last_seen

  return (
    <Link to={`/devices/${device.device_id}`} className="device-card">
      <div className="device-card-header">
        <h2>{device.child_name}</h2>
        <span className={`device-status-badge device-status-${device.status}`}>
          {device.status}
        </span>
      </div>

      <p className="device-card-id">{device.device_id}</p>

      <div className="device-card-battery">
        <span>Battery</span>
        <strong>{battery}%</strong>
      </div>

      {lastSeen && (
        <p className="device-card-last-seen">
          Last seen {new Date(lastSeen).toLocaleString()}
        </p>
      )}
    </Link>
  )
}

export default DeviceCard
