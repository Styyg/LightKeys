import NavItem from "./NavItem";

type SidebarProps = {
  open: boolean;
  toggle: () => void;
};

export default function Sidebar({ open, toggle }: SidebarProps) {
  return (
    <div
      className={`${open ? "w-56" : "w-16"} transition-all duration-300 bg-neutral-800 flex flex-col p-4 gap-4`}
    >
      <button
        className="mb-6 p-2 bg-neutral-700 rounded-xl hover:bg-neutral-600"
        onClick={toggle}
      >
        {open ? "←" : "→"}
      </button>

      <NavItem to="/" label="Dashboard" open={open} />
      <NavItem to="/color-modes" label="Color Modes" open={open} />
      <NavItem to="/effect-modes" label="Effect Modes" open={open} />
      <NavItem to="/live-view" label="Live View" open={open} />
      <NavItem to="/about" label="About / Logs" open={open} />
    </div>
  );
}
