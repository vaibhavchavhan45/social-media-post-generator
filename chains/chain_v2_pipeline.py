# Method v2: runs the campaign pipeline as one connected chain and keeps the output of every stage.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from prompts import template1, template2, template3, template4, template5
from prompts import parser1, parser2, parser3, parser4, parser5

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1",
)

stage1 = template1 | model | parser1

stage2 = RunnableLambda(lambda x: {
    "input": {
        "primary_interest": x["audience_analysis"].get("primary_interest"),
        "pain_points": x["audience_analysis"].get("pain_points"),
        "purchase_motivation": x["audience_analysis"].get("purchase_motivation"),
    }
}) | template2 | model | parser2

stage3 = RunnableLambda(lambda x: {
    "input": {
        "content_tone": x["campaign_strategy"].get("content_tone"),
        "key_messages": x["campaign_strategy"].get("key_messages"),
        "content_angle": x["campaign_strategy"].get("content_angle"),
    }
}) | template3 | model | parser3

stage4 = RunnableLambda(lambda x: {
    "input": {
        "opening_attention": x["post_copy"].get("opening_attention"),
        "main_body": x["post_copy"].get("main_body"),
    },
    "platform": x["platform"],
}) | template4 | model | parser4

stage5 = RunnableLambda(lambda x: {
    "input": x["hashtags"]
}) | template5 | model | parser5

chain = (
    RunnablePassthrough.assign(audience_analysis=stage1)
    | RunnablePassthrough.assign(campaign_strategy=stage2)
    | RunnablePassthrough.assign(post_copy=stage3)
    | RunnablePassthrough.assign(hashtags=stage4)
    | RunnablePassthrough.assign(call_to_action=stage5)
)