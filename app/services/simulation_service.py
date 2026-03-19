from app.models import RiskLevel
from app.schemas import SimulationRequest, SimulationResponse


def simulate_manager_response(payload: SimulationRequest, score: int) -> SimulationResponse:
    if score < 30:
        manager_response = (
            "I understand your request, but given the current dependency on your role, we will need you to complete the full notice period."
        )
        your_reply = (
            "Understood. I will focus on closing the gaps first and revisit the discussion once I have a stronger transition plan."
        )
        risk_level = RiskLevel.high
    elif score < 60:
        manager_response = (
            "We can discuss a partial reduction, but I need a clear handover plan before I can commit to anything shorter."
        )
        your_reply = (
            "That works. I will share a transition plan with milestones so we can agree on an earlier release date this week."
        )
        risk_level = RiskLevel.medium
    else:
        manager_response = (
            "If you can ensure a smooth handover and document the transition, I am open to discussing an earlier release."
        )
        your_reply = (
            "Thank you. I will send a handover plan today and propose a practical release timeline for your approval."
        )
        risk_level = RiskLevel.low

    if payload.manager_type == "toxic" and risk_level != RiskLevel.high:
        risk_level = RiskLevel.medium
        manager_response = (
            "I will review it, but do not assume anything changes until HR and leadership approve the transition."
        )
        your_reply = (
            "Understood. I will send the plan in writing and keep the request focused on a workable release timeline."
        )

    if payload.brutal_mode and risk_level == RiskLevel.high:
        manager_response = (
            "Right now there is no realistic path to an early release. The team needs you, and we will hold you to the full notice period."
        )
        your_reply = (
            "I understand. I will strengthen the handover case first and return with a more realistic proposal."
        )

    return SimulationResponse(
        manager_response=manager_response,
        your_reply=your_reply,
        risk_level=risk_level,
    )
