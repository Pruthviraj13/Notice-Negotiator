import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


EXPECTED = {
    "No offer plus service should be low": {
        "probability": "Low",
        "estimated_reduction": "0-10 days",
        "next_action": "Get an offer within 1-2 weeks before negotiating.",
        "final_decision": "Do NOT resign now. Your leverage is too weak.",
    },
    "Offer plus startup should be high": {
        "probability": "High",
        "estimated_reduction": "30-60 days",
        "next_action": "Start negotiation immediately with a clear exit plan.",
        "final_decision": "You are in a strong position. Start negotiation this week.",
    },
    "Product company with medium risk should be medium": {
        "probability": "Medium",
        "estimated_reduction": "10-30 days",
        "next_action": "Schedule manager discussion this week.",
        "final_decision": "Proceed only after securing an offer.",
    },
    "Startup without offer but supportive manager stays medium": {
        "probability": "Medium",
        "estimated_reduction": "10-30 days",
        "next_action": "Get an offer within 1-2 weeks before negotiating.",
        "final_decision": "Proceed only after securing an offer.",
    },
    "Service company with offer and high criticality stays medium": {
        "probability": "Medium",
        "estimated_reduction": "10-30 days",
        "next_action": "Schedule manager discussion this week.",
        "final_decision": "Proceed only after securing an offer.",
    },
}


def main() -> None:
    client = TestClient(app)
    cases = json.loads(Path("manual_test_cases.json").read_text())

    for case in cases:
        payload = {**case["payload"], "brutal_mode": False}
        response = client.post("/analyze", json=payload)
        response.raise_for_status()
        body = response.json()
        expected = EXPECTED[case["name"]]
        strategies = body["strategies"]
        status = (
            "PASS"
            if body["probability"] == expected["probability"]
            and body["estimated_reduction"] == expected["estimated_reduction"]
            and body["next_action"] == expected["next_action"]
            and body["final_decision"] == expected["final_decision"]
            and 0 <= body["confidence"] <= 100
            and len(body["reasoning"]) >= 1
            and bool(body["scenario_id"])
            and all(key in strategies for key in ("safe", "balanced", "aggressive"))
            and all(len(strategies[key]) >= 2 for key in ("safe", "balanced", "aggressive"))
            else "FAIL"
        )
        print(f"{status}: {case['name']}")
        print(f"  scenario_id={body['scenario_id']}")
        print(f"  score={body['score']} probability={body['probability']}")
        print(f"  estimated_reduction={body['estimated_reduction']}")
        print(f"  next_action={body['next_action']}")
        print(f"  final_decision={body['final_decision']}")
        print(f"  confidence={body['confidence']}")
        print(f"  brutal_mode={payload['brutal_mode']}")
        print(f"  reasoning={len(body['reasoning'])}")
        print(
            "  strategies="
            f"safe:{len(strategies['safe'])} "
            f"balanced:{len(strategies['balanced'])} "
            f"aggressive:{len(strategies['aggressive'])}"
        )
        if status != "PASS":
            raise SystemExit(1)


if __name__ == "__main__":
    main()
