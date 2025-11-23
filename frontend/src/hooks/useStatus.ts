import { useEffect, useState } from "react"
import { API_URL } from "../config"

export type Status = {
  midi_connected: boolean
  leds_on: boolean
  fps: number
}

export function useStatus() {
  const [status, setStatus] = useState<Status | null>(null)

  useEffect(() => {
    const fetchStatus = () => {
      fetch(`${API_URL}/api/status`)
        .then(res => res.json())
        .then(setStatus)
        .catch(err => console.error("Failed to fetch status:", err))
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 5000)

    return () => clearInterval(interval)
  }, [])

  return status
}
