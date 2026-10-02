# Uses an LLM to check that the product name and description are real, and the platform exists.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from schemas.validation_schemas import ValidationResult

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1",
)

parser = JsonOutputParser(pydantic_object=ValidationResult)

template = PromptTemplate(
    template=(
        "Check the following inputs for a social media campaign generator:\n"
        "Product name: {product_name}\n"
        "Product description: {product_description}\n"
        "Platform: {platform}\n\n"
        "Check 1: Is the product name a real, meaningful name (not random letters or gibberish)?\n"
        "Check 2: Is the product description a real, meaningful description (not random letters or gibberish)?\n"
        "Check 3: Is the platform a real, existing social media platform (e.g. Instagram, Threads, Bluesky, LinkedIn etc.)?\n\n"
        "{format_instruction}"
    ),
    input_variables=["product_name", "product_description", "platform"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)

validation_chain = template | model | parser


def validate_input(product_name: str, product_description: str, platform: str) -> dict:
    """
        Run the 3 inputs through the validation chain and return the result for each.
    """
    result = validation_chain.invoke({
        "product_name": product_name,
        "product_description": product_description,
        "platform": platform,
    })
    return result