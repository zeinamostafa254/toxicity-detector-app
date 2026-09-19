# Toxic Content Detection

A simple toxic-content classification application built with LangChain, OpenRouter, and Streamlit.

## Stack

- Python 3.12
- LangChain
- `langchain-openrouter`
- OpenRouter
- Pydantic structured output
- Streamlit
- Docker
- uv

## Run locally

```bash
uv sync
copy .env.example .env
```

Edit `.env` and add your OpenRouter API key.

Then:

```bash
uv run streamlit run app.py
```

Open the Streamlit URL shown in the terminal.

## Docker

Build:

```bash
docker build -t toxic-content-detector .
```

Run:

```bash
docker run --rm -p 8501:8501 --env-file .env toxic-content-detector
```

Open `http://localhost:8501`.

## Classification

The application performs binary classification:

- Toxic
- Non-Toxic

The LLM is instructed to judge the text rather than generate a free-form response. LangChain structures the prompt and validates the result against a Pydantic schema.
