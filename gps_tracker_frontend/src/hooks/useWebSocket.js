import { useCallback, useEffect, useRef } from 'react'
import { useDispatch } from 'react-redux'

import { updateLocation } from '../store/trackingSlice'

const RECONNECT_DELAY = 3000

export function useWebSocket(deviceId) {
  const dispatch = useDispatch()
  const ws = useRef(null)
  const reconnectTimeout = useRef(null)
  const shouldReconnect = useRef(true)

  const connectRef = useRef(() => {})

  const connect = useCallback(() => {
    const socket = new WebSocket(`${import.meta.env.VITE_WS_BASE}/tracking/${deviceId}/`)
    ws.current = socket

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data)

      if (message.type === 'location') {
        dispatch(updateLocation(message))
      } else if (message.type === 'sos') {
        alert(`SOS alert from device ${message.device_id}`)
      }
    }

    socket.onclose = () => {
      if (shouldReconnect.current) {
        reconnectTimeout.current = setTimeout(() => connectRef.current(), RECONNECT_DELAY)
      }
    }
  }, [deviceId, dispatch])

  useEffect(() => {
    connectRef.current = connect
    shouldReconnect.current = true
    connect()

    return () => {
      shouldReconnect.current = false
      clearTimeout(reconnectTimeout.current)
      ws.current?.close()
    }
  }, [connect])
}
