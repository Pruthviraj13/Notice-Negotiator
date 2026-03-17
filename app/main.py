from fastapi import FastAPI, HTTPException

from app.database import init_db, save_feedback, save_scenario
from app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    FeedbackRequest,
    FeedbackResponse,
    ScriptRequest,
    ScriptResponse,
)
from app.services.analysis_service import build_analysis_response, calculate_score
from app.services.script_service import generate_negotiation_script

app = FastAPI(title="Notice Negotiator API")


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_notice(payload: AnalyzeRequest) -> AnalyzeResponse:
    score = calculate_score(payload)
    scenario_id = save_scenario(payload.model_dump(mode="json"), score)
    return build_analysis_response(payload, scenario_id)


@app.post("/generate-script", response_model=ScriptResponse)
def generate_script(payload: ScriptRequest) -> ScriptResponse:
    score = calculate_score(payload)
    try:
        script = generate_negotiation_script(payload, score, payload.mode.value)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ScriptResponse(script=script)


@app.post("/feedback", response_model=FeedbackResponse)
def create_feedback(payload: FeedbackRequest) -> FeedbackResponse:
    feedback_id = save_feedback(payload.scenario_id, payload.outcome.value)
    return FeedbackResponse(feedback_id=feedback_id, status="saved")
