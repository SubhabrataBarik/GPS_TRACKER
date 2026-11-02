import { useSelector } from 'react-redux'

function DeviceCard({ deviceId }) {
  const device = useSelector((state) =>
    state.tracking.devices.find((d) => d.device_id === deviceId),
  )

  if (!device) return null

  return (
    <div className="device-card">
      <div className="device-card-header">
        <h2>{device.child_name}</h2>
        <span className={`device-status-badge device-status-${device.status}`}>
          {device.status}
        </span>
      </div>

      <p className="device-card-id">{device.device_id}</p>

      <div className="device-card-battery">
        <span>Battery</span>
        <strong>{device.battery}%</strong>
      </div>

      {device.last_seen && (
        <p className="device-card-last-seen">
          Last seen {new Date(device.last_seen).toLocaleString()}
        </p>
      )}
    </div>
  )
}

export default DeviceCard
