import DashboardHeader from "./components/DashboardHeader"
import { useStatus } from "./hooks/useStatus"
import './App.css'

function App() {
  const status = useStatus()

  return (
    <div className="min-h-screen bg-neutral-950 text-white p-6">
      <DashboardHeader status={status} />

      {/* Ici on ajoutera les panneaux ColorModes et EffectModes */}
      <div className="text-neutral-400">
        Interface en construction...
      </div>
    </div>
  )
}

export default App
