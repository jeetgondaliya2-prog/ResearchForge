import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const runResearch = async () => {
    if (!query.trim()) {
      setError("Please enter a research question.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/research",
        {
          user_query: query,
        }
      );

      console.log("Backend response:", response.data);

      setResult(response.data);
    } catch (err) {
      console.error(err);

      if (err.response) {
        setError(
          err.response.data?.detail ||
            "Backend returned an error."
        );
      } else {
        setError(
          "Unable to connect to backend. Make sure FastAPI is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo">
          ResearchForge <span>AI</span>
        </div>

        <div className="nav-links">
          <a href="#research">Research</a>
          <a href="#results">Results</a>
        </div>
      </nav>

      {/* HERO */}
      <section className="hero" id="research">

        <div className="hero-content">

          <div className="badge">
            ⚡ Multi-Agent AI Research System
          </div>

          <h1>
            Research smarter.
            <br />
            <span>Build better.</span>
          </h1>

          <p>
            ResearchForge AI uses multiple intelligent agents
            to research, analyze, validate and evaluate your
            project idea.
          </p>

        </div>

      </section>

      {/* RESEARCH BOX */}
      <section className="research-section">

        <div className="research-card">

          <h2>What do you want to research?</h2>

          <p className="subtitle">
            Enter your research question, project idea,
            or technical problem.
          </p>

          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Example: I want to build an AI-powered crop disease detection system..."
            rows={7}
          />

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          <button
            onClick={runResearch}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Researching...
              </>
            ) : (
              <>
                🔍 Start Research
              </>
            )}
          </button>

        </div>

      </section>

      {/* AGENTS */}
      <section className="agents-section">

        <h2>How ResearchForge Works</h2>

        <p className="section-description">
          Your research passes through multiple specialized
          AI agents.
        </p>

        <div className="agents-grid">

          <div className="agent-card">
            <div className="agent-icon">🎯</div>
            <h3>Supervisor</h3>
            <p>
              Understands the research objective and
              coordinates the workflow.
            </p>
          </div>

          <div className="agent-card">
            <div className="agent-icon">📋</div>
            <h3>Planner</h3>
            <p>
              Creates a structured research plan.
            </p>
          </div>

          <div className="agent-card">
            <div className="agent-icon">🌐</div>
            <h3>Web Researcher</h3>
            <p>
              Searches the web for current information
              and existing solutions.
            </p>
          </div>

          <div className="agent-card">
            <div className="agent-icon">📚</div>
            <h3>Academic Researcher</h3>
            <p>
              Finds relevant academic research and
              scientific information.
            </p>
          </div>

          <div className="agent-card">
            <div className="agent-icon">🧠</div>
            <h3>RAG Researcher</h3>
            <p>
              Uses your uploaded documents and knowledge
              base.
            </p>
          </div>

          <div className="agent-card">
            <div className="agent-icon">📊</div>
            <h3>Analyst</h3>
            <p>
              Combines research and produces structured
              analysis.
            </p>
          </div>

          <div className="agent-card">
            <div className="agent-icon">⚙️</div>
            <h3>Feasibility</h3>
            <p>
              Evaluates technical and practical
              feasibility.
            </p>
          </div>

          <div className="agent-card">
            <div className="agent-icon">🛡️</div>
            <h3>Critic</h3>
            <p>
              Reviews the research and requests
              improvements when necessary.
            </p>
          </div>

        </div>

      </section>

      {/* RESULTS */}
      {result && (
        <section className="results-section" id="results">

          <h2>Research Results</h2>

          <div className="result-card">

            {result.analysis && (
              <div className="result-block">
                <h3>📊 Analysis</h3>
                <pre>
                  {result.analysis}
                </pre>
              </div>
            )}

            {result.feasibility && (
              <div className="result-block">
                <h3>⚙️ Feasibility</h3>
                <pre>
                  {result.feasibility}
                </pre>
              </div>
            )}

            {result.critique && (
              <div className="result-block">
                <h3>🛡️ Critic Review</h3>
                <pre>
                  {result.critique}
                </pre>
              </div>
            )}

            {!result.analysis &&
              !result.feasibility &&
              !result.critique && (
                <pre>
                  {JSON.stringify(result, null, 2)}
                </pre>
              )}

          </div>

        </section>
      )}

      {/* FOOTER */}
      <footer>
        <p>
          ResearchForge AI © 2026
        </p>

        <p>
          Multi-Agent Research Assistant
        </p>
      </footer>

    </div>
  );
}

export default App;