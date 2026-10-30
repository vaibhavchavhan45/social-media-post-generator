# [Social Campaign Generator](https://social-media-post-generator-yud5.onrender.com/docs)

A pipeline that builds a full social media campaign for a product. You give it a product name, description and target platform, and it handles the audience research, strategy, post copy, hashtags and call-to-action in one connected flow.

Built with **Python**, **FastAPI** and **LangChain**, using the **OpenAI model**.

[Live API](https://social-media-post-generator-yud5.onrender.com/docs)

## How It Works

The pipeline runs five stages, and each stage's output feeds the next:

1. **Audience Analysis**: age group, interests, pain points, platform habits, purchase motivation
2. **Campaign Strategy**: goals, tone, key messages, content angle, posting recommendations
3. **Post Copy**: opening line, main body, emotional appeal, social proof, CTA line
4. **Hashtags**: trending, niche and branded hashtags with a short strategy note
5. **Call-to-Action**: CTA text, placement, urgency, link destination

- Model: `openai/gpt-oss-120b`, via Groq's OpenAI-compatible API (`langchain-openai`).

## Features

- Full campaign from three inputs: product name, description and platform
- Prompt chaining, where every stage builds on the previous one
- Two pipeline versions (step-by-step and a connected LCEL chain)
- LLM-based input validation
- CLI and FastAPI interfaces

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/generate-campaign` | Full result as JSON: `structured_data` (all 5 stages) and `ready_to_post` |
| POST | `/generate-campaign/ready-to-post` | Only the ready-to-post text, as plain text |

Both take the same body: `product_name`, `product_description`, `platform` and `method` (`v1` or `v2`).

Try them live at [social-media-post-generator-yud5.onrender.com/docs](https://social-media-post-generator-yud5.onrender.com/docs), with no setup needed.

## Setup

```bash
cd social-campaign-generator
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your key:

```
GROQ_API_KEY=your_api_key_here
```

## Run

```bash
python main.py --version v1   # CLI, step-by-step pipeline
python main.py --version v2   # CLI, connected pipeline (default)
uvicorn app:app --reload      # API at http://127.0.0.1:8000/docs
```

## Sample

Request:

```json
{
  "product_name": "Smartwatch",
  "product_description": "A new-gen smartwatch with voice calling and health tracking.",
  "platform": "Instagram",
  "method": "v2"
}
```

Response:

- `/generate-campaign` returns `structured_data` (all 5 stages) and `ready_to_post` (the plain text version, shown as a JSON string).
- `/generate-campaign/ready-to-post` returns only the ready-to-post text as plain text.
- On invalid input, both return an error listing which field failed and why.

## Two Pipeline Versions

Both the CLI and the API can run either version. They produce the same result structure and differ only in how the flow is built.

- `chains/chain_v1_orchestrated.py`: each stage is called on its own, one after another. Good for debugging, since every intermediate result can be checked.
- `chains/chain_v2_pipeline.py`: all stages are connected in one LCEL chain using `RunnablePassthrough.assign`, so every stage's output is carried forward, not just the last one.

## Input Validation

Before the pipeline runs, one LLM call checks that the product name and description are meaningful (not random text) and that the platform is a real social media platform.

- **CLI:** the invalid fields are pointed out and re-asked.
- **API:** the whole request is rejected with a message saying which field failed and why. The API is stateless, so the client resends all fields corrected.

## Project Structure

```text
social-campaign-generator/
├── api/
│   ├── routes.py                   JSON campaign endpoint
│   └── ready_to_post_routes.py     plain text campaign endpoint
├── chains/
│   ├── chain_v1_orchestrated.py
│   └── chain_v2_pipeline.py
├── cli/
│   ├── product_input.py            asks for product details and re-asks invalid ones
│   └── campaign_runner.py          runs the pipeline (v1 or v2) and prints the result
├── schemas/
│   ├── pipeline_schemas.py         data structure for each stage's output
│   ├── request_schemas.py          API request and response models
│   └── validation_schema.py        LLM validation response model
├── validations/
│   └── input_validation.py         LLM-based check for name, description, platform
├── services/
│   └── formatter.py                converts JSON into ready-to-post text
├── middleware/
│   └── error_handler.py            centralized API error handling
├── prompts.py                      prompt templates and parsers for each stage
├── main.py                         CLI entry point
├── app.py                          FastAPI entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

## Future Improvements

- Save each generated campaign in a database (SQLite), so users can search past campaigns by product name, platform or keyword.
- Add user login, so each user saves and searches only their own campaigns.
- Support several platforms in one request, returning a separate post for each, tailored to that platform's style.
- Let the user pick a tone (playful, formal, minimal) instead of the model choosing it each time.

## Author

Built by **Vaibhav Chavhan** | [GitHub](https://github.com/vaibhavchavhan45) | [LinkedIn](https://www.linkedin.com/in/vaibhavchavhan/) | [Portfolio](https://vaibhav-chavhan.vercel.app) | Email: [chavhanvaibhav708@gmail.com](mailto:chavhanvaibhav708@gmail.com)