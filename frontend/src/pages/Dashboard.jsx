import ResearchCard from "../components/ResearchCard";


function Dashboard() {

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold text-white">
          Research Dashboard
        </h1>

        <p className="text-slate-400 mt-2">
          Welcome to ResearchForge AI.
        </p>
      </div>


      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">

        <ResearchCard
          title="Research Projects"
          value="0"
        />

        <ResearchCard
          title="Documents"
          value="0"
        />

        <ResearchCard
          title="Reports"
          value="0"
        />

        <ResearchCard
          title="Agents"
          value="10"
        />

      </div>


      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">

        <h2 className="text-xl font-semibold text-white">
          How ResearchForge Works
        </h2>

        <p className="text-slate-400 mt-3 leading-7">
          ResearchForge AI uses multiple specialized AI agents
          to investigate a research problem, collect information,
          analyze evidence, evaluate feasibility and generate a
          final research report.
        </p>

      </div>

    </div>
  );
}

export default Dashboard;