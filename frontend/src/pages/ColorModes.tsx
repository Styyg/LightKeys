import { useState } from "react";

type ColorMode = {
  id: string;
  name: string;
  type: "static" | "gradient" | "rainbow" | "velocity";
};

// Exemple temporaire avant API
const MOCK_MODES: ColorMode[] = [
  { id: "1", name: "Static Color", type: "static" },
  { id: "2", name: "Gradient", type: "gradient" },
  { id: "3", name: "Rainbow", type: "rainbow" },
  { id: "4", name: "Velocity Color", type: "velocity" },
];

export default function ColorModes() {
  const [selected, setSelected] = useState<ColorMode | null>(null);

  return (
    <div className="flex gap-6">
      
      {/* LISTE DES MODES */}
      <div className="w-64 bg-neutral-800 p-4 rounded-xl flex flex-col gap-2">
        <h2 className="text-lg font-bold mb-2">Color Modes</h2>
        {MOCK_MODES.map((mode) => (
          <button
            key={mode.id}
            onClick={() => setSelected(mode)}
            className="p-2 rounded-lg bg-neutral-700 hover:bg-neutral-600 text-left"
          >
            {mode.name}
          </button>
        ))}
      </div>

      {/* DETAILS DU MODE */}
      <div className="flex-1 bg-neutral-800 p-4 rounded-xl">
        {!selected ? (
          <p className="text-neutral-400">Sélectionne un color mode</p>
        ) : (
          <ColorModeEditor mode={selected} />
        )}
      </div>
    </div>
  );
}

function ColorModeEditor({ mode }: { mode: ColorMode }) {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">{mode.name}</h2>

      {mode.type === "static" && <StaticColorEditor />}
      {mode.type === "gradient" && <GradientEditor />}
      {mode.type === "rainbow" && <RainbowEditor />}
      {mode.type === "velocity" && <VelocityEditor />}
    </div>
  );
}

function StaticColorEditor() {
  return <p>Static color editor (color picker ici)</p>;
}

function GradientEditor() {
  return <p>Gradient editor (couleurs A → B)</p>;
}

function RainbowEditor() {
  return <p>Rainbow editor (pas de paramètres)</p>;
}

function VelocityEditor() {
  return <p>Velocity → color mapping editor</p>;
}
