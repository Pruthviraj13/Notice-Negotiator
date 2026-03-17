import { useState } from "react";

const BASE_URL = import.meta.env.VITE_API_URL || "https://notice-negotiator.onrender.com";

const initialForm = {
  company_type: "service",
  notice_period: "30",
  offer_in_hand: "no",
  buyout_allowed: "no",
  project_critical: "medium",
  manager_type: "neutral",
  brutal_mode: false
};

const fieldGroups = [
  {
    label: "Company type",
    name: "company_type",
    options: [
      { value: "service", label: "Service" },
      { value: "startup", label: "Startup" },
      { value: "product", label: "Product" }
    ]
  },
  {
    label: "Notice period",
    name: "notice_period",
    options: [
      { value: "30", label: "30 days" },
      { value: "60", label: "60 days" },
      { value: "90", label: "90 days" }
    ]
  },
  {
    label: "Offer in hand",
    name: "offer_in_hand",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" }
    ]
  },
  {
    label: "Buyout allowed",
    name: "buyout_allowed",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" }
    ]
  },
  {
    label: "Project criticality",
    name: "project_critical",
    options: [
      { value: "low", label: "Low" },
      { value: "medium", label: "Medium" },
      { value: "high", label: "High" }
    ]
  },
  {
    label: "Manager type",
    name: "manager_type",
    options: [
      { value: "supportive", label: "Supportive" },
      { value: "neutral", label: "Neutral" },
      { value: "toxic", label: "Toxic" }
    ]
  }
];

const feedbackOptions = [
  { label: "Yes", value: "success" },
  { label: "Partial", value: "partial" },
  { label: "No", value: "failed" }
];

const strategyGroups = [
  { key: "safe", label: "Safe" },
  { key: "balanced", label: "Balanced" },
  { key: "aggressive", label: "Aggressive" }
];

function buildAnalyzePayload(form) {
  return {
    company_type: form.company_type,
    notice_period: Number(form.notice_period),
    offer_in_hand: form.offer_in_hand === "yes",
    buyout_allowed: form.buyout_allowed === "yes",
    project_critical: form.project_critical,
    manager_type: form.manager_type,
    brutal_mode: form.brutal_mode
  };
}

function buildScriptPayload(form, scriptMode) {
  return {
    ...buildAnalyzePayload(form),
    mode: scriptMode
  };
}

