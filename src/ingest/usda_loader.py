
from pathlib import Path

import pandas as pd


def load_usda_csv(file_path):
    """
    Load a USDA FoodData Central CSV file.

    Args:
        file_path: Path to a USDA CSV file.

    Returns:
        A cleaned pandas DataFrame.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the file is empty or cannot be read.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"USDA CSV file not found: {path}")

    if not path.is_file():
        raise ValueError(f"The provided path is not a file: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"The USDA CSV file is empty: {path}")

    try:
        dataframe = pd.read_csv(path, low_memory=False)
    except (pd.errors.ParserError, UnicodeDecodeError) as error:
        raise ValueError(f"Could not parse USDA CSV file: {error}") from error
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"The USDA CSV file contains no data: {path}") from error

    if dataframe.empty:
        raise ValueError(f"The USDA CSV file contains no records: {path}")

    # Normalize column names for consistent processing.
    dataframe.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in dataframe.columns
    ]

    # Remove rows where every column is empty.
    dataframe = dataframe.dropna(how="all").reset_index(drop=True)

    return dataframe


def search_foods(dataframe, query, food_column="description", limit=10):
    """
    Search a USDA food DataFrame by a food-description column.

    Args:
        dataframe: DataFrame returned by load_usda_csv().
        query: Food name or partial food name.
        food_column: Column containing food descriptions.
        limit: Maximum number of results.

    Returns:
        A DataFrame containing matching foods.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query must be a non-empty string.")

    if limit < 1:
        raise ValueError("Limit must be at least 1.")

    column = food_column.strip().lower().replace(" ", "_")

    if column not in dataframe.columns:
        raise ValueError(
            f"Column '{column}' not found. "
            f"Available columns: {list(dataframe.columns)}"
        )

    matches = dataframe[
        dataframe[column]
        .astype("string")
        .str.contains(query.strip(), case=False, na=False, regex=False)
    ]

    return matches.head(limit).reset_index(drop=True)
