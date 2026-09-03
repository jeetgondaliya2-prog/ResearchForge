import { useState, useEffect, useRef, useCallback } from "react";
import "./App.css";

// ── Constants ──────────────────────────────────────────────
const BACKEND = "http://127.0.0.1:8000";

// Agent descriptions defined FIRST to avoid ReferenceError
const AGENT_DESCRIPTIONS = {
  supervisor:        "Understands the research objective and coordinates the entire workflow.",
  planner:           "Converts the user query into a structured, step-by-step research plan.",
  web_research:      "Searches the web via Tavily for current solutions, technologies and trends.",
  academic_research: "Discovers peer-reviewed research papers, studies and academic findings.",
  rag_research:      "Retrieves relevant content from your uploaded documents using RAG + ChromaDB.",
  research_merge:    "Combines and deduplicates findings from web, academic and document research.",
  analyst:           "Synthesizes all research into a structured 10-part analysis.",
  feasibility:       "Evaluates technical, dataset, cost and implementation feasibility.",
  critic:            "Reviews the analysis for weaknesses, gaps and unsupported claims. May request revision.",
  final_writer:      "Writes the final 15-section professional research report based on all agent outputs.",
};

const PIPELINE = [
  { id: "supervisor",        label: "Supervisor",          icon: "🎯", desc: "Coordinating the research workflow" },
  { id: "planner",           label: "Planner",             icon: "🧠", desc: "Building a structured research plan" },
  { id: "web_research",      label: "Web Researcher",      icon: "🌐", desc: "Searching web sources via Tavily" },
  { id: "academic_research", label: "Academic Researcher", icon: "📚", desc: "Finding academic papers & studies" },
  { id: "rag_research",      label: "RAG Researcher",      icon: "📄", desc: "Searching uploaded documents" },
  { id: "research_merge",    label: "Research Merge",      icon: "🔗", desc: "Combining all research streams" },
  { id: "analyst",           label: "Analyst",             icon: "📊", desc: "Synthesizing evidence & analysis" },
  { id: "feasibility",       label: "Feasibility",         icon: "⚙️", desc: "Evaluating technical feasibility" },
  { id: "critic",            label: "Critic",              icon: "🔍", desc: "Reviewing & requesting revisions" },
  { id: "final_writer",      label: "Final Writer",        icon: "✍️", desc: "Writing the final research report" },
];

const DEMO_QUERIES = [
  {
    label: "AI in Education",
    icon: "🎓",
    query: "How can AI improve the education system in India? Find existing solutions, research papers, technologies, datasets, implementation challenges and research gaps.",
  },
  {
    label: "Healthcare Diagnostics",
    icon: "🏥",
    query: "How can AI agents improve healthcare diagnostics? What technologies, datasets, and existing solutions are available?",
  },
  {
    label: "Smart Cities",
    icon: "🏙️",
    query: "How can computer vision improve traffic management in Indian cities? Find existing systems, datasets and recommended architecture.",
  },
  {
    label: "Crop Disease Detection",
    icon: "🌿",
    query: "I want to build an AI system that detects crop diseases using images. What technologies, datasets, existing solutions and challenges should I consider?",
  },
];

// ── Helpers ────────────────────────────────────────────────

