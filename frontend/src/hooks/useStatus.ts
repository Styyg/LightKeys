import { useEffect, useState } from "react"

export type Status = {
  midi_connected: boolean
  leds_on: boolean
  fps: number
}

export function useStatus() {
  const [status, setStatus] = useState<Status | null>(null)

  useEffect(() => {
    const fetchStatus = () => {
      fetch("/api/status")
        .then(res => res.json())
        .then(setStatus)
        .catch(err => console.error("Failed to fetch status:", err))
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 1000)

    return () => clearInterval(interval)
  }, [])

  return status
}
