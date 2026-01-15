import logging
from datetime import datetime
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain, SequentialChain
from langchain_community.callbacks import get_openai_callback
import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv(override=True)

key=os.getenv("Openai_api_key")
llm=ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    openai_api_key=key,
    tiktoken_model_name='openai/gpt-oss-20b:free',
    temperature=0.7
    )

with open(r"C:\Users\user\OneDrive\Desktop\Generative AI\genai-github\response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

template = """
Text:
{text}

You are an expert MCQ generator.

Your task is to create exactly {number} multiple-choice questions (MCQs) 
for {subject} students using the above text.

Difficulty / Tone:
{tone}

Instructions:
- Each question must be clear and relevant to the given text.
- Do NOT repeat any questions.
- Each MCQ must have four options.
- Only one option should be correct.
- Ensure all questions are conceptually accurate.

Return the output strictly in the JSON format shown below.
Do NOT add any extra text outside the JSON.

### RESPONSE_JSON
{RESPONSE_JSON}
"""

quiz_generation_prompt=PromptTemplate(
    input_variables=['text','number','subject','tone','RESPONSE_JSON'],
    template=template
)

quiz_chain=LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key='quiz',
    verbose=True
    )

template2 = """
You are an expert educational content reviewer.

Below is a quiz for {subject} students.

Your task is to:
1. Verify the factual correctness of each MCQ.
2. Confirm that the provided correct answers are accurate.
3. Improve grammar, clarity, and wording where needed.
4. Ensure all questions meet proper academic standards.
5. Fix or upgrade any MCQ that has errors or ambiguity.
6. Do NOT change the total number of questions.
7. Follow the response structure exactly as defined in response.json.

### QUIZ DATA
{quiz}
"""

quiz_evaluation_prompt=PromptTemplate(
    input_variables=['subject','quiz'],
    template=template2
)

review_chain=LLMChain(
    llm=llm,
    prompt=quiz_evaluation_prompt,
    output_key='review',
    verbose=True
    )

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=['text', 'number', 'subject','RESPONSE_JSON', 'tone'],  # combined input vars
    output_variables=['quiz', 'review'],                    # plural
    verbose=True
)