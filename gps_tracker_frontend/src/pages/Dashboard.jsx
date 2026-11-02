import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { getDevices } from '../api/deviceApi'
import { setDevices } from '../store/trackingSlice'
import Navbar from '../components/Navbar'
import DeviceCard from '../components/DeviceCard'

function Dashboard() {
  const dispatch = useDispatch()
  const devices = useSelector((state) => state.tracking.devices)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false

    getDevices()
      .then(({ data }) => {
        if (!cancelled) dispatch(setDevices(data))
      })
      .catch(() => {
        if (!cancelled) setError('Could not load devices')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [dispatch])

  return (
    <div className="dashboard-page">
      <Navbar />

      <main className="device-grid-wrapper">
        {loading && <p className="dashboard-status">Loading devices…</p>}

        {!loading && error && (
          <p className="dashboard-status dashboard-status-error">{error}</p>
        )}

        {!loading && !error && devices.length === 0 && (
          <p className="dashboard-status">No devices registered yet</p>
        )}

        {!loading && !error && devices.length > 0 && (
          <div className="device-grid">
            {devices.map((device) => (
              <DeviceCard key={device.device_id} deviceId={device.device_id} />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

export default Dashboard
