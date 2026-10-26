import json

from src.ingest.nutrition_lookup import get_food_nutrition
from src.llm import ask_llm


def answer_nutrition_question(food_query: str) -> str:
    """Answer a nutrition question using USDA data and the local LLM."""

    if not isinstance(food_query, str) or not food_query.strip():
        raise ValueError("Food query must be a non-empty string.")

    query = food_query.strip()
    nutrition_data = get_food_nutrition(query)

    if nutrition_data is None:
        return (
            f"I couldn't find nutrition information for '{query}' "
            "in the available USDA dataset. Try another food name."
        )

    nutrition_json = json.dumps(nutrition_data, indent=2, default=str)

    prompt = f"""
Answer the user's nutrition question using the USDA data below.

USDA nutrition data:
{nutrition_json}

Instructions:
- Use only the nutrition values provided in the USDA data.
- Never invent, estimate, or change nutrient measurements.
- Include the food description in your answer.
- Include the original units for every nutrient value.
- If a nutrient is missing, clearly say it is not available.
- Do not invent daily recommended intake percentages or daily values.
- Do not make unsupported health claims.
- Do not call a food healthy or unhealthy based on insufficient data.
- Do not claim a nutrient is a good or poor source without supporting data.
- Explain the available information in simple language.
- Clarify that values refer to the specific USDA food record provided.
"""

    return ask_llm(
        prompt,
        system=(
            "You are a careful food and nutrition assistant. "
            "Use supplied USDA data as the source of nutrition measurements. "
            "Never invent measurements, daily-value percentages, or health claims. "
            "If the data does not support a conclusion, say so."
        ),
    )


if __name__ == "__main__":
    food = input("Enter a food to check (example: hummus): ").strip()

    try:
        print("\nFoodInsightAI:")
        print(answer_nutrition_question(food))
    except Exception as error:
        print(f"Could not answer the question: {error}")
