import { Link } from "react-router-dom";

type NavItemProps = {
  to: string;
  label: string;
  open: boolean;
};

export default function NavItem({ to, label, open }: NavItemProps) {
  return (
    <Link
      to={to}
      className="flex items-center gap-3 p-2 rounded-xl hover:bg-neutral-700 transition"
    >
      <span className="text-lg">•</span>
      {open && <span>{label}</span>}
    </Link>
  );
}