function parseSections(text) {
  if (!text) return null;
  const lines = text.split("\n");
  const sections = [];
  let current = null;

  for (const line of lines) {
    const h1 = line.match(/^#\s+(.+)/);
    const h2 = line.match(/^##\s+(.+)/);
    if (h1) {
      if (current) sections.push(current);
      current = { title: h1[1], level: 1, content: [] };
    } else if (h2) {
      if (current) sections.push(current);
      current = { title: h2[1], level: 2, content: [] };
    } else if (current) {
      current.content.push(line);
    }
  }
  if (current) sections.push(current);
  return sections.length > 0 ? sections : null;
}

function formatTimestamp(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleString("en-IN", {
      day: "2-digit", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  } catch {
    return iso;
  }
}

function downloadText(content, filename, mimeType = "text/plain") {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

// ── App ────────────────────────────────────────────────────
export default function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [agentIndex, setAgentIndex] = useState(-1);
  const [allDone, setAllDone] = useState(false);
  const [backendStatus, setBackendStatus] = useState("checking");
  const [scrolled, setScrolled] = useState(false);

  // Document upload state
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [uploadMessage, setUploadMessage] = useState("");
  const [documents, setDocuments] = useState([]);

  // Result tabs
  const [activeTab, setActiveTab] = useState("report");
  const [copied, setCopied] = useState(false);

  // History
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);

  // Nav tab
  const [activeNav, setActiveNav] = useState("research");

  const resultRef = useRef(null);
  const timerRef = useRef(null);

  // ── Backend health check ──────────────────────────────────
  useEffect(() => {
    fetch(`${BACKEND}/`)
      .then((r) => setBackendStatus(r.ok ? "online" : "offline"))
      .catch(() => setBackendStatus("offline"));
  }, []);

  // ── Scroll detection ──────────────────────────────────────
  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", fn);
    return () => window.removeEventListener("scroll", fn);
  }, []);

  // ── Pipeline step advancement during loading ──────────────
  useEffect(() => {
    if (!loading) {
      clearInterval(timerRef.current);
      return;
    }
    setAllDone(false);
    setAgentIndex(0);
    let idx = 0;
    // Advance roughly every 2.5s to simulate agent progression
    timerRef.current = setInterval(() => {
      idx += 1;
      if (idx >= PIPELINE.length - 1) {
        clearInterval(timerRef.current);
        setAgentIndex(PIPELINE.length - 1);
      } else {
        setAgentIndex(idx);
      }
    }, 2500);
    return () => clearInterval(timerRef.current);
  }, [loading]);

  // ── Load documents list ───────────────────────────────────
  const loadDocuments = useCallback(async () => {
    try {
      const res = await fetch(`${BACKEND}/api/documents/list`);
      const data = await res.json();
      setDocuments(data.documents || []);
    } catch {
      setDocuments([]);
    }
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  // ── Load history ──────────────────────────────────────────
  const loadHistory = useCallback(async () => {
    setHistoryLoading(true);
    try {
      const res = await fetch(`${BACKEND}/api/research/history?limit=20`);
      const data = await res.json();
      setHistory(data.history || []);
    } catch {
      setHistory([]);
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  const toggleHistory = () => {
    if (!showHistory) loadHistory();
    setShowHistory((v) => !v);
  };

  // ── Research ──────────────────────────────────────────────
  const startResearch = async () => {
    if (!query.trim()) { setError("Please enter a research question."); return; }
    setLoading(true);
    setError("");
    setResult(null);
    setActiveTab("report");
    setAllDone(false);

    try {
      const res = await fetch(`${BACKEND}/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_query: query }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || err.message || `Backend error ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
      setAllDone(true);
      setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth" }), 200);
    } catch (e) {
      setError(
        e.message?.includes("fetch")
          ? "Cannot connect to backend. Make sure FastAPI is running on port 8000."
          : e.message
      );
    } finally {
      setLoading(false);
    }
  };

  // ── Document upload ───────────────────────────────────────
  const uploadDocument = async () => {
    if (!uploadFile) return;
    setUploadStatus("uploading");
    setUploadMessage("");
    const form = new FormData();
    form.append("file", uploadFile);
    try {
      const res = await fetch(`${BACKEND}/api/documents/upload`, { method: "POST", body: form });
      const data = await res.json();
      if (data.status === "success") {
        setUploadStatus("success");
        setUploadMessage(data.message + " " + (data.ingestion || ""));
        setUploadFile(null);
        loadDocuments();
      } else {
        setUploadStatus("error");
        setUploadMessage(data.detail || data.message || "Upload failed.");
      }
    } catch {
      setUploadStatus("error");
      setUploadMessage("Upload failed. Make sure the backend is running.");
    }
  };

  const deleteDocument = async (filename) => {
    try {
      await fetch(`${BACKEND}/api/documents/${encodeURIComponent(filename)}`, { method: "DELETE" });
      loadDocuments();
    } catch {
      // ignore
    }
  };

  // ── Copy / Export ─────────────────────────────────────────
  const copyReport = () => {
    const text = result?.report || result?.final_report || "";
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const exportMarkdown = () => {
    const text = result?.report || result?.final_report || "";
    const q = (result?.user_query || "research").slice(0, 40).replace(/\s+/g, "_");
    downloadText(text, `ResearchForge_${q}.md`, "text/markdown");
  };

  const exportTxt = () => {
    const text = result?.report || result?.final_report || "";
    const q = (result?.user_query || "research").slice(0, 40).replace(/\s+/g, "_");
    downloadText(text, `ResearchForge_${q}.txt`, "text/plain");
  };

  // ── History actions ───────────────────────────────────────
  const loadHistoryEntry = (entry) => {
    setResult({
      user_query: entry.user_query,
      report: entry.final_report,
      final_report: entry.final_report,
      analysis: entry.analysis || "",
      feasibility: entry.feasibility || "",
      critique: entry.critique || "",
    });
    setActiveTab("report");
    setShowHistory(false);
    setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth" }), 200);
  };

  const deleteHistoryEntry = async (id) => {
    await fetch(`${BACKEND}/api/research/history/${id}`, { method: "DELETE" });
    loadHistory();
  };

  // ── Keyboard shortcut ─────────────────────────────────────
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) startResearch();
  };

  const reportText = result?.report || result?.final_report || "";
  const sections = parseSections(reportText);

  // Progress percentage
  const progressPct = loading
    ? Math.round(((agentIndex + 1) / PIPELINE.length) * 100)
    : allDone ? 100 : 0;

  return (
    <div className="app">

      {/* ── NAVBAR ── */}
      <nav className={`navbar ${scrolled ? "nb-scrolled" : ""}`}>
        <div className="logo">
          <span>⚡</span>ResearchForge<span className="ai-text"> AI</span>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#research">Research</a>
          <a href="#agents">Agents</a>
          <a href="#upload">Documents</a>
        </div>

        <div className="nav-end">
          <button className="history-btn" onClick={toggleHistory} title="Research History">
            🕒 History
          </button>
          <div className={`status-pill ${backendStatus}`}>
            <span className="dot" />
            {backendStatus === "checking" ? "Checking…"
              : backendStatus === "online" ? "Backend Online"
              : "Backend Offline"}
          </div>
        </div>
      </nav>

      {/* ── HISTORY PANEL ── */}
      {showHistory && (
        <div className="history-overlay" onClick={() => setShowHistory(false)}>
          <div className="history-panel" onClick={(e) => e.stopPropagation()}>
            <div className="history-header">
              <h3>🕒 Research History</h3>
              <button className="history-close" onClick={() => setShowHistory(false)}>✕</button>
            </div>
            {historyLoading ? (
              <div className="history-loading">Loading history…</div>
            ) : history.length === 0 ? (
              <div className="history-empty">
                <span>📭</span>
                <p>No research history yet.</p>
                <p>Run a research query to get started.</p>
              </div>
            ) : (
              <div className="history-list">
                {history.map((entry) => (
                  <div key={entry.id} className="history-item">
                    <div className="history-item-meta">
                      <span className="history-time">{formatTimestamp(entry.timestamp)}</span>
                      <span className="history-len">{entry.report_length.toLocaleString()} chars</span>
                    </div>
                    <p className="history-query">{entry.user_query}</p>
                    <p className="history-preview">{entry.report_preview}</p>
                    <div className="history-actions">
                      <button className="btn-load" onClick={() => loadHistoryEntry(entry)}>
                        Load Report
                      </button>
                      <button className="btn-del-history" onClick={() => deleteHistoryEntry(entry.id)}>
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── HERO ── */}
      <section className="hero" id="home">
        <div className="hero-glow" />
        <div className="badge-pill">
          <span className="badge-dot" />
          Multi-Agent AI Research Platform
        </div>
        <h1 className="hero-title">
          Research Smarter.<br />
          <span className="grad">Build Better.</span>
        </h1>
        <p className="hero-sub">
          ResearchForge AI uses <strong>10 specialized AI agents</strong> — Supervisor, Planner,
          Web Researcher, Academic Researcher, RAG Researcher, Analyst, Feasibility, Critic
          and Final Writer — to transform any research question into a structured, evidence-driven report.
        </p>
        <div className="hero-btns">
          <a href="#research" className="btn-primary">Start Research →</a>
          <a href="#agents" className="btn-ghost">See Agents</a>
        </div>
        <div className="hero-stats">
          <div className="stat"><span className="sval">10</span><span className="slbl">AI Agents</span></div>
          <div className="divider" />
          <div className="stat"><span className="sval">3</span><span className="slbl">Research Sources</span></div>
          <div className="divider" />
          <div className="stat"><span className="sval">15</span><span className="slbl">Report Sections</span></div>
          <div className="divider" />
          <div className="stat"><span className="sval">∞</span><span className="slbl">Topics</span></div>
        </div>
      </section>

      {/* ── RESEARCH INPUT ── */}
      <section className="section" id="research">
        <div className="section-tag">01 — Input</div>
        <h2 className="section-title">Start Your Research</h2>
        <p className="section-desc">
          Enter any research question, project idea, or technical problem below.
        </p>

        {/* Demo queries */}
        <div className="demo-queries">
          {DEMO_QUERIES.map((d) => (
            <button
              key={d.label}
              className="demo-btn"
              onClick={() => setQuery(d.query)}
              title={d.query}
            >
              <span>{d.icon}</span> {d.label}
            </button>
          ))}
        </div>

        <div className={`input-card ${loading ? "input-card--loading" : ""}`}>
          <div className="input-header">
            <span className="input-label">Research Question</span>
            <span className="input-hint">Ctrl+Enter to submit</span>
          </div>
          <textarea
            id="research-query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Example: I want to build an AI system that detects crop diseases using images. What technologies, datasets, existing solutions and challenges should I consider?"
            disabled={loading}
            rows={6}
          />
          {error && <div className="error-msg" role="alert">⚠ {error}</div>}
          <div className="input-footer">
            <span className="char-count">{query.length} characters</span>
            <button
              id="start-research-btn"
              className="btn-research"
              onClick={startResearch}
              disabled={loading || !query.trim()}
            >
              {loading ? <><span className="spin" /> Researching…</> : "Start Research →"}
            </button>
          </div>
        </div>
      </section>

      {/* ── LIVE PIPELINE ── */}
      {(loading || (allDone && result)) && (
        <section className="pipeline-section">
          <div className="section-tag">Live Pipeline</div>
          <h2 className="section-title">
            {loading ? "Research in Progress" : "Research Complete"}
          </h2>

          {/* Progress bar */}
          <div className="progress-bar-wrap">
            <div className="progress-bar-track">
              <div
                className="progress-bar-fill"
                style={{ width: `${progressPct}%` }}
              />
            </div>
            <span className="progress-pct">{progressPct}%</span>
          </div>

          <div className="pipeline-grid">
            {PIPELINE.map((step, i) => {
              const isDone = allDone || i < agentIndex;
              const isActive = !allDone && i === agentIndex;
              const status = isDone ? "done" : isActive ? "active" : "pending";
              return (
                <div key={step.id} className={`pipeline-card p-${status}`}>
                  <div className="pipeline-icon">
                    {isDone ? "✓" : step.icon}
                  </div>
                  <div className="pipeline-info">
                    <span className="pipeline-name">{step.label}</span>
                    <span className="pipeline-desc">
                      {isDone ? "Completed" : isActive ? step.desc : "Waiting…"}
                    </span>
                  </div>
                  {isActive && <div className="pipeline-spin" />}
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* ── RESULT ── */}
      {result && (
        <section className="result-section" ref={resultRef} id="results">
          <div className="section-tag">03 — Output</div>
          <h2 className="section-title">Research Report</h2>
          <p className="section-desc">Generated by the full 10-agent ResearchForge workflow.</p>

          {/* Tabs */}
          <div className="result-tabs">
            {[
              { id: "report",      label: "📋 Full Report" },
              { id: "analysis",   label: "📊 Analysis" },
              { id: "feasibility",label: "⚙️ Feasibility" },
              { id: "critique",   label: "🔍 Critic Review" },
            ].map((t) => (
              <button
                key={t.id}
                className={`tab-btn ${activeTab === t.id ? "tab-active" : ""}`}
                onClick={() => setActiveTab(t.id)}
              >
                {t.label}
              </button>
            ))}
          </div>

          <div className="result-card">
            <div className="result-header">
              <span className="result-done">✓ Research Complete</span>
              <div className="result-actions">
                <button className="copy-btn" onClick={copyReport}>
                  {copied ? "✓ Copied!" : "📋 Copy"}
                </button>
                <button className="export-btn" onClick={exportMarkdown} title="Download as Markdown">
                  ⬇ .md
                </button>
                <button className="export-btn" onClick={exportTxt} title="Download as Text">
                  ⬇ .txt
                </button>
              </div>
            </div>

            {/* Full Report */}
            {activeTab === "report" && (
              sections ? (
                <div className="report-sections">
                  {sections.map((sec, i) => (
                    <div key={i} className={`report-section lv${sec.level}`}>
                      {sec.level === 1
                        ? <h2 className="sec-h1">{sec.title}</h2>
                        : <h3 className="sec-h2">
                            <span className="sec-num">{String(i).padStart(2, "0")}</span>
                            {sec.title}
                          </h3>
                      }
                      <div className="sec-body">
                        {sec.content.filter(l => l.trim()).map((line, j) => {
                          if (line.startsWith("- ") || line.startsWith("* "))
                            return <div key={j} className="sec-bullet">• {line.replace(/^[-*]\s+/, "")}</div>;
                          if (/^\d+\./.test(line))
                            return <div key={j} className="sec-numbered">{line}</div>;
                          // Table rows
                          if (line.startsWith("|"))
                            return <div key={j} className="sec-table-row">{line}</div>;
                          // Code blocks
                          if (line.startsWith("```"))
                            return <div key={j} className="sec-code-marker">{line}</div>;
                          return <p key={j} className="sec-para">{line}</p>;
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <pre className="raw-pre">{reportText || JSON.stringify(result, null, 2)}</pre>
              )
            )}

            {/* Analysis Tab */}
            {activeTab === "analysis" && (
              <pre className="raw-pre">{result.analysis || "No analysis data available."}</pre>
            )}

            {/* Feasibility Tab */}
            {activeTab === "feasibility" && (
              <pre className="raw-pre">
                {typeof result.feasibility === "string"
                  ? result.feasibility
                  : result.feasibility?.analysis || "No feasibility data available."}
              </pre>
            )}

            {/* Critique Tab */}
            {activeTab === "critique" && (
              <pre className="raw-pre">{result.critique || "No critic review available."}</pre>
            )}
          </div>
        </section>
      )}

      {/* ── AGENTS ── */}
      <section className="section" id="agents">
        <div className="section-tag">02 — Pipeline</div>
        <h2 className="section-title">10 Specialized AI Agents</h2>
        <p className="section-desc">
          Each agent has a defined role. They collaborate in sequence through a LangGraph workflow
          with a built-in Critic revision loop.
        </p>

        {/* Workflow Diagram */}
        <div className="workflow-diagram">
          <div className="wf-row">
            <div className="wf-node wf-main">👤 User Question</div>
          </div>
          <div className="wf-arrow">↓</div>
          <div className="wf-row">
            <div className="wf-node wf-purple">🎯 Supervisor</div>
          </div>
          <div className="wf-arrow">↓</div>
          <div className="wf-row">
            <div className="wf-node wf-purple">🧠 Planner</div>
          </div>
          <div className="wf-arrow">↓</div>
          <div className="wf-row wf-parallel">
            <div className="wf-node wf-blue">🌐 Web Researcher</div>
            <div className="wf-node wf-blue">📚 Academic Researcher</div>
            <div className="wf-node wf-blue">📄 RAG Researcher</div>
          </div>
          <div className="wf-arrow">↓</div>
          <div className="wf-row">
            <div className="wf-node wf-teal">🔗 Research Merge</div>
          </div>
          <div className="wf-arrow">↓</div>
          <div className="wf-row wf-parallel">
            <div className="wf-node wf-indigo">📊 Analyst</div>
            <div className="wf-node wf-indigo">⚙️ Feasibility</div>
          </div>
          <div className="wf-arrow">↓</div>
          <div className="wf-row">
            <div className="wf-node wf-orange">🔍 Critic</div>
          </div>
          <div className="wf-arrow">↓</div>
          <div className="wf-row wf-parallel">
            <div className="wf-node wf-red">🔄 Revise → Analyst</div>
            <div className="wf-node wf-green">✅ PASS</div>
          </div>
          <div className="wf-arrow">↓</div>
          <div className="wf-row">
            <div className="wf-node wf-green">✍️ Final Writer → Report</div>
          </div>
        </div>

        <div className="agents-grid">
          {PIPELINE.map((agent, i) => (
            <div className="agent-card" key={i}>
              <div className="agent-icon">{agent.icon}</div>
              <div className="agent-num">Step {String(i + 1).padStart(2, "0")}</div>
              <h3>{agent.label}</h3>
              <p>{AGENT_DESCRIPTIONS[agent.id]}</p>
              <div className="agent-ready"><span className="green-dot" /> Ready</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── DOCUMENT UPLOAD ── */}
      <section className="section" id="upload">
        <div className="section-tag">04 — RAG</div>
        <h2 className="section-title">Upload Documents</h2>
        <p className="section-desc">
          Upload PDF, DOCX or TXT files to enhance research with your own documents.
          The RAG Researcher agent will search them during the workflow.
        </p>

        <div className="upload-card">
          <div className="upload-area" onClick={() => document.getElementById("file-input").click()}>
            <div className="upload-icon">📁</div>
            <p>{uploadFile ? uploadFile.name : "Click or drag to upload a PDF / DOCX / TXT"}</p>
            <span className="upload-hint">Supported: PDF, DOCX, TXT, MD</span>
          </div>
          <input
            id="file-input"
            type="file"
            accept=".pdf,.docx,.txt,.md"
            hidden
            onChange={(e) => { setUploadFile(e.target.files[0]); setUploadStatus(""); setUploadMessage(""); }}
          />
          {uploadFile && (
            <div className="upload-footer">
              <span className="upload-filename">📄 {uploadFile.name}</span>
              <button className="btn-upload" onClick={uploadDocument} disabled={uploadStatus === "uploading"}>
                {uploadStatus === "uploading" ? "Uploading…" : "Upload for RAG"}
              </button>
            </div>
          )}
          {uploadStatus === "success" && (
            <div className="upload-success">✓ {uploadMessage || "Document uploaded and ingested into RAG!"}</div>
          )}
          {uploadStatus === "error" && (
            <div className="upload-error">✗ {uploadMessage || "Upload failed. Make sure the backend is running."}</div>
          )}
        </div>

        {/* Document Library */}
        {documents.length > 0 && (
          <div className="doc-library">
            <h3 className="doc-library-title">📚 Document Library ({documents.length})</h3>
            <div className="doc-list">
              {documents.map((doc) => (
                <div key={doc.filename} className="doc-item">
                  <div className="doc-icon">
                    {doc.extension === ".pdf" ? "📕" : doc.extension === ".docx" ? "📘" : "📄"}
                  </div>
                  <div className="doc-info">
                    <span className="doc-name">{doc.filename}</span>
                    <span className="doc-meta">
                      {(doc.size_bytes / 1024).toFixed(1)} KB · {formatTimestamp(doc.modified)}
                    </span>
                  </div>
                  <button
                    className="doc-delete"
                    onClick={() => deleteDocument(doc.filename)}
                    title="Delete document"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* ── ABOUT ── */}
      <section className="about-section">
        <div className="about-inner">
          <h2>One Question.<br /><span className="grad">Multiple AI Agents.</span></h2>
          <p>
            ResearchForge AI combines LangChain, LangGraph, RAG pipelines, Tavily web search
            and academic research into a single intelligent workflow — turning any research question
            into a structured 15-section professional report.
          </p>
          <div className="tech-chips">
            {["LangGraph", "LangChain", "Mistral AI", "FastAPI", "React + Vite", "ChromaDB", "Tavily", "arXiv", "RAG"].map((t) => (
              <span key={t} className="chip">{t}</span>
            ))}
          </div>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer>
        <div className="logo">
          <span>⚡</span>ResearchForge<span className="ai-text"> AI</span>
        </div>
        <p>Multi-Agent AI Research Platform · Built by Jeet Gondaliya</p>
        <p className="footer-sub">React · FastAPI · LangGraph · Mistral AI · ChromaDB · Tavily · arXiv</p>
      </footer>

    </div>
  );
}