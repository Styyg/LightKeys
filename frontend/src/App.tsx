import { Routes, Route } from "react-router-dom";
import { useState } from "react";

import Sidebar from "./components/Sidebar/Sidebar";
import DashboardHeader from "./components/Header/DashboardHeader";
import { useStatus } from "./hooks/useStatus";

import Dashboard from "./pages/Dashboard";
import ColorModes from "./pages/ColorModes";
import EffectModes from "./pages/EffectModes";
import LiveView from "./pages/LiveView";
import AboutLogs from "./pages/AboutLogs";

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const status = useStatus();

  return (
    <div className="flex h-screen bg-neutral-900 text-white">
      
      {/* SIDEBAR */}
      <Sidebar open={sidebarOpen} toggle={() => setSidebarOpen(o => !o)} />

      {/* MAIN */}
      <div className="flex-1 p-4">
        <DashboardHeader status={status} />

        <div className="mt-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/color-modes" element={<ColorModes />} />
            <Route path="/effect-modes" element={<EffectModes />} />
            <Route path="/live-view" element={<LiveView />} />
            <Route path="/about" element={<AboutLogs />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}
