# Prompt templates for the 5 campaign stages, each telling the LLM what to create and in what format.

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from schemas.pipeline_schemas import AudienceAnalysis, CampaignStrategy, PostCopy, Hashtags, CallToAction

parser1 = JsonOutputParser(pydantic_object=AudienceAnalysis)
parser2 = JsonOutputParser(pydantic_object=CampaignStrategy)
parser3 = JsonOutputParser(pydantic_object=PostCopy)
parser4 = JsonOutputParser(pydantic_object=Hashtags)
parser5 = JsonOutputParser(pydantic_object=CallToAction)

template1 = PromptTemplate(
    template="Analyse the target audience for this product: {product_name}, {product_description}, {platform} \n {format_instruction}",
    input_variables=["product_name", "product_description", "platform"],
    partial_variables={"format_instruction": parser1.get_format_instructions()},
)

template2 = PromptTemplate(
    template="Based on this audience data: {input} \n\nCreate a comprehensive campaign strategy \n {format_instruction}",
    input_variables=["input"],
    partial_variables={"format_instruction": parser2.get_format_instructions()},
)

template3 = PromptTemplate(
    template="Using this campaign strategy data: {input} \n\nCreate an engaging post copy \n {format_instruction}",
    input_variables=["input"],
    partial_variables={"format_instruction": parser3.get_format_instructions()},
)

template4 = PromptTemplate(
    template="Using this post copy data: {input} \n\nCreate appropriate hashtags for {platform} \n {format_instruction}",
    input_variables=["input", "platform"],
    partial_variables={"format_instruction": parser4.get_format_instructions()},
)

template5 = PromptTemplate(
    template="Using this hashtags and campaign data: {input} \n\nCreate a compelling call-to-action \n {format_instruction}",
    input_variables=["input"],
    partial_variables={"format_instruction": parser5.get_format_instructions()},
)