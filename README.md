# Social Campaign Generator

## Problem
Building a social media campaign for a product usually means doing audience research, deciding a strategy, writing post copy, picking hashtags, and creating a call-to-action, all separately. This project automates that entire flow using a connected, multi-step pipeline powered by an LLM.


## What It Does
The user provides a product name, description, and target platform. The pipeline then produces a full campaign output:
1. **Audience Analysis** — age group, interests, pain points, platform habits, purchase motivation.
2. **Campaign Strategy** — goals, tone, key messages, content angle, posting recommendations.
3. **Post Copy** — opening line, main body, emotional appeal, social proof, CTA line.
4. **Hashtags** — trending, niche, and branded hashtags with a short strategy note.
5. **Call-to-Action** — CTA text, placement, urgency, and link destination.

Each stage's output feeds into the next stage as input.


## Model
Uses `openai/gpt-oss-120b`, accessed via Groq's OpenAI-compatible API (through `langchain-openai`'s `ChatOpenAI` class).


## Input Validation
Before running the campaign pipeline, the product name, description, and platform are checked using a separate LLM call. It verifies:
- The product name is meaningful, not random text.
- The product description is meaningful, not random text.
- The platform is a real, existing social media platform (All real social media platforms are accepted).

If something is invalid, the behavior differs by interface:
- **CLI** — the invalid fields are pointed out and re-asked, since all 3 fields are validated together in one call.
- **API** — the entire request is rejected with a message showing which specific field failed and why. Since the API is stateless, the client must resend all fields corrected.


## Two Ways to Run
This project can be used in two ways:

- **CLI** (`main.py`) — asks for product details in the terminal, validates them, runs the pipeline, and prints the result.
- **API** (`app.py`) — a FastAPI backend with two endpoints. Comes with an interactive `/docs` page (Swagger UI) to test both endpoints directly in the browser, no separate tool needed.


## API Endpoints
- **POST `/generate-campaign`** — Returns the full result as JSON: `structured_data` (all 5 stages) and `ready_to_post` (the formatted text as an escaped JSON string).
- **POST `/generate-campaign/ready-to-post`** — Returns only the ready-to-post text, as true plain text (real line breaks, no JSON wrapping).

Both endpoints accept the same request body: `product_name`, `product_description`, `platform`, and `method` (`v1` or `v2`).


## Two Pipeline Implementations
Both the CLI and the API can run either version of the pipeline:

- `chains/chain_v1_orchestrated.py` — Each stage is called on its own, one after another. Good for debugging, since every intermediate result can be checked.
- `chains/chain_v2_pipeline.py` — All stages are connected into a single LCEL chain using `RunnablePassthrough.assign`, so every stage's output is carried forward, not just the last one.

Both produce the same result structure; they differ in how the flow is built.


## Concepts Used
- Multi-stage LLM pipelines
- Structured output parsing (Pydantic + JSON)
- Prompt chaining
- LangChain Expression Language (LCEL)
- LLM-based input validation
- REST API design (FastAPI)
- Centralized error handling


## Project Structure
social-campaign-generator/
├── api/
│ ├── routes.py - JSON campaign endpoint
│ └── ready_to_post_routes.py - plain text campaign endpoint
├── chains/
│ ├── chain_v1_orchestrated.py
│ └── chain_v2_pipeline.py
├── cli/
│ ├── product_input.py - asks for the product details and re-asks invalid ones
│ └── campaign_runner.py - runs the pipeline (v1 or v2) and prints the result
├── schemas/
│ ├── pipeline_schemas.py - data structure for each stage's output
│ ├── request_schemas.py - API request/response models
│ └── validation_schema.py - LLM validation response model
├── validations/
│ └── input_validation.py - LLM-based check for product name, description, platform
├── services/
│ └── formatter.py - converts JSON into a plain, ready-to-post text
├── middleware/
│ └── error_handler.py - centralized API error handling
├── prompts.py - prompt templates + parsers for each stage
├── main.py - CLI entry point (uses cli/)
├── app.py - FastAPI entry point
├── requirements.txt
├── .env.example
└── .gitignore


## Setup
1. Clone the repository and move into the project folder:
cd social-campaign-generator


2. Create a virtual environment:
python3 -m venv venv


3. Activate the virtual environment:
- macOS/Linux:
source venv/bin/activate

- Windows:
venv\Scripts\activate


4. Install dependencies:
pip install -r requirements.txt


5. Copy `.env.example` to `.env` and add your Groq API key:
GROQ_API_KEY=your_api_key_here


## Run (CLI)
- Step-by-step version:
python main.py --version v1

- Connected pipeline version (default):
python main.py --version v2


## Run (API)
**Locally:**
uvicorn app:app --reload

Then open `http://127.0.0.1:8000/docs` in the browser to test both endpoints interactively.

**Live (deployed):**
Open `<live-link>/docs` in the browser to test both endpoints interactively. No local setup needed.


## Sample Request (API)
```json
{
  "product_name": "Smartwatch",
  "product_description": "A new-gen smartwatch with voice calling and health tracking.",
  "platform": "Instagram",
  "method": "v2"
}
```


## Sample Response
- `/generate-campaign` — on valid input, returns a JSON object with `structured_data` (all 5 stages) and `ready_to_post` (plain text version, shown as a JSON string). On invalid input, returns an error listing which specific field failed and why.
- `/generate-campaign/ready-to-post` — on valid input, returns only the ready-to-post text as plain text. On invalid input, returns an error listing which specific field failed and why.


## Future Improvements
- Save each generated campaign in a database (SQLite), so a user can look back and search past campaigns by product name, platform or keyword.
- Add user login (auth), so each user can save and search only their own past campaigns.
- Support more platforms at once, so one request takes a list of platforms and returns a separate post for each, tailored to that platform's style.
- Let the user pick a tone or style preference (for example, playful, formal, minimal) instead of the model choosing it on its own each time.