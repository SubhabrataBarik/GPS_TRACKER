import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useSelector } from 'react-redux'

import { getLocationHistory } from '../api/trackingApi'
import { getGeofences } from '../api/geofenceApi'
import DeviceTracker from '../components/DeviceTracker'
import LiveMap from '../components/LiveMap'

function DeviceDetail() {
  const { deviceId } = useParams()
  const navigate = useNavigate()

  const device = useSelector((state) =>
    state.tracking.devices.find((d) => d.device_id === deviceId),
  )

  const [history, setHistory] = useState([])
  const [geofences, setGeofences] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!device) return undefined

    let cancelled = false

    Promise.all([getLocationHistory(deviceId), getGeofences(device.child_id)])
      .then(([historyRes, geofenceRes]) => {
        if (cancelled) return
        setHistory(historyRes.data)
        setGeofences(geofenceRes.data)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [deviceId, device])

  if (!device) {
    return (
      <div className="device-detail-page">
        <p className="dashboard-status">Device not found</p>
        <button onClick={() => navigate('/')}>Back to Dashboard</button>
      </div>
    )
  }

  return (
    <div className="device-detail-page">
      <DeviceTracker deviceId={deviceId} />

      <header className="device-detail-header">
        <button className="device-detail-back" onClick={() => navigate('/')}>
          ← Back
        </button>
        <h1>{device.child_name}</h1>
      </header>

      <div className="device-detail-map">
        {loading ? (
          <p className="dashboard-status">Loading map…</p>
        ) : (
          <LiveMap deviceId={deviceId} geofences={geofences} history={history} />
        )}
      </div>
    </div>
  )
}

export default DeviceDetail
