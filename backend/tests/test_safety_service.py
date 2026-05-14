from app.services.safety_service import safety_service


def test_safety_service_flags_pii_without_returning_values() -> None:
    text = (
        "Contact me at person@example.com or +254712345678. "
        "My ID is 12345678 and I am near house no A12."
    )

    assessment = safety_service.assess_text(text)

    assert assessment.pii_detected is True
    assert assessment.flag_count == 4
    assert assessment.flag_summary == "email,phone_number,possible_id_number,address_hint"
    assert "person@example.com" not in assessment.flag_summary
    assert "+254712345678" not in assessment.flag_summary
