import {
  CheckCircle,
  LoaderCircle,
  Circle,
} from "lucide-react";


function AgentStatus({ currentAgent }) {

  const agents = [
    "Supervisor",
    "Planner",
    "Web Research",
    "Academic Research",
    "RAG Research",
    "Research Merge",
    "Analyst",
    "Feasibility",
    "Critic",
    "Final Writer",
  ];


  const currentIndex = agents.indexOf(currentAgent);


  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">

      <h2 className="text-white font-semibold mb-5">
        Research Pipeline
      </h2>


      <div className="space-y-3">

        {agents.map((agent, index) => {

          let status = "pending";

          if (currentIndex > index) {
            status = "completed";
          }

          if (currentAgent === agent) {
            status = "running";
          }


          return (
            <div
              key={agent}
              className="flex items-center gap-3"
            >

              {status === "completed" && (
                <CheckCircle
                  size={18}
                  className="text-green-500"
                />
              )}


              {status === "running" && (
                <LoaderCircle
                  size={18}
                  className="text-purple-500 animate-spin"
                />
              )}


              {status === "pending" && (
                <Circle
                  size={18}
                  className="text-slate-600"
                />
              )}


              <span
                className={`text-sm ${
                  status === "running"
                    ? "text-purple-400"
                    : status === "completed"
                    ? "text-green-400"
                    : "text-slate-500"
                }`}
              >
                {agent}
              </span>

            </div>
          );
        })}

      </div>

    </div>
  );
}

export default AgentStatus;