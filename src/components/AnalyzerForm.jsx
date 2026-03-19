import { fieldGroups } from "../constants";

function AnalyzerForm({ form, isAnalyzing, onChange, onSubmit }) {
  return (
    <form className="form-card" onSubmit={onSubmit}>
      {fieldGroups.map((group) => (
        <label className="field" key={group.name}>
          <span>{group.label}</span>
          <select name={group.name} value={form[group.name]} onChange={onChange}>
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
        <input type="checkbox" name="brutal_mode" checked={form.brutal_mode} onChange={onChange} />
      </label>

      <button className="analyze-button" type="submit" disabled={isAnalyzing}>
        {isAnalyzing ? "Analyzing your leverage..." : "Analyze"}
      </button>
    </form>
  );
}

export default AnalyzerForm;
