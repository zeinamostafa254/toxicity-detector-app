import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field

load_dotenv()

st.set_page_config(
    page_title="Toxic Content Detector",
    page_icon="",
    layout="centered",
)

st.title("Toxic Content Detector")
st.write(
    "Enter a piece of text and the LLM will classify it as "
    "Toxic or Non-Toxic and provide a short explanation."
)


class ToxicityResult(BaseModel):
    """Validated result returned by the LLM."""

    classification: str = Field(
        description="Exactly one of: Toxic or Non-Toxic"
    )
    explanation: str = Field(
        description="A concise explanation of why the text received this classification."
    )


api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b")

if not api_key:
    st.error(
        "OPENROUTER_API_KEY is not configured. "
        "Create a .env file locally or provide the variable to Docker."
    )
    st.stop()

model = ChatOpenRouter(
    model=model_name,
    temperature=0,
    max_tokens=180,
)

structured_model = model.with_structured_output(
    ToxicityResult,
    method="function_calling",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a strict toxic-content classification system.

Classify the user's text into exactly one category:
- Toxic: the text contains abusive, hateful, threatening, harassing,
  demeaning, or otherwise clearly harmful language directed at a person
  or protected group.
- Non-Toxic: the text does not meet the Toxic definition.

Do not classify a text as toxic merely because it discusses toxicity,
insults, violence, politics, or controversial subjects in a neutral,
descriptive, quoted, or educational way.

Return a concise explanation based only on the submitted text.
Never invent context that is not present.""",
        ),
        ("human", "{text}"),
    ]
)

chain = prompt | structured_model

text = st.text_area(
    "Text to analyze",
    height=180,
    placeholder="Type or paste text here...",
)

if st.button("Analyze", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                result = chain.invoke({"text": text.strip()})

                classification = result.classification.strip()
                if classification.lower() == "toxic":
                    st.error("Classification: Toxic")
                else:
                    st.success("Classification: Non-Toxic")

                st.subheader("Explanation")
                st.write(result.explanation)

                with st.expander("Technical details"):
                    st.write(f"Model: {model_name}")
                    st.write("Framework: LangChain")
                    st.write("Provider: OpenRouter")
                    st.write("Output validation: Pydantic structured output")

            except Exception as exc:
                st.error("The model request failed.")
                st.exception(exc)
