
from pathlib import Path

import pandas as pd

from src.ingest.usda_loader import load_usda_csv



DATA_DIR = Path("data/raw/foundation")

# USDA nutrient IDs
NUTRIENTS = {
    "calories": 1008,
    "protein": 1003,
    "fat": 1004,
    "carbohydrates": 1005,
    "saturated_fat": 1258,
}


def load_nutrition_data(data_dir=DATA_DIR):
    """Load and combine USDA food and nutrient datasets."""

    data_dir = Path(data_dir)

    foods = load_usda_csv(data_dir / "food.csv")
    measurements = load_usda_csv(data_dir / "food_nutrient.csv")
    nutrients = load_usda_csv(data_dir / "nutrient.csv")

    # Ensure identifiers use compatible data types.
    foods["fdc_id"] = pd.to_numeric(
        foods["fdc_id"], errors="coerce"
    )
    measurements["fdc_id"] = pd.to_numeric(
        measurements["fdc_id"], errors="coerce"
    )
    measurements["nutrient_id"] = pd.to_numeric(
        measurements["nutrient_id"], errors="coerce"
    )
    nutrients["id"] = pd.to_numeric(
        nutrients["id"], errors="coerce"
    )

    # Keep food records that have a valid identifier.
    foods = foods.dropna(subset=["fdc_id"]).copy()

    # Attach nutrient names and units to their measurements.
    measurements = measurements.merge(
        nutrients[["id", "name", "unit_name"]],
        left_on="nutrient_id",
        right_on="id",
        how="left",
    )

    # Attach food descriptions to the measurements.
    measurements = measurements.merge(
        foods[["fdc_id", "description", "data_type"]],
        on="fdc_id",
        how="inner",
    )

    return measurements


def _find_matching_foods(query, data_dir=DATA_DIR):
    """Load nutrition data and find foods matching a partial name."""

    data = load_nutrition_data(data_dir)

    matches = data[
        data["description"].str.contains(
            query.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ].copy()

    return matches


def search_nutrition(query, data_dir=DATA_DIR, limit=10):
    """Search foods and return available nutrient information."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query must be a non-empty string.")

    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("Limit must be a positive integer.")

    matches = _find_matching_foods(query, data_dir)

    if matches.empty:
        return pd.DataFrame(
            columns=[
                "fdc_id",
                "description",
                "data_type",
                "name",
                "amount",
                "unit_name",
            ]
        )

    # Prefer Foundation Foods when available.
    priority = {
        "foundation_food": 0,
        "sample_food": 1,
        "market_acquisition": 2,
        "agricultural_acquisition": 3,
        "sub_sample_food": 4,
    }

    matches["priority"] = (
        matches["data_type"].map(priority).fillna(99)
    )

    matches = matches.sort_values(
        ["priority", "description"]
    )

    # Limit the number of distinct foods, not nutrient rows.
    food_results = matches[
        ["fdc_id", "description", "data_type"]
    ].drop_duplicates("fdc_id").head(limit)

    return matches[
        matches["fdc_id"].isin(food_results["fdc_id"])
    ][
        [
            "fdc_id",
            "description",
            "data_type",
            "name",
            "amount",
            "unit_name",
        ]
    ].reset_index(drop=True)


def get_food_nutrition(query, data_dir=DATA_DIR):
    """Return a concise nutrition summary for the best food match."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query must be a non-empty string.")

    matches = _find_matching_foods(query, data_dir)

    if matches.empty:
        return None

    # Prefer the main Foundation Food record.
    priority = {
        "foundation_food": 0,
        "sample_food": 1,
        "market_acquisition": 2,
        "agricultural_acquisition": 3,
        "sub_sample_food": 4,
    }

    matches["priority"] = (
        matches["data_type"].map(priority).fillna(99)
    )

    matches = matches.sort_values(
        ["priority", "description"]
    )

    # Select one food record, not multiple related samples.
    food = matches.iloc[0]
    food_id = food["fdc_id"]

    food_data = matches[matches["fdc_id"] == food_id]

    # Define preferred nutrient names.
    nutrient_names = {
        "Calories": [
            "Energy (Atwater Specific Factors)",
            "Energy",
            "Energy (Atwater General Factors)",
        ],
        "Protein": ["Protein"],
        "Total fat": ["Total lipid (fat)", "Total fat (NLEA)"],
        "Carbohydrates": [
            "Carbohydrate, by difference",
            "Carbohydrate, by summation",
        ],
        "Saturated fat": ["Fatty acids, total saturated"],
    }

    summary = {
        "food": food["description"],
        "fdc_id": int(food_id),
        "data_type": food["data_type"],
        "nutrition": {},
    }


    # Choose the first available measurement for each nutrient.
    for label, possible_names in nutrient_names.items():
        for nutrient_name in possible_names:
            rows = food_data[
                food_data["name"] == nutrient_name
            ]

            if not rows.empty:
                row = rows.iloc[0]
                amount = row["amount"]

                if pd.isna(amount):
                    amount = None
                else:
                    amount = float(amount)

                summary["nutrition"][label] = {
                    "amount": amount,
                    "unit": row["unit_name"],
                }
                break

    return summary

