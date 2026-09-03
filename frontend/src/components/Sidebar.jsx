import {
  LayoutDashboard,
  Search,
  FolderKanban,
  FileText,
  BarChart3,
  Settings,
} from "lucide-react";

function Sidebar({ activePage, setActivePage }) {

  const menuItems = [
    {
      name: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      name: "Research",
      icon: Search,
    },
    {
      name: "Projects",
      icon: FolderKanban,
    },
    {
      name: "Documents",
      icon: FileText,
    },
    {
      name: "Reports",
      icon: BarChart3,
    },
  ];


  return (
    <aside className="w-64 min-h-screen bg-slate-950 border-r border-slate-800 p-4">

      <div className="mb-8">

        <div className="text-2xl font-bold text-white">
          RF
        </div>

        <p className="text-xs text-slate-500 mt-1">
          ResearchForge
        </p>

      </div>


      <nav className="space-y-2">

        {menuItems.map((item) => {

          const Icon = item.icon;

          const active = activePage === item.name;

          return (
            <button
              key={item.name}
              onClick={() => setActivePage(item.name)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm transition ${
                active
                  ? "bg-purple-600 text-white"
                  : "text-slate-400 hover:bg-slate-800 hover:text-white"
              }`}
            >

              <Icon size={19} />

              {item.name}

            </button>
          );
        })}

      </nav>


      <div className="absolute bottom-5">

        <button className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-white">

          <Settings size={19} />

          Settings

        </button>

      </div>

    </aside>
  );
}

export default Sidebar;