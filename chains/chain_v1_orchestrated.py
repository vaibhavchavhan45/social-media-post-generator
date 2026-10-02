# Method v1: runs the campaign pipeline step by step, so each stage's output can be checked before the next.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from prompts import template1, template2, template3, template4, template5
from prompts import parser1, parser2, parser3, parser4, parser5

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1",
)


def run_campaign_pipeline(product_input: dict) -> dict:
    """
        Run the 5 campaign stages one after another and return the output of each stage.
    """
    # step 1: understand the target audience
    audience = (template1 | model | parser1).invoke(product_input)

    # step 2: build a campaign strategy using the audience data
    strategy = (template2 | model | parser2).invoke({
        "input": {
            "primary_interest": audience.get("primary_interest"),
            "pain_points": audience.get("pain_points"),
            "purchase_motivation": audience.get("purchase_motivation"),
        }
    })

    # step 3: write the post copy using the strategy
    post = (template3 | model | parser3).invoke({
        "input": {
            "content_tone": strategy.get("content_tone"),
            "key_messages": strategy.get("key_messages"),
            "content_angle": strategy.get("content_angle"),
        }
    })

    # step 4: create hashtags based on the post
    hashtags = (template4 | model | parser4).invoke({
        "input": {
            "opening_attention": post.get("opening_attention"),
            "main_body": post.get("main_body"),
        },
        "platform": product_input.get("platform"),
    })

    # step 5: create the call-to-action
    cta = (template5 | model | parser5).invoke({"input": hashtags})

    return {
        "audience_analysis": audience,
        "campaign_strategy": strategy,
        "post_copy": post,
        "hashtags": hashtags,
        "call_to_action": cta,
    }