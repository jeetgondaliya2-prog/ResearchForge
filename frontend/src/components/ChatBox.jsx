import { useState } from "react";
import { Send } from "lucide-react";
import { startResearch } from "../services/api";


function ChatBox({ onResult, onAgentChange }) {

  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  const handleSubmit = async (e) => {

    e.preventDefault();

    if (!query.trim()) {
      return;
    }


    setLoading(true);
    setError("");

    try {

      onAgentChange("Supervisor");

      const result = await startResearch(query);

      onAgentChange("Final Writer");

      onResult(result);

      setQuery("");

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Unable to connect to ResearchForge backend."
      );

    } finally {

      setLoading(false);

    }
  };


  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">

      <h2 className="text-white text-lg font-semibold mb-2">
        Start New Research
      </h2>

      <p className="text-slate-400 text-sm mb-5">
        Ask ResearchForge AI to investigate a research problem.
      </p>


      <form onSubmit={handleSubmit}>

        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Example: Research AI-based crop disease detection using deep learning..."
          rows="6"
          className="w-full bg-slate-950 border border-slate-700 rounded-lg p-4 text-white placeholder-slate-600 outline-none focus:border-purple-500 resize-none"
        />


        {error && (
          <p className="text-red-400 text-sm mt-3">
            {error}
          </p>
        )}


        <button
          type="submit"
          disabled={loading}
          className="mt-4 w-full bg-purple-600 hover:bg-purple-700 disabled:bg-slate-700 text-white py-3 rounded-lg flex items-center justify-center gap-2 transition"
        >

          <Send size={18} />

          {loading
            ? "Researching..."
            : "Start Research"
          }

        </button>

      </form>

    </div>
  );
}

export default ChatBox;