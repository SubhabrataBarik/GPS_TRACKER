import { Circle } from '@react-google-maps/api'

const TYPE_COLORS = {
  home: '#16a34a',
  school: '#2563eb',
  custom: '#aa3bff',
}

function GeofenceCircle({ geofence }) {
  const color = TYPE_COLORS[geofence.type] || TYPE_COLORS.custom

  return (
    <Circle
      center={{ lat: geofence.lat, lng: geofence.lon }}
      radius={geofence.radius_meters}
      options={{
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.12,
      }}
    />
  )
}

export default GeofenceCircle
