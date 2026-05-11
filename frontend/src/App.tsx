import { useState, useEffect, useRef } from "react";
import Editor from "@monaco-editor/react";
import "./App.css";

const API = (import.meta as any).env?.VITE_API_URL || "http://127.0.0.1:8000";

interface Problem {
  id: string;
  folder: string;
  title: string;
  difficulty: string;
  language: string;
  description: string;
  instructions: string;
  expected_behavior: string;
  hints: string[];
  starter_code: string;
  completed?: boolean;
  problem_type?: "bug_fix" | "write_from_scratch";
  function_signature?: string;
}

interface TestResult {
  test: string;
  status: "pass" | "fail" | "error";
  expected?: any;
  got?: any;
  message?: string;
  input?: any;
}

interface DebugState {
  session_id: string;
  paused: boolean;
  running: boolean;
  finished: boolean;
  current_line: number;
  variables: Record<string, string>;
  call_stack: Array<{ function: string; line: number; file: string }>;
  error: string | null;
}

export default function App() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [selected, setSelected] = useState<Problem | null>(null);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [outputError, setOutputError] = useState("");
  const [submitResults, setSubmitResults] = useState<TestResult[]>([]);
  const [submitSummary, setSubmitSummary] = useState("");
  const [submitPassed, setSubmitPassed] = useState<boolean | null>(null);
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [activePanel, setActivePanel] = useState<"problems" | "debugger" | "settings">("problems");
  const [showHints, setShowHints] = useState(false);
  const [hintIndex, setHintIndex] = useState(0);
  const [debugState, setDebugState] = useState<DebugState | null>(null);
  const [debugging, setDebugging] = useState(false);
  const [progress, setProgress] = useState<Record<string, boolean>>({});
  const [filterLang, setFilterLang] = useState<string>("all");
  const [filterDiff, setFilterDiff] = useState<string>("all");
  const editorRef = useRef<any>(null);

  // Load problems and progress
  useEffect(() => {
    fetchProblems();
    fetch(`${API}/progress`).then(r => r.json()).then(setProgress).catch(() => {});
  }, []);

  const fetchProblems = () => {
    fetch(`${API}/problems`)
      .then(r => r.json())
      .then(data => setProblems(data))
      .catch(() => setProblems([]));
  };

  const loadProblem = (p: Problem) => {
    fetch(`${API}/problems/${p.language}/${p.folder}`)
      .then(r => r.json())
      .then(data => {
        setSelected(data);
        setCode(data.starter_code || "");
        clearResults();
        setShowHints(false);
        setHintIndex(0);
        if (debugging) stopDebug();
      });
  };

  const clearResults = () => {
    setOutput(""); setOutputError(""); setSubmitResults([]);
    setSubmitSummary(""); setSubmitPassed(null);
  };

  const handleRun = async () => {
    if (!selected) return;
    setRunning(true);
    setOutput(""); setOutputError(""); setSubmitResults([]); setSubmitPassed(null);
    try {
      const res = await fetch(`${API}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language: selected.language })
      });
      const data = await res.json();
      setOutput(data.output || "");
      setOutputError(data.error || "");
      if (!data.output && !data.error) setOutput("Code ran with no output.");
    } catch {
      setOutputError("Could not connect to backend.");
    } finally {
      setRunning(false);
    }
  };

  const handleSubmit = async () => {
    if (!selected) return;
    setSubmitting(true);
    setOutput(""); setOutputError(""); setSubmitResults([]); setSubmitPassed(null);
    try {
      const res = await fetch(`${API}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, problem_id: selected.folder, language: selected.language })
      });
      const data = await res.json();
      setSubmitPassed(data.passed);
      setSubmitSummary(data.summary || "");
      setSubmitResults(data.results || []);
      if (data.error) setOutputError(data.error);

      // Update progress if passed
      if (data.passed) {
        const newProgress = { ...progress, [selected.folder]: true };
        setProgress(newProgress);
        setProblems(prev => prev.map(p => p.folder === selected.folder ? { ...p, completed: true } : p));
        await fetch(`${API}/progress`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ problem_id: selected.folder, completed: true })
        });
      }
    } catch {
      setOutputError("Could not connect to backend.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleSkip = () => {
    if (!problems.length || !selected) return;
    const filtered = getFilteredProblems();
    const idx = filtered.findIndex(p => p.folder === selected.folder);
    loadProblem(filtered[(idx + 1) % filtered.length]);
  };

  const startDebug = async () => {
    if (!selected || selected.language !== "python") {
      setOutputError("Debugging only supports Python.");
      return;
    }
    setDebugging(true);
    setActivePanel("debugger");
    clearResults();
    try {
      const res = await fetch(`${API}/debug/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, breakpoints: [], language: "python" })
      });
      const data = await res.json();
      setDebugState(data);
    } catch {
      setOutputError("Could not start debugger.");
      setDebugging(false);
    }
  };

  const debugAction = async (action: "step" | "continue" | "stop") => {
    if (!debugState) return;
    if (action === "stop") {
      await fetch(`${API}/debug/stop`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: debugState.session_id })
      });
      setDebugState(null); setDebugging(false); return;
    }
    const res = await fetch(`${API}/debug/${action}`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: debugState.session_id })
    });
    const data = await res.json();
    setDebugState(data);
    if (data.finished) setDebugging(false);
  };

  const stopDebug = () => debugAction("stop");

  const showNextHint = () => {
    if (!selected) return;
    setShowHints(true);
    setHintIndex(prev => Math.min(prev + 1, (selected.hints?.length || 1) - 1));
  };

  const getFilteredProblems = () => {
    return problems.filter(p => {
      if (filterLang !== "all" && p.language !== filterLang) return false;
      if (filterDiff !== "all" && p.difficulty !== filterDiff) return false;
      return true;
    });
  };

  const completedCount = problems.filter(p => progress[p.folder] || p.completed).length;
  const diffColor = (d: string) => d === "easy" ? "#4ec94e" : d === "medium" ? "#f0a500" : "#e05555";
  const langLabel = (l: string) => l === "cpp" ? "C++" : l.charAt(0).toUpperCase() + l.slice(1);
  const editorLang = (l: string) => l === "cpp" ? "cpp" : l === "typescript" ? "typescript" : "python";

  const filteredProblems = getFilteredProblems();

  return (
    <div className="app">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-logo">🐛</div>
        {(["problems", "debugger", "settings"] as const).map(panel => (
          <button key={panel} className={`sidebar-btn ${activePanel === panel ? "active" : ""}`}
            onClick={() => setActivePanel(panel)} title={panel}>
            {panel === "problems" ? "📋" : panel === "debugger" ? "🔍" : "⚙️"}
          </button>
        ))}
        <div className="sidebar-progress" title={`${completedCount}/${problems.length} completed`}>
          <div className="progress-ring">
            <span className="progress-num">{completedCount}</span>
          </div>
        </div>
      </div>

      {/* Left Panel */}
      <div className="left-panel">

        {/* Problems Panel */}
        {activePanel === "problems" && (
          <div className="panel-content">
            {!selected ? (
              <>
                <h2 className="panel-title">Problems</h2>

                {/* Progress bar */}
                <div className="progress-bar-container">
                  <div className="progress-bar-label">
                    <span>{completedCount} / {problems.length} completed</span>
                    <span>{Math.round((completedCount / Math.max(problems.length, 1)) * 100)}%</span>
                  </div>
                  <div className="progress-bar-track">
                    <div className="progress-bar-fill" style={{ width: `${(completedCount / Math.max(problems.length, 1)) * 100}%` }} />
                  </div>
                </div>

                {/* Filters */}
                <div className="filter-row">
                  <select className="filter-select" value={filterLang} onChange={e => setFilterLang(e.target.value)}>
                    <option value="all">All Languages</option>
                    <option value="python">Python</option>
                    <option value="typescript">TypeScript</option>
                    <option value="cpp">C++</option>
                  </select>
                  <select className="filter-select" value={filterDiff} onChange={e => setFilterDiff(e.target.value)}>
                    <option value="all">All Difficulties</option>
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </div>

                {/* Problem list */}
                <div className="problem-list">
                  {filteredProblems.length === 0 && <p className="no-problems">No problems match your filters.</p>}
                  {filteredProblems.map(p => (
                    <div key={p.folder} className={`problem-card ${(progress[p.folder] || p.completed) ? "completed" : ""}`}
                      onClick={() => loadProblem(p)}>
                      <div className="problem-card-left">
                        <span className="completion-dot">{(progress[p.folder] || p.completed) ? "✓" : "○"}</span>
                      </div>
                      <div className="problem-card-info">
                        <div className="problem-card-title">{p.title}</div>
                        <div className="problem-card-meta">
                          <span className="lang-badge">{langLabel(p.language)}</span>
                          <span className="diff-badge" style={{ color: diffColor(p.difficulty) }}>{p.difficulty}</span>
                          {p.problem_type === "write_from_scratch" && <span className="type-badge">✏️ Write</span>}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <>
                <button className="back-btn" onClick={() => { setSelected(null); clearResults(); }}>← Back</button>

                {/* Completion badge */}
                {(progress[selected.folder] || selected.completed) && (
                  <div className="completed-banner">✓ Completed</div>
                )}

                <h2 className="panel-title">{selected.title}</h2>
                <div className="meta-row">
                  <span className="lang-badge">{langLabel(selected.language)}</span>
                  <span className="diff-badge" style={{ color: diffColor(selected.difficulty) }}>{selected.difficulty}</span>
                  {selected.problem_type === "write_from_scratch" && <span className="type-badge">✏️ Write from scratch</span>}
                </div>

                <div className="section-label">Description</div>
                <p className="panel-text">{selected.description}</p>

                <div className="section-label">Instructions</div>
                <p className="panel-text">{selected.instructions}</p>

                <div className="section-label">Expected Behavior</div>
                <p className="panel-text">{selected.expected_behavior}</p>

                {selected.function_signature && (
                  <>
                    <div className="section-label">Function Signature</div>
                    <pre className="signature-box">{selected.function_signature}</pre>
                  </>
                )}

                {/* Progressive hints */}
                {selected.hints?.length > 0 && (
                  <div className="hints-section">
                    {showHints && (
                      <div className="hints-list">
                        {selected.hints.slice(0, hintIndex + 1).map((h, i) => (
                          <div key={i} className="hint-item">
                            <span className="hint-num">Hint {i + 1}</span>
                            <span className="hint-text">{h}</span>
                          </div>
                        ))}
                      </div>
                    )}
                    {(!showHints || hintIndex < (selected.hints?.length || 0) - 1) && (
                      <button className="hints-toggle" onClick={showNextHint}>
                        {!showHints ? "Show Hint 1" : `Show Hint ${hintIndex + 2}`}
                      </button>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* Debugger Panel */}
        {activePanel === "debugger" && (
          <div className="panel-content">
            <h2 className="panel-title">Debugger</h2>

            {debugging && debugState ? (
              <div className="debug-controls">
                <button className="dbg-btn" onClick={() => debugAction("step")} disabled={!debugState.paused}>⏭ Step</button>
                <button className="dbg-btn" onClick={() => debugAction("continue")} disabled={!debugState.paused}>▶ Continue</button>
                <button className="dbg-btn dbg-stop" onClick={stopDebug}>■ Stop</button>
              </div>
            ) : (
              <button className="dbg-start-btn" onClick={startDebug}
                disabled={!selected || selected?.language !== "python"}>
                {!selected ? "Load a problem first" : selected.language !== "python" ? "Python only" : "▶ Start Debug"}
              </button>
            )}

            <div className="section-label">Status</div>
            <div className="debug-box">
              {!debugState ? <span className="debug-placeholder">No active session</span> : (
                <span style={{ color: debugState.finished ? "#e05555" : debugState.paused ? "#f0a500" : "#4ec94e", fontSize: 12 }}>
                  {debugState.finished ? `Finished${debugState.error ? ` — ${debugState.error}` : ""}` : debugState.paused ? `Paused at line ${debugState.current_line}` : "Running..."}
                </span>
              )}
            </div>

            <div className="section-label">Call Stack</div>
            <div className="debug-box" style={{ flexDirection: "column", alignItems: "flex-start", gap: 4 }}>
              {!debugState?.call_stack?.length ? <span className="debug-placeholder">No stack data</span>
                : debugState.call_stack.map((f, i) => (
                  <div key={i} style={{ fontSize: 11, color: "#e8e8f0", fontFamily: "JetBrains Mono, monospace" }}>
                    {f.function}() <span style={{ color: "#7a7a8c" }}>line {f.line}</span>
                  </div>
                ))}
            </div>

            <div className="section-label">Variables</div>
            <div className="debug-box" style={{ flexDirection: "column", alignItems: "flex-start", gap: 4 }}>
              {!debugState?.variables || Object.keys(debugState.variables).length === 0
                ? <span className="debug-placeholder">No variables</span>
                : Object.entries(debugState.variables).map(([k, v]) => (
                  <div key={k} style={{ fontSize: 11, fontFamily: "JetBrains Mono, monospace" }}>
                    <span style={{ color: "#7c6dfa" }}>{k}</span>
                    <span style={{ color: "#7a7a8c" }}> = </span>
                    <span style={{ color: "#4ec94e" }}>{v}</span>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Settings Panel */}
        {activePanel === "settings" && (
          <div className="panel-content">
            <h2 className="panel-title">Settings</h2>
            <div className="section-label">Languages</div>
            <p className="panel-text">Python — fully supported with execution and debugging. TypeScript and C++ — execution supported, debugging coming soon.</p>
            <div className="section-label">Progress</div>
            <p className="panel-text">{completedCount} of {problems.length} problems completed. Progress is saved for this session.</p>
            <button className="hints-toggle" style={{ marginTop: 12 }} onClick={() => {
              setProgress({});
              setProblems(prev => prev.map(p => ({ ...p, completed: false })));
            }}>Reset Progress</button>
          </div>
        )}
      </div>

      {/* Main Area */}
      <div className="main-area">
        <div className="editor-area">
          <div className="editor-header">
            <span className="editor-filename">
              {selected ? `${selected.title.toLowerCase().replace(/\s+/g, "_")}${selected.language === "python" ? ".py" : selected.language === "typescript" ? ".ts" : ".cpp"}` : "No problem loaded"}
            </span>
            <div className="editor-actions">
              {selected?.language === "python" && !debugging && (
                <button className="action-btn debug-btn" onClick={startDebug}>🔍 Debug</button>
              )}
              {debugging && <button className="action-btn debug-btn" onClick={stopDebug}>■ Stop</button>}
              <button className="action-btn run-btn" onClick={handleRun} disabled={running || !selected}>
                {running ? "Running..." : "▶ Run"}
              </button>
              <button className="action-btn submit-btn" onClick={handleSubmit} disabled={submitting || !selected}>
                {submitting ? "Checking..." : "✓ Submit"}
              </button>
              <button className="action-btn skip-btn" onClick={handleSkip} disabled={!selected}>⏭ Skip</button>
            </div>
          </div>

          <div className="editor-wrapper">
            <Editor
              height="100%"
              language={selected ? editorLang(selected.language) : "python"}
              value={code}
              onChange={val => setCode(val || "")}
              theme="vs-dark"
              onMount={(editor) => { editorRef.current = editor; }}
              options={{
                automaticLayout: true,
                minimap: { enabled: false },
                fontSize: 14,
                wordWrap: "on",
                scrollBeyondLastLine: false,
                lineNumbers: "on",
                renderLineHighlight: "line",
                fontFamily: "JetBrains Mono, Fira Code, monospace",
              }}
            />
          </div>
        </div>

        {/* Output Panel */}
        <div className="output-panel">
          <div className="output-header">
            <span>Output</span>
            {submitPassed !== null && (
              <span className={`result-badge ${submitPassed ? "pass" : "fail"}`}>
                {submitPassed ? "✓ Passed" : "✗ Failed"} — {submitSummary}
              </span>
            )}
          </div>
          <div className="output-body">
            {!selected && <span className="output-placeholder">Load a problem and click Run to see output.</span>}
            {output && <pre className="output-text">{output}</pre>}
            {outputError && <pre className="output-error">{outputError}</pre>}

            {/* Test results - Replit style */}
            {submitResults.length > 0 && (
              <div className="test-results">
                <div className="test-results-title">Test Results</div>
                {submitResults.map((r, i) => (
                  <div key={i} className={`test-row ${r.status}`}>
                    <div className="test-row-header">
                      <span className="test-icon">{r.status === "pass" ? "✓" : "✗"}</span>
                      <span className="test-name">{r.test}</span>
                    </div>
                    {r.status === "fail" && (
                      <div className="test-vectors">
                        {r.input !== undefined && <div className="test-vector"><span className="vec-label">Input:</span><span className="vec-value">{JSON.stringify(r.input)}</span></div>}
                        <div className="test-vector"><span className="vec-label">Expected:</span><span className="vec-value vec-expected">{JSON.stringify(r.expected)}</span></div>
                        <div className="test-vector"><span className="vec-label">Got:</span><span className="vec-value vec-got">{JSON.stringify(r.got)}</span></div>
                      </div>
                    )}
                    {r.status === "error" && (
                      <div className="test-vectors">
                        <div className="test-vector"><span className="vec-label">Error:</span><span className="vec-value vec-got">{r.message}</span></div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