async function readError(response, fallbackMessage) {
  try {
    const data = await response.json();
    return data.detail || fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [script, setScript] = useState("");
  const [scriptMode, setScriptMode] = useState("balanced");
  const [feedbackStatus, setFeedbackStatus] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGeneratingScript, setIsGeneratingScript] = useState(false);
  const [isSendingFeedback, setIsSendingFeedback] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value, type, checked } = event.target;
    setForm((currentForm) => ({
      ...currentForm,
      [name]: type === "checkbox" ? checked : value
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsAnalyzing(true);
    setError("");
    setFeedbackStatus("");

    try {
      const response = await fetch(`${BASE_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(buildAnalyzePayload(form))
      });

      if (!response.ok) {
        throw new Error(await readError(response, "The analysis request failed."));
      }

      const data = await response.json();
      setResult(data);
    } catch (submissionError) {
      setError(submissionError.message);
    } finally {
      setIsAnalyzing(false);
    }
  }

  async function handleGenerateScript() {
    setIsGeneratingScript(true);
    setError("");

    try {
      const response = await fetch(`${BASE_URL}/generate-script`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(buildScriptPayload(form, scriptMode))
      });

      if (!response.ok) {
        throw new Error(await readError(response, "Script generation failed."));
      }

      const data = await response.json();
      setScript(data.script);
    } catch (scriptError) {
      setError(scriptError.message);
    } finally {
      setIsGeneratingScript(false);
    }
  }

  async function handleFeedback(outcome) {
    if (!result?.scenario_id) {
      return;
    }

    setIsSendingFeedback(true);
    setError("");

    try {
      const response = await fetch(`${BASE_URL}/feedback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          scenario_id: result.scenario_id,
          outcome
        })
      });

      if (!response.ok) {
        throw new Error(await readError(response, "Feedback could not be saved."));
      }

      setFeedbackStatus("Feedback saved.");
    } catch (feedbackError) {
      setError(feedbackError.message);
    } finally {
      setIsSendingFeedback(false);
    }
  }

  const scoreTone = result?.probability?.toLowerCase() ?? "idle";

  return (
    <div className="page-shell">
      <main className="layout">
        <section className="intro">
          <p className="eyebrow">Notice Negotiator</p>
          <h1>Find the strongest exit plan before you resign.</h1>
          <p className="intro-copy">
            Fill in the company situation and get a clear score, action plan, and
            negotiation message.
          </p>
        </section>

        <section className="workspace">
          <div className="left-column">
            <form className="form-card" onSubmit={handleSubmit}>
              {fieldGroups.map((group) => (
                <label className="field" key={group.name}>
                  <span>{group.label}</span>
                  <select
                    name={group.name}
                    value={form[group.name]}
                    onChange={handleChange}
                  >
                    {group.options.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </label>
              ))}

              <label className="toggle-card">
                <div>
                  <p className="toggle-title">Brutal mode</p>
                  <p className="toggle-copy">More direct and realistic output.</p>
                </div>
                <input
                  type="checkbox"
                  name="brutal_mode"
                  checked={form.brutal_mode}
                  onChange={handleChange}
                />
              </label>

              <button className="analyze-button" type="submit" disabled={isAnalyzing}>
                {isAnalyzing ? "Analyzing..." : "Analyze"}
              </button>
            </form>

            <section className="script-panel">
              <div className="script-header">
                <div>
                  <p className="mini-label">Negotiation script</p>
                  <p className="script-help">Choose a mode, then generate a ready-to-send message.</p>
                </div>
              </div>

              <div className="mode-picker">
                {strategyGroups.map((group) => (
                  <button
                    key={group.key}
                    type="button"
                    className={`mode-button ${scriptMode === group.key ? "is-active" : ""}`}
                    onClick={() => setScriptMode(group.key)}
                  >
                    {group.label}
                  </button>
                ))}
              </div>

              <button
                className="secondary-button standalone-button"
                type="button"
                onClick={handleGenerateScript}
                disabled={isGeneratingScript}
              >
                {isGeneratingScript ? `Generating ${scriptMode} script...` : `Generate ${scriptMode} script`}
              </button>

              {error ? <p className="error-text compact-error">{error}</p> : null}

              {script ? (
                <p className="script-card">{script}</p>
              ) : (
                <div className="script-placeholder">
                  <p>
                    The script will appear here after generation. Use `Safe` for a softer ask,
                    `Balanced` for a practical ask, and `Aggressive` for a direct time-bound ask.
                  </p>
                </div>
              )}
            </section>
          </div>

          <aside className={`result-card tone-${scoreTone}`}>
            {result ? (
              <>
                <p className="mini-label">Result</p>
                <div className="score-line">
                  <div>
                    <p className="score">{result.score}</p>
                    <p className="score-caption">Score out of 100</p>
                  </div>
                  <div className="probability-pill">{result.probability}</div>
                </div>

                <div className="summary-grid">
                  <div className="summary-item">
                    <p className="mini-label">Estimated reduction</p>
                    <p>{result.estimated_reduction}</p>
                  </div>
                  <div className="summary-item">
                    <p className="mini-label">Next action</p>
                    <p>{result.next_action}</p>
                  </div>
                </div>

                <div className="content-block">
                  <p className="mini-label">Reasoning</p>
                  <ul>
                    {result.reasoning.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="content-block">
                  <p className="mini-label">Recommended plan</p>
                  {strategyGroups.map((group) => (
                    <div className="strategy-group" key={group.key}>
                      <p className="strategy-title">{group.label}</p>
                      <ul>
                        {result.strategies[group.key].map((strategy) => (
                          <li key={`${group.key}-${strategy}`}>{strategy}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>

                <div className="content-block feedback-block">
                  <p className="mini-label">Did this work?</p>
                  <div className="feedback-actions">
                    {feedbackOptions.map((option) => (
                      <button
                        key={option.value}
                        className="feedback-button"
                        type="button"
                        onClick={() => handleFeedback(option.value)}
                        disabled={isSendingFeedback}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>
                  {feedbackStatus ? <p className="feedback-status">{feedbackStatus}</p> : null}
                </div>
              </>
            ) : (
              <div className="empty-state">
                <p className="mini-label">Result</p>
                <h2>Your strategy will appear here.</h2>
                <p>
                  Keep the inputs simple. The app will turn them into a practical
                  notice-period plan.
                </p>
              </div>
            )}
          </aside>
        </section>
      </main>
    </div>
  );
}

export default App;
