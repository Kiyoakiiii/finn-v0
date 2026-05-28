from finn.safety import route_message


def test_medication_request_is_declined() -> None:
    decision = route_message("Should I take 10mg melatonin every night?")

    assert decision.allowed is False
    assert decision.category == "medication_request"
    assert "cannot recommend" in decision.message


def test_diagnosis_request_is_declined() -> None:
    decision = route_message("Can you diagnose my chest pain?")

    assert decision.allowed is False
    assert decision.category == "urgent_or_crisis"
    assert "emergency" in decision.message.lower()


def test_out_of_scope_request_is_declined() -> None:
    decision = route_message("What stock should I buy today?")

    assert decision.allowed is False
    assert decision.category == "out_of_scope"


def test_wellness_question_is_allowed() -> None:
    decision = route_message("How can I improve my sleep?")

    assert decision.allowed is True
    assert decision.category == "wellness_candidate"
