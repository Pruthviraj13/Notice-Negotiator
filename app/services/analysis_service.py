from app.schemas import AnalyzeRequest, AnalyzeResponse

BASE_SCORE = 30


def calculate_score(payload: AnalyzeRequest) -> int:
    score = BASE_SCORE

    if payload.offer_in_hand:
        score += 35
    else:
        score -= 25

    if payload.buyout_allowed:
        score += 20

    if payload.company_type == "startup":
        score += 15
    elif payload.company_type == "product":
        score += 5

    if payload.manager_type == "supportive":
        score += 10
    elif payload.manager_type == "toxic":
        score -= 20

    if payload.project_critical == "high":
        score -= 30
    elif payload.project_critical == "medium":
        score -= 10

    if payload.notice_period == 60:
        score -= 5
    elif payload.notice_period == 90:
        score -= 10

    return max(0, min(100, score))


def map_probability(score: int) -> str:
    if score < 30:
        return "Low"
    if score < 60:
        return "Medium"
    return "High"


def estimate_reduction(score: int) -> str:
    if score < 30:
        return "0-10 days"
    if score < 60:
        return "10-30 days"
    return "30-60 days"


def tone(normal: str, brutal: str, brutal_mode: bool) -> str:
    return brutal if brutal_mode else normal


def get_next_action(payload: AnalyzeRequest, score: int) -> str:
    if not payload.offer_in_hand:
        return tone(
            "Get an offer within 1-2 weeks before negotiating.",
            "Get an offer first. Right now you do not have enough leverage.",
            payload.brutal_mode,
        )
    if score < 30:
        return tone(
            "Do NOT resign yet. Improve leverage.",
            "Do not resign now. You will likely be forced through full notice.",
            payload.brutal_mode,
        )
    if score < 60:
        return tone(
            "Schedule manager discussion this week.",
            "Talk to your manager this week, but do not expect an easy release.",
            payload.brutal_mode,
        )
    return tone(
        "Start negotiation immediately with a clear exit plan.",
        "Start the negotiation now while your leverage is still strong.",
        payload.brutal_mode,
    )


def get_final_decision(payload: AnalyzeRequest, score: int) -> str:
    if score < 30:
        return tone(
            "Do NOT resign now. Your leverage is too weak.",
            "Do NOT resign now. Your leverage is too weak.",
            payload.brutal_mode,
        )
    if score <= 60:
        return tone(
            "Proceed only after securing an offer.",
            "Proceed only after securing an offer.",
            payload.brutal_mode,
        )
    return tone(
        "You are in a strong position. Start negotiation this week.",
        "You are in a strong position. Start negotiation this week.",
        payload.brutal_mode,
    )


def get_confidence(payload: AnalyzeRequest, score: int) -> int:
    confidence = score

    if not payload.offer_in_hand:
        confidence -= 15
    if payload.project_critical == "high":
        confidence -= 10
    elif payload.project_critical == "medium":
        confidence -= 5
    if payload.manager_type == "supportive":
        confidence += 10
    elif payload.manager_type == "toxic":
        confidence -= 5

    return max(0, min(100, confidence))


def build_reasoning(payload: AnalyzeRequest) -> list[str]:
    reasons: list[str] = []

    if payload.offer_in_hand:
        reasons.append(
            tone(
                "You have leverage due to an offer.",
                "An external offer is the main reason this negotiation has any strength.",
                payload.brutal_mode,
            )
        )
    else:
        reasons.append(
            tone(
                "No offer reduces negotiation power.",
                "No offer means the company has little incentive to release you early.",
                payload.brutal_mode,
            )
        )

    if payload.project_critical == "high":
        reasons.append(
            tone(
                "High project dependency reduces flexibility.",
                "High project dependency makes an early release much harder to win.",
                payload.brutal_mode,
            )
        )

    if payload.manager_type == "supportive":
        reasons.append(
            tone(
                "Supportive manager increases chances.",
                "A supportive manager improves your odds, but it does not override weak leverage.",
                payload.brutal_mode,
            )
        )
    elif payload.manager_type == "toxic" and payload.brutal_mode:
        reasons.append("A toxic manager can stall this even if your overall case looks decent.")

    if payload.brutal_mode and not payload.buyout_allowed and payload.project_critical == "high":
        reasons.append("Your leverage is weak due to no buyout and high dependency.")

    return reasons


