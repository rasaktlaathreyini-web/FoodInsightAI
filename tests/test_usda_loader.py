
import pandas as pd
import pytest

from src.ingest.usda_loader import load_usda_csv, search_foods


def test_load_usda_csv_normalizes_columns_and_removes_empty_rows(tmp_path):
    csv_file = tmp_path / "food.csv"

    csv_file.write_text(
        "Description,Food Category\n"
        "Apple, Fruit\n"
        ",\n"
        "Banana, Fruit\n",
        encoding="utf-8",
    )

    result = load_usda_csv(csv_file)

    assert list(result.columns) == ["description", "food_category"]
    assert len(result) == 2
    assert result["description"].tolist() == ["Apple", "Banana"]


def test_load_usda_csv_missing_file():
    with pytest.raises(FileNotFoundError):
        load_usda_csv("missing_usda_file.csv")


def test_load_usda_csv_empty_file(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_usda_csv(csv_file)


def test_search_foods_is_case_insensitive():
    foods = pd.DataFrame(
        {
            "description": [
                "Raw Apple",
                "Banana",
                "Apple Juice",
            ]
        }
    )

    result = search_foods(foods, "apple")

    assert len(result) == 2
    assert result["description"].tolist() == [
        "Raw Apple",
        "Apple Juice",
    ]


def test_search_foods_rejects_blank_query():
    foods = pd.DataFrame({"description": ["Apple"]})

    with pytest.raises(ValueError, match="non-empty"):
        search_foods(foods, "   ")


def test_search_foods_respects_limit():
    foods = pd.DataFrame(
        {
            "description": [
                "Apple",
                "Apple Juice",
                "Apple Pie",
            ]
        }
    )

    result = search_foods(foods, "apple", limit=2)

    assert len(result) == 2
