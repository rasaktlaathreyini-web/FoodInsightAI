from unittest.mock import patch

import pytest

from src.nutrition_assistant import answer_nutrition_question


def test_returns_not_found_message_for_unknown_food():
    with patch(
        "src.nutrition_assistant.get_food_nutrition",
        return_value=None,
    ):
        result = answer_nutrition_question("unknown food xyz")

    assert "couldn't find nutrition information" in result


def test_rejects_empty_query():
    with pytest.raises(ValueError):
        answer_nutrition_question("")


def test_sends_retrieved_nutrition_data_to_llm():
    nutrition_data = {
        "food": "Hummus, commercial",
        "fdc_id": 321358,
        "data_type": "foundation_food",
        "nutrition": {
            "Calories": {"amount": 229.0, "unit": "KCAL"},
            "Protein": {"amount": 7.35, "unit": "G"},
        },
    }

    with (
        patch(
            "src.nutrition_assistant.get_food_nutrition",
            return_value=nutrition_data,
        ),
        patch(
            "src.nutrition_assistant.ask_llm",
            return_value="Hummus contains 229 KCAL and 7.35 G protein.",
        ) as mock_llm,
    ):
        result = answer_nutrition_question("hummus")

    assert "229 KCAL" in result
    mock_llm.assert_called_once()

    prompt = mock_llm.call_args.args[0]
    assert "Hummus, commercial" in prompt
    assert "7.35" in prompt

def test_prompt_rejects_unsupported_nutrition_claims():
    nutrition_data = {
        "food": "Hummus, commercial",
        "fdc_id": 321358,
        "data_type": "foundation_food",
        "nutrition": {
            "Calories": {"amount": 229.0, "unit": "KCAL"},
        },
    }

    with (
        patch(
            "src.nutrition_assistant.get_food_nutrition",
            return_value=nutrition_data,
        ),
        patch(
            "src.nutrition_assistant.ask_llm",
            return_value="Hummus contains 229 KCAL.",
        ) as mock_llm,
    ):
        answer_nutrition_question("hummus")

    prompt = mock_llm.call_args.args[0].lower()
    assert "daily recommended intake percentages" in prompt
    assert "unsupported health claims" in prompt
