from pydantic import BaseModel

from app.models import (
    CompanyType,
    FeedbackOutcome,
    ManagerType,
    NoticePeriod,
    ProjectCriticality,
    RiskLevel,
    ScriptMode,
)


class AnalyzeRequest(BaseModel):
    company_type: CompanyType
    notice_period: NoticePeriod
    offer_in_hand: bool
    buyout_allowed: bool
    project_critical: ProjectCriticality
    manager_type: ManagerType
    brutal_mode: bool = False


class AnalyzeResponse(BaseModel):
    scenario_id: str
    score: int
    probability: str
    estimated_reduction: str
    next_action: str
    final_decision: str
    confidence: int
    reasoning: list[str]
    strategies: dict[str, list[str]]


class ScriptRequest(AnalyzeRequest):
    mode: ScriptMode = ScriptMode.balanced


class ScriptResponse(BaseModel):
    script: str


class SimulationRequest(AnalyzeRequest):
    mode: ScriptMode = ScriptMode.balanced


class SimulationResponse(BaseModel):
    manager_response: str
    your_reply: str
    risk_level: RiskLevel


class FeedbackRequest(BaseModel):
    scenario_id: str
    outcome: FeedbackOutcome


class FeedbackResponse(BaseModel):
    feedback_id: str
    status: str
