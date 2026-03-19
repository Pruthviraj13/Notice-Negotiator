import { strategyGroups } from "../constants";

function ResultPanel({ helpfulVote, onHelpfulVote, result }) {
  const scoreTone = result?.probability?.toLowerCase() ?? "idle";

  return (
    <aside className={`result-card tone-${scoreTone}`}>
      {result ? (
        <>
          <div className="decision-card">
            <p className="mini-label">Final decision</p>
            <h2>{result.final_decision}</h2>
            <p className="decision-confidence">Confidence: {result.confidence}/100</p>
          </div>

          <p className="mini-label result-label">Result</p>
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

          <div className="content-block helpful-block">
            <p className="mini-label">Did this help?</p>
            <div className="helpful-actions">
              <button
                className={`helpful-button ${helpfulVote === "yes" ? "is-selected" : ""}`}
                type="button"
                onClick={() => onHelpfulVote("yes")}
              >
                ?? Yes
              </button>
              <button
                className={`helpful-button ${helpfulVote === "no" ? "is-selected" : ""}`}
                type="button"
                onClick={() => onHelpfulVote("no")}
              >
                ?? No
              </button>
            </div>
          </div>
        </>
      ) : (
        <div className="empty-state">
          <p className="mini-label">Result</p>
          <h2>Your strategy will appear here.</h2>
          <p>Keep the inputs simple. The app will turn them into a practical notice-period plan.</p>
        </div>
      )}
    </aside>
  );
}

export default ResultPanel;
