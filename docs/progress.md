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
