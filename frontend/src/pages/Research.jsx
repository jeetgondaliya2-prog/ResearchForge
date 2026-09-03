import { useState } from "react";

import ChatBox from "../components/ChatBox";
import AgentStatus from "../components/AgentStatus";
import ReportViewer from "../components/ReportViewer";


function Research() {

  const [currentAgent, setCurrentAgent] =
    useState("");

  const [result, setResult] =
    useState(null);


  return (
    <div className="space-y-6">

      <div>

        <h1 className="text-3xl font-bold text-white">
          AI Research Agent
        </h1>

        <p className="text-slate-400 mt-2">
          Give ResearchForge a research problem and let the
          multi-agent system investigate it.
        </p>

      </div>


      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

        <div className="xl:col-span-2">

          <ChatBox
            onResult={setResult}
            onAgentChange={setCurrentAgent}
          />

        </div>


        <AgentStatus
          currentAgent={currentAgent}
        />

      </div>


      <ReportViewer
        report={
          result?.final_report ||
          result?.report ||
          result?.analysis ||
          result
        }
      />

    </div>
  );
}

export default Research;