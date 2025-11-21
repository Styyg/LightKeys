import { type Status } from "../hooks/useStatus"

export default function DashboardHeader({ status }: { status: Status | null }) {
  return (
    <header className="bg-neutral-900 p-4 rounded-xl flex items-center gap-6 mb-6">
      <h1 className="text-xl font-bold">🎹 LightKeys</h1>

      <div className="flex items-center gap-2">
        <span className="text-neutral-400">MIDI :</span>
        <span className={status?.midi_connected ? "text-green-400" : "text-red-400"}>
          {status?.midi_connected ? "Connecté" : "Déconnecté"}
        </span>
      </div>

      <div className="flex items-center gap-2">
        <span className="text-neutral-400">LEDs :</span>
        <span className={status?.leds_on ? "text-green-400" : "text-red-400"}>
          {status?.leds_on ? "Allumées" : "Éteintes"}
        </span>
      </div>

      <div className="flex items-center gap-2">
        <span className="text-neutral-400">FPS :</span>
        <span className="text-blue-400">{status?.fps ?? "--"}</span>
      </div>
    </header>
  )
}
