import { BASE_URL } from "./config";

function buildAnalyzePayload(form) {
  return {
    company_type: form.company_type,
    notice_period: Number(form.notice_period),
    offer_in_hand: form.offer_in_hand === "yes",
    buyout_allowed: form.buyout_allowed === "yes",
    project_critical: form.project_critical,
    manager_type: form.manager_type,
    brutal_mode: form.brutal_mode,
  };
}

function buildScriptPayload(form, mode) {
  return {
    ...buildAnalyzePayload(form),
    mode,
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

export async function analyzeScenario(form) {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(buildAnalyzePayload(form)),
  });

  if (!response.ok) {
    throw new Error(await readError(response, "The analysis request failed."));
  }

  return response.json();
}

export async function generateScript(form, mode) {
  const response = await fetch(`${BASE_URL}/generate-script`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(buildScriptPayload(form, mode)),
  });

  if (!response.ok) {
    throw new Error(await readError(response, "Script generation failed."));
  }

  return response.json();
}

export async function simulateResponse(form, mode) {
  const response = await fetch(`${BASE_URL}/simulate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(buildScriptPayload(form, mode)),
  });

  if (!response.ok) {
    throw new Error(await readError(response, "Simulation failed."));
  }

  return response.json();
}
