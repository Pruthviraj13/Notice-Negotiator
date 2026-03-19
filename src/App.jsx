import { useState } from "react";

import { analyzeScenario, generateScript, simulateResponse } from "./api";
import HeroSection from "./components/HeroSection";
import AnalyzerForm from "./components/AnalyzerForm";
import ScriptWorkspace from "./components/ScriptWorkspace";
import ResultPanel from "./components/ResultPanel";
import { initialForm } from "./constants";

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [script, setScript] = useState("");
  const [scriptMode, setScriptMode] = useState("balanced");
  const [simulation, setSimulation] = useState(null);
  const [copyStatus, setCopyStatus] = useState("");
  const [helpfulVote, setHelpfulVote] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGeneratingScript, setIsGeneratingScript] = useState(false);
  const [isSimulating, setIsSimulating] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value, type, checked } = event.target;
    setForm((currentForm) => ({
      ...currentForm,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsAnalyzing(true);
    setError("");
    setHelpfulVote("");

    try {
      const data = await analyzeScenario(form);
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
    setCopyStatus("");

    try {
      const data = await generateScript(form, scriptMode);
      setScript(data.script);
    } catch (scriptError) {
      setError(scriptError.message);
    } finally {
      setIsGeneratingScript(false);
    }
  }

  async function handleSimulate() {
    setIsSimulating(true);
    setError("");

    try {
      const data = await simulateResponse(form, scriptMode);
      setSimulation(data);
    } catch (simulationError) {
      setError(simulationError.message);
    } finally {
      setIsSimulating(false);
    }
  }

  async function handleCopy() {
    if (!script) {
      return;
    }

    await navigator.clipboard.writeText(script);
    setCopyStatus("Copied!");
    window.setTimeout(() => setCopyStatus(""), 1800);
  }

  return (
    <div className="page-shell">
      <main className="layout">
        <HeroSection />

        <section className="workspace">
          <div className="left-column">
            <AnalyzerForm form={form} isAnalyzing={isAnalyzing} onChange={handleChange} onSubmit={handleSubmit} />
            <ScriptWorkspace
              copyStatus={copyStatus}
              error={error}
              isGeneratingScript={isGeneratingScript}
              isSimulating={isSimulating}
              onCopy={handleCopy}
              onGenerate={handleGenerateScript}
              onModeChange={setScriptMode}
              onSimulate={handleSimulate}
              script={script}
              scriptMode={scriptMode}
              simulation={simulation}
            />
          </div>

          <ResultPanel helpfulVote={helpfulVote} onHelpfulVote={setHelpfulVote} result={result} />
        </section>
      </main>
    </div>
  );
}

export default App;
