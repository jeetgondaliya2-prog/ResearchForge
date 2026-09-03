import {
  Search,
  Bell,
  User,
} from "lucide-react";

function Navbar() {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950 flex items-center justify-between px-6">

      <div>
        <h1 className="text-xl font-bold text-white">
          ResearchForge AI
        </h1>

        <p className="text-xs text-slate-400">
          AI Research & Project Agent
        </p>
      </div>


      <div className="flex items-center gap-5">

        <button className="text-slate-400 hover:text-white">
          <Search size={20} />
        </button>

        <button className="text-slate-400 hover:text-white">
          <Bell size={20} />
        </button>

        <div className="flex items-center gap-2">

          <div className="w-9 h-9 rounded-full bg-purple-600 flex items-center justify-center">
            <User size={18} />
          </div>

          <span className="text-sm text-white">
            Researcher
          </span>

        </div>

      </div>

    </header>
  );
}

export default Navbar;