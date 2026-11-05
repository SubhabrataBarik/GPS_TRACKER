import { useEffect, useState } from 'react'

import { getTrackingSchedule, updateTrackingSchedule } from '../api/deviceApi'

function TrackingSchedulePanel({ deviceId }) {
  const [startTime, setStartTime] = useState('08:00')
  const [endTime, setEndTime] = useState('20:00')
  const [hoursPerDay, setHoursPerDay] = useState(null)
  const [estimatedCost, setEstimatedCost] = useState(null)
  const [ratePerHour, setRatePerHour] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const applySchedule = (data) => {
    setStartTime(data.start_time.slice(0, 5))
    setEndTime(data.end_time.slice(0, 5))
    setHoursPerDay(data.hours_per_day)
    setEstimatedCost(data.estimated_daily_cost)
    setRatePerHour(data.rate_per_hour)
  }

  useEffect(() => {
    let cancelled = false

    getTrackingSchedule(deviceId)
      .then(({ data }) => {
        if (!cancelled) applySchedule(data)
      })
      .catch(() => {
        if (!cancelled) setError('Could not load tracking schedule')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [deviceId])

  const handleSave = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess(false)
    setSaving(true)

    try {
      const { data } = await updateTrackingSchedule(deviceId, {
        start_time: startTime,
        end_time: endTime,
      })
      applySchedule(data)
      setSuccess(true)
    } catch (err) {
      setError(err.response?.data?.error || 'Could not update tracking schedule')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return <p className="dashboard-status">Loading tracking schedule…</p>
  }

  return (
    <form className="schedule-panel" onSubmit={handleSave}>
      <h2>Tracking Schedule</h2>
      <p className="auth-subtitle">
        Location pings are accepted only during this daily window. SOS always gets through.
      </p>

      {error && <p className="auth-error">{error}</p>}
      {success && <p className="auth-success">Schedule updated.</p>}

      <div className="schedule-time-row">
        <label>
          From
          <input
            type="time"
            value={startTime}
            onChange={(event) => setStartTime(event.target.value)}
            required
          />
        </label>

        <label>
          To
          <input
            type="time"
            value={endTime}
            onChange={(event) => setEndTime(event.target.value)}
            required
          />
        </label>
      </div>

      <div className="schedule-summary">
        <span>{hoursPerDay}h/day</span>
        <span>₹{ratePerHour}/hr</span>
        <strong>₹{estimatedCost}/day</strong>
      </div>

      <button type="submit" disabled={saving}>
        {saving ? 'Saving…' : 'Save schedule'}
      </button>
    </form>
  )
}

export default TrackingSchedulePanel
