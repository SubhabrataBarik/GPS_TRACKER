import { GoogleMap, Marker, Polyline, useJsApiLoader } from '@react-google-maps/api'

import { useLocation } from '../hooks/useLocation'
import GeofenceCircle from './GeofenceCircle'

const containerStyle = { width: '100%', height: '100%' }

function LiveMap({ deviceId, geofences, history }) {
  const liveLocation = useLocation(deviceId)

  const { isLoaded, loadError } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_KEY,
  })

  const latestHistoryPoint = history[0]
  const current =
    liveLocation ||
    (latestHistoryPoint && { lat: latestHistoryPoint.lat, lon: latestHistoryPoint.lon })

  if (loadError) {
    return (
      <p className="dashboard-status dashboard-status-error">
        Failed to load Google Maps. Check VITE_GOOGLE_MAPS_KEY in .env.
      </p>
    )
  }

  if (!isLoaded) {
    return <p className="dashboard-status">Loading map…</p>
  }

  if (!current) {
    return <p className="dashboard-status">Waiting for location data…</p>
  }

  const center = { lat: current.lat, lng: current.lon }

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={16}>
      <Marker position={center} />

      {geofences.map((geofence) => (
        <GeofenceCircle key={geofence.id} geofence={geofence} />
      ))}

      {history.length > 1 && (
        <Polyline
          path={history.map((point) => ({ lat: point.lat, lng: point.lon }))}
          options={{ strokeColor: '#aa3bff', strokeWeight: 3 }}
        />
      )}
    </GoogleMap>
  )
}

export default LiveMap
