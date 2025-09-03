---
lang: en
source_lang: kr
source_sha: 20c5c8fd9de01d6cfe00191ca847c15adfb7eeec25ea5b30c136fcdbddbca3d8
---
# Prompt Recipes

## Docker Image Optimization
"Rewrite using our standard Dockerfile template (multi-stage + alpine), remove unnecessary packages, suggest cache strategies, apply `--platform`, and provide a docker inspect size report."

## React Chunk Optimization
"Load font/icon resources separately, exclude unicons TTF/EOT, prioritize WOFF2. Show a table comparing bundle sizes before and after optimization and highlight the timeline."

## Prisma Migration Review
"Review compliance with composite key/relationship naming conventions, outline the downgrade migration path, and summarize the risk level (High/Medium/Low)."

## Python 3.13 FastAPI Boilerplate
"Generate scaffolding that passes `mypy --strict`, uses pydantic v2, prohibits synchronous/asynchronous mixing, and separates modules for router/schema/service layers."

## API Documentation Generation
"Automatically generate OpenAPI 3.0 specification documents based on the FastAPI app's routes and Pydantic models, including Swagger UI configuration."

## Code Style Improvement
"Refactor this Python code to conform to PEP 8 standards.  Specifically, make variable, function, and class names clear and descriptive, and remove unnecessary comments."

## Performance Analysis
"Analyze the bottlenecks of this Node.js Express app using profiling tools and provide specific suggestions and code modifications for performance improvement."
