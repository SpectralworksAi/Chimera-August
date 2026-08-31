from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from core.app.main import app


client = TestClient(app)


VALID_PION = {
    "protocol": "CPS/1.0 PION",
    "header": {
        "iteration": 1,
        "source_engine": "CHIMERA",
        "execution_mode": "CCCC",
    },
    "state": {
        "current_objective": "Preserve useful continuity",
        "active_uncertainty": "Whether the proposed change improves continuity",
        "next_executable_step": "Run controlled A/B/C test",
        "held_contradictions": "None",
        "implementation_status": "Ready for validation",
    },
    "payload": {"guardian": "on", "evidence_level": "test"},
}


def test_generate_rejects_invalid_pion():
    response = client.post(
        "/generate",
        json={"prompt": "Proceed", "vesicle": {"id": "v1", "payload": {}}},
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error"] == "invalid_pion_state"


def test_generate_sends_validated_pion_to_openai():
    output = Mock(output_text="grounded response")

    with patch("core.app.main.OpenAI") as openai_cls:
        openai_cls.return_value.responses.create.return_value = output

        response = client.post(
            "/generate",
            json={
                "prompt": "What is the next step?",
                "vesicle": {"id": "v1", "payload": VALID_PION},
            },
        )

    assert response.status_code == 200
    assert response.json()["output"] == "grounded response"
    call = openai_cls.return_value.responses.create.call_args.kwargs
    assert "VALIDATED_CHIMERA_PION_STATE:" in call["input"]
    assert "Preserve useful continuity" in call["input"]
    assert "What is the next step?" in call["input"]
