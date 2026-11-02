import { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'

const MIN_SEND_INTERVAL_MS = 4000

function DeviceSimulator() {
  const { deviceId } = useParams()

  const [apiKey, setApiKey] = useState(
    () => localStorage.getItem(`sim_api_key_${deviceId}`) || '',
  )
  const [battery, setBattery] = useState(100)
  const [sharing, setSharing] = useState(false)
  const [lastPing, setLastPing] = useState(null)
  const [error, setError] = useState('')

  const watchIdRef = useRef(null)
  const lastSentAtRef = useRef(0)

  useEffect(() => {
    return () => {
      if (watchIdRef.current !== null) {
        navigator.geolocation.clearWatch(watchIdRef.current)
      }
    }
  }, [])

  const sendPing = async (lat, lon) => {
    try {
      await axios.post(
        `${import.meta.env.VITE_API_BASE}/devices/ingest/`,
        { device_id: deviceId, lat, lon, battery: Number(battery) },
        { headers: { 'X-API-Key': apiKey } },
      )
      setLastPing({ lat, lon, time: new Date().toLocaleTimeString() })
      setError('')
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          'Failed to send location',
      )
    }
  }

  const handleStart = () => {
    if (!apiKey) {
      setError('Enter the device API key first')
      return
    }

    if (!navigator.geolocation) {
      setError('Geolocation is not supported on this browser')
      return
    }

    localStorage.setItem(`sim_api_key_${deviceId}`, apiKey)
    setError('')

    const id = navigator.geolocation.watchPosition(
      (position) => {
        const now = Date.now()
        if (now - lastSentAtRef.current < MIN_SEND_INTERVAL_MS) return
        lastSentAtRef.current = now
        sendPing(position.coords.latitude, position.coords.longitude)
      },
      (geoError) => setError(geoError.message),
      { enableHighAccuracy: true, maximumAge: 5000, timeout: 15000 },
    )

    watchIdRef.current = id
    setSharing(true)
  }

  const handleStop = () => {
    if (watchIdRef.current !== null) {
      navigator.geolocation.clearWatch(watchIdRef.current)
      watchIdRef.current = null
    }
    setSharing(false)
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-brand">
          <h1>Device Simulator</h1>
          <p className="auth-subtitle">Sending live location as {deviceId}</p>
        </div>

        <div className="auth-form">
          {error && <p className="auth-error">{error}</p>}
          {lastPing && (
            <p className="auth-success">
              Sent {lastPing.lat.toFixed(5)}, {lastPing.lon.toFixed(5)} at {lastPing.time}
            </p>
          )}

          <label>
            Device API key
            <input
              type="text"
              value={apiKey}
              onChange={(event) => setApiKey(event.target.value)}
              placeholder="paste the device's api_key"
              disabled={sharing}
            />
          </label>

          <label>
            Battery %
            <input
              type="number"
              min="0"
              max="100"
              value={battery}
              onChange={(event) => setBattery(event.target.value)}
              disabled={sharing}
            />
          </label>

          {!sharing ? (
            <button type="button" onClick={handleStart}>
              Start sharing location
            </button>
          ) : (
            <button type="button" onClick={handleStop}>
              Stop sharing
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default DeviceSimulator
