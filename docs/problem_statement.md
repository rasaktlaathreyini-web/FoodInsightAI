# FoodInsightAI: Problem Statement

## Problem
Most food and nutrition apps offer calorie tracking and basic advice, but they
cannot understand natural-language questions about nutrition, allergens, food
safety, recipes, and ingredient substitutions at the same time. General-purpose
chatbots can answer these questions, but prior research found that LLM-generated
allergen-free diets can still contain allergens and can miscalculate quantities
and energy values (Niszczota & Rybicka, 2023, as reviewed in Ma et al., 2024).

## Goal
Build a multi-agent, retrieval-grounded food assistant that:
- answers food questions in natural language, with cited sources
- computes nutrient totals in code instead of letting the LLM guess
- screens ingredients for allergens using deterministic rules
- generates recipes and suggests ingredient substitutions
- personalizes suggestions using diet type, allergies, and goals

## Scope
In scope: nutrition lookup, allergen screening, food-safety Q&A, recipe
generation, ingredient substitution, personalization (session only).
Out of scope: medical diagnosis, treatment advice, storing personal health data.

## Approach
Retrieval-augmented generation (RAG) over USDA food data and recipe datasets,
a router plus specialist agents (LangGraph), a rule-based safety layer, and a
verifier that checks answers against retrieved sources.

## Evaluation plan
Compare three systems on the same test questions: plain LLM, RAG only, and the
full multi-agent system. Metrics: answer accuracy, allergen-miss rate, citation
correctness.

## Base paper
Ma, P., Tsai, S., He, Y., Jia, X., Zhen, D., Yu, N., Wang, Q., Ahuja, J.K.C., &
Wei, C.-I. (2024). Large language models in food science: Innovations,
applications, and future. Trends in Food Science & Technology, 148, 104488.
https://doi.org/10.1016/j.tifs.2024.104488

## Limitations (acknowledged up front)
LLMs can hallucinate; datasets over-represent some cuisines; this is a
learning/research project and not a substitute for a dietitian or doctor.