import json

from src.ingest.nutrition_lookup import get_food_nutrition
from src.llm import ask_llm


def answer_nutrition_question(food_query: str) -> str:
    """Answer a nutrition question using USDA data and the local LLM."""

    if not isinstance(food_query, str) or not food_query.strip():
        raise ValueError("Food query must be a non-empty string.")

    nutrition_data = get_food_nutrition(food_query.strip())

    if nutrition_data is None:
        return (
            f"I couldn't find nutrition information for '{food_query}' "
            "in the available USDA dataset. Try another food name."
        )

    nutrition_json = json.dumps(nutrition_data, indent=2, default=str)

    prompt = f"""
Answer the user's nutrition question using the USDA data below.

USDA nutrition data:
{nutrition_json}

Instructions:
- Use only the nutrition values provided in the USDA data.
- Do not invent missing nutrient values.
- Include the food description in your answer.
- Include units for every nutrient value.
- If a nutrient is missing, clearly say it is not available.
- Explain the result in simple language.
"""

    return ask_llm(
        prompt,
        system=(
            "You are a food and nutrition assistant. "
            "Use the supplied USDA data as the source of nutrition values. "
            "Never invent nutrition measurements."
        ),
    )


if __name__ == "__main__":
    food = input("Enter a food to check (example: hummus): ").strip()

    try:
        print("\nFoodInsightAI:")
        print(answer_nutrition_question(food))
    except Exception as error:
        print(f"Could not answer the question: {error}")
