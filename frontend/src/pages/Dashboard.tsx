import { useStatus } from "../hooks/useStatus";

export default function Dashboard() {
  const status = useStatus();

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>

      {!status ? (
        <p className="text-neutral-400">Chargement...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          <Card title="MIDI">
            <p className={status.midi_connected ? "text-green-400" : "text-red-400"}>
              {status.midi_connected ? "Connecté" : "Déconnecté"}
            </p>
          </Card>

          <Card title="LEDs">
            <p className={status.leds_on ? "text-green-400" : "text-red-400"}>
              {status.leds_on ? "Allumées" : "Éteintes"}
            </p>
          </Card>

          <Card title="FPS">
            <p className="text-blue-400">{status.fps}</p>
          </Card>

        </div>
      )}
    </div>
  );
}

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-neutral-800 p-4 rounded-xl shadow border border-neutral-700">
      <h3 className="text-lg font-semibold mb-2 text-neutral-300">{title}</h3>
      {children}
    </div>
  );
}