def build_strategies(payload: AnalyzeRequest, score: int, brutal_mode: bool) -> dict[str, list[str]]:
    safe = [
        tone(
            "Avoid risk and strengthen your position before resigning.",
            "If you move now, you will probably serve the full notice period.",
            brutal_mode,
        ),
        tone(
            "Secure a written offer before opening negotiation.",
            "Without a written offer, you have almost no leverage.",
            brutal_mode,
        ),
    ]
    balanced = [
        tone(
            "Talk to your manager with a structured transition plan.",
            "Talk to your manager only with a concrete transition plan, or the discussion will stall.",
            brutal_mode,
        ),
        tone(
            "Plan a structured negotiation instead of a rushed ask.",
            "If your ask is vague, they will default to the full notice period.",
            brutal_mode,
        ),
    ]
    aggressive = [
        tone(
            "Use leverage such as offer urgency and buyout to push faster release.",
            "Use offer urgency, buyout, and hard dates if you want movement.",
            brutal_mode,
        ),
        tone(
            "Escalate to HR if the discussion does not move.",
            "If the manager stalls, go to HR and force a timeline discussion.",
            brutal_mode,
        ),
    ]

    if score < 30:
        safe.append(tone(
            "Wait and improve leverage before negotiating.",
            "If you proceed now, you will likely serve full notice.",
            brutal_mode,
        ))
        balanced.append(tone(
            "Do not pressure the company yet; reduce risk first.",
            "Pushing now without leverage is more likely to fail than help.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Aggressive tactics are too risky in this position.",
            "Aggressive tactics here will likely backfire.",
            brutal_mode,
        ))
    elif score < 60:
        safe.append(tone(
            "Keep a backup plan in case the company resists.",
            "There is a serious chance they refuse, so prepare for resistance.",
            brutal_mode,
        ))
        balanced.append(tone(
            "Set up a manager conversation this week and align on handover.",
            "Have the manager conversation now and expect negotiation, not approval.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Push timelines only after you test the manager response.",
            "Do not escalate blindly. First confirm how much pushback you are dealing with.",
            brutal_mode,
        ))
    else:
        safe.append(tone(
            "Protect goodwill while documenting handover carefully.",
            "Even strong leverage can collapse if your handover story looks weak.",
            brutal_mode,
        ))
        balanced.append(tone(
            "Negotiate with a clear ask and a credible transition plan.",
            "Ask directly for the shorter timeline now while your case is strong.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Use hard leverage and deadlines to accelerate release.",
            "Push hard now, because this is the best position you are likely to get.",
            brutal_mode,
        ))

    if not payload.offer_in_hand:
        safe.append(tone(
            "Focus on securing an offer before making a move.",
            "Without an offer, this negotiation starts from a weak position.",
            brutal_mode,
        ))
        balanced.append(tone(
            "Keep discussions quiet until the external role is confirmed.",
            "Do not expose your plans too early when you still have nothing concrete.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Do not use pressure tactics without a confirmed fallback option.",
            "Aggressive tactics without an offer will make you look exposed, not strong.",
            brutal_mode,
        ))

    if payload.manager_type == "supportive":
        balanced.append(tone(
            "Use your manager to shape a practical release path.",
            "Use the supportive manager now before that advantage disappears.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Ask your manager to support faster release with HR.",
            "Use your manager to push HR instead of negotiating alone.",
            brutal_mode,
        ))
    elif payload.manager_type == "toxic":
        safe.append(tone(
            "Keep communication documented and low-risk.",
            "A toxic manager can weaponize sloppy communication, so document everything.",
            brutal_mode,
        ))
        balanced.append(tone(
            "Keep discussions formal and tightly scoped.",
            "With a toxic manager, one loose conversation can derail the whole process.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Bypass unproductive discussion if needed.",
            "If the manager blocks progress, stop waiting and go to HR.",
            brutal_mode,
        ))

    if payload.project_critical == "high":
        safe.append(tone(
            "Prepare a handover plan before making hard asks.",
            "High dependency already gives them a strong reason to keep you longer.",
            brutal_mode,
        ))
        balanced.append(tone(
            "Use milestone-based transition to reduce resistance.",
            "If you cannot break the work into milestones, your ask will not look credible.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Counter project pushback with a transfer timeline.",
            "If they cite project risk, answer with dates and owners immediately.",
            brutal_mode,
        ))

    if payload.buyout_allowed:
        balanced.append(tone(
            "Keep buyout available as negotiation leverage.",
            "Buyout is one of the few hard levers you can use if discussion stalls.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Use buyout if they refuse to move timelines.",
            "If they do not move, use buyout instead of waiting for goodwill.",
            brutal_mode,
        ))
    else:
        safe.append(tone(
            "Plan for transition because buyout is not available.",
            "No buyout means you cannot force speed through money.",
            brutal_mode,
        ))

    if payload.notice_period == 90:
        safe.append(tone(
            "Expect a slower path and negotiate in phases.",
            "A 90-day notice period is hard to cut fast, so assume resistance.",
            brutal_mode,
        ))
        balanced.append(tone(
            "Negotiate milestone-based reduction instead of full waiver first.",
            "A full waiver ask on 90 days is often unrealistic, so negotiate in stages.",
            brutal_mode,
        ))
        aggressive.append(tone(
            "Push for partial waivers with fixed dates if full waiver is rejected.",
            "If full waiver fails, force the conversation into partial reductions with dates.",
            brutal_mode,
        ))

    return {
        "safe": safe,
        "balanced": balanced,
        "aggressive": aggressive,
    }


def build_analysis_response(payload: AnalyzeRequest, scenario_id: str) -> AnalyzeResponse:
    score = calculate_score(payload)
    return AnalyzeResponse(
        scenario_id=scenario_id,
        score=score,
        probability=map_probability(score),
        estimated_reduction=estimate_reduction(score),
        next_action=get_next_action(payload, score),
        final_decision=get_final_decision(payload, score),
        confidence=get_confidence(payload, score),
        reasoning=build_reasoning(payload),
        strategies=build_strategies(payload, score, payload.brutal_mode),
    )
