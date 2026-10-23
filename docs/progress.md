# Progress Log

## Day 1
- Created repo, folder structure, .gitignore, .env.example
- Wrote problem statement
- Next: pick LLM option, download USDA subset (Day 2)
## Day 2 — Local LLM Integration

### Completed

* Configured the Python virtual environment.
* Installed the Ollama Python client and supporting packages.
* Installed and verified the local Ollama model `llama3.2:3b`.
* Implemented the LLM wrapper in `src/llm.py`.
* Configured the model name through environment variables using `python-dotenv`.
* Successfully tested the local LLM wrapper.

### Technical Stack

* Python
* Ollama
* Llama 3.2 (3B)
* python-dotenv
* pytest
* NumPy

### Next Steps

* Download USDA Foundation Foods and SR Legacy datasets.
* Inspect the CSV files and their column structures.
* Implement the food data loader.
* Prepare the data pipeline for later embedding generation and retrieval.
## Day 3 — USDA Data Ingestion

### Completed

* Loaded USDA food records from CSV files.
* Loaded nutrient measurements and nutrient definitions.
* Implemented a reusable CSV loader in `src/ingest/usda_loader.py`.
* Added food-search functionality with case-insensitive matching.
* Added automated tests for CSV loading, missing files, empty files, and food search.

### Validation

* Verified that the loader handles missing and empty CSV files.
* Tested case-insensitive food searches.
* Confirmed that the food-search limit works correctly.
* Ran the automated tests successfully.

### Next Steps

* Connect food records to their nutrient measurements.
* Implement structured nutrition lookup.
* Add tests for nutrition queries.


## Day 4 — USDA Nutrition Lookup

### Completed
- Loaded USDA food, nutrient measurement, and nutrient definition datasets.
- Connected food records with their nutrient measurements.
- Implemented food-name search with preferred food-record ordering.
- Implemented structured nutrition summaries.
- Added automated tests for nutrition lookup and invalid searches.

### Validation
- Verified USDA dataset loading and ID relationships.
- Tested nutrition lookup using real USDA food data.
- Added automated tests using temporary CSV fixtures.

### Next Steps
- Improve food matching and nutrient selection.
- Connect structured nutrition results to the local LLM.
- Continue testing and documenting the application.
## Day 5: Nutrition Assistant Integration

**Goal:** Connect the USDA nutrition lookup system with the local LLM.

### Work Completed

* Created `src/nutrition_assistant.py`.
* Integrated the USDA nutrition lookup function with the local Llama 3.2 (3B) model through Ollama.
* Implemented `answer_nutrition_question()` to retrieve nutrition information and generate simple explanations.
* Added input validation for empty food queries.
* Implemented a response for foods that are not found in the available USDA dataset.
* Created `tests/test_nutrition_assistant.py` with automated tests for the assistant.
* Verified that the assistant can retrieve and explain nutrition information for hummus.
* Ran the automated test suite successfully.

### Outcome

FoodInsightAI can now combine structured USDA nutrition data with a locally running LLM to answer food-related nutrition queries.

### Next Steps

* Improve response reliability and prevent unsupported nutrition claims.
* Improve nutrition data search and handling of missing nutrient values.
* Expand automated test coverage.
* Continue developing the nutrition assistant.
