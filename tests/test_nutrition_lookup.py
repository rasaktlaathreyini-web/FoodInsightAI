import pandas as pd
import pytest

from src.ingest.nutrition_lookup import (
    _find_matching_foods,
    get_food_nutrition,
    search_nutrition,
)


def test_find_matching_foods_is_case_insensitive(tmp_path):
    create_test_data(tmp_path)

    result = _find_matching_foods(
        "HUMMUS",
        data_dir=tmp_path,
    )

    assert not result.empty
    assert result["description"].eq("Test Hummus").all()


def test_find_matching_foods_returns_empty_for_unknown_food(tmp_path):
    create_test_data(tmp_path)

    result = _find_matching_foods(
        "unknown_food_xyz",
        data_dir=tmp_path,
    )

    assert result.empty


def create_test_data(data_dir):
    """Create small USDA-like CSV files for testing."""

    foods = pd.DataFrame([
        {
            "fdc_id": 1,
            "data_type": "foundation_food",
            "description": "Test Hummus",
            "food_category_id": 1,
            "publication_date": "2026-01-01",
        }
    ])

    foods.to_csv(data_dir / "food.csv", index=False)

    measurements = pd.DataFrame([
        {"id": 1, "fdc_id": 1, "nutrient_id": 1008, "amount": 200.0},
        {"id": 2, "fdc_id": 1, "nutrient_id": 1003, "amount": 8.0},
        {"id": 3, "fdc_id": 1, "nutrient_id": 1004, "amount": 10.0},
        {"id": 4, "fdc_id": 1, "nutrient_id": 1005, "amount": 20.0},
        {"id": 5, "fdc_id": 1, "nutrient_id": 1258, "amount": 2.0},
    ])

    measurements.to_csv(
        data_dir / "food_nutrient.csv",
        index=False,
    )

    nutrients = pd.DataFrame([
        {"id": 1008, "name": "Energy", "unit_name": "KCAL"},
        {"id": 1003, "name": "Protein", "unit_name": "G"},
        {"id": 1004, "name": "Total lipid (fat)", "unit_name": "G"},
        {
            "id": 1005,
            "name": "Carbohydrate, by difference",
            "unit_name": "G",
        },
        {
            "id": 1258,
            "name": "Fatty acids, total saturated",
            "unit_name": "G",
        },
    ])

    nutrients.to_csv(data_dir / "nutrient.csv", index=False)


def test_returns_food_nutrition(tmp_path):
    create_test_data(tmp_path)

    result = get_food_nutrition("hummus", data_dir=tmp_path)

    assert result is not None
    assert result["food"] == "Test Hummus"
    assert result["nutrition"]["Protein"]["amount"] == 8.0
    assert result["nutrition"]["Calories"]["unit"] == "KCAL"


def test_returns_none_for_unknown_food(tmp_path):
    create_test_data(tmp_path)

    result = get_food_nutrition(
        "food_that_does_not_exist",
        data_dir=tmp_path,
    )

    assert result is None


def test_rejects_empty_query(tmp_path):
    with pytest.raises(ValueError):
        get_food_nutrition("", data_dir=tmp_path)

def test_search_nutrition_uses_custom_data_directory(tmp_path):
    create_test_data(tmp_path)

    result = search_nutrition("hummus", data_dir=tmp_path)

    assert not result.empty
    assert result["description"].eq("Test Hummus").all()


def test_search_nutrition_returns_empty_for_unknown_food(tmp_path):
    create_test_data(tmp_path)

    result = search_nutrition(
        "unknown_food_xyz",
        data_dir=tmp_path,
    )

    assert result.empty


def test_search_nutrition_rejects_empty_query(tmp_path):
    with pytest.raises(ValueError):
        search_nutrition("", data_dir=tmp_path)


def test_search_nutrition_rejects_invalid_limit(tmp_path):
    with pytest.raises(ValueError):
        search_nutrition("hummus", data_dir=tmp_path, limit=0)
def test_missing_nutrient_amount_is_not_reported_as_zero(tmp_path):
    create_test_data(tmp_path)

    # Read the test nutrition data.
    measurements = pd.read_csv(tmp_path / "food_nutrient.csv")

    # Simulate a missing protein measurement.
    measurements.loc[
        measurements["nutrient_id"] == 1003, "amount"
    ] = float("nan")

    measurements.to_csv(
        tmp_path / "food_nutrient.csv",
        index=False,
    )

    result = get_food_nutrition("hummus", data_dir=tmp_path)

    assert result is not None
    assert result["nutrition"]["Protein"]["amount"] is None