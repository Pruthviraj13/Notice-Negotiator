import { strategyGroups } from "../constants";

function ScriptWorkspace({
  copyStatus,
  error,
  isGeneratingScript,
  isSimulating,
  onCopy,
  onGenerate,
  onModeChange,
  onSimulate,
  script,
  scriptMode,
  simulation,
}) {
  return (
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
            onClick={() => onModeChange(group.key)}
          >
            {group.label}
          </button>
        ))}
      </div>

      <div className="script-actions-grid">
        <button className="secondary-button standalone-button" type="button" onClick={onGenerate} disabled={isGeneratingScript}>
          {isGeneratingScript ? "Generating negotiation script..." : `Generate ${scriptMode} script`}
        </button>

        <button className="secondary-button standalone-button" type="button" onClick={onSimulate} disabled={isSimulating}>
          {isSimulating ? "Simulating manager response..." : "Simulate Manager Response"}
        </button>
      </div>

      {error ? <p className="error-text compact-error">{error}</p> : null}

      {script ? (
        <div className="script-output-card">
          <div className="script-toolbar">
            <p className="mini-label">Ready to send</p>
            <button className="copy-button" type="button" onClick={onCopy}>
              {copyStatus || "Copy to Clipboard"}
            </button>
          </div>
          <p className="script-card">{script}</p>
        </div>
      ) : (
        <div className="script-placeholder">
          <p>
            The script will appear here after generation. Use Safe for a softer ask,
            Balanced for a practical ask, and Aggressive for a direct time-bound ask.
          </p>
        </div>
      )}

      {simulation ? (
        <div className="simulation-card">
          <p className="mini-label">Simulation</p>
          <div className="simulation-risk">Risk level: {simulation.risk_level}</div>
          <div className="simulation-block">
            <p className="simulation-title">Manager response</p>
            <p>{simulation.manager_response}</p>
          </div>
          <div className="simulation-block">
            <p className="simulation-title">Your reply</p>
            <p>{simulation.your_reply}</p>
          </div>
        </div>
      ) : null}
    </section>
  );
}

export default ScriptWorkspace;
