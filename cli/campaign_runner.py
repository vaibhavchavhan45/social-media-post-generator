# Runs the campaign pipeline (v1 or v2) and prints the result and the ready-to-post text.

import json

from chains.chain_v1_orchestrated import run_campaign_pipeline
from chains.chain_v2_pipeline import chain as chain_v2
from services.formatter import format_post

BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def run_v1(product_input):
    """
        Run the campaign with the step-by-step pipeline (v1).
    """
    return run_campaign_pipeline(product_input)


def run_v2(product_input):
    """
        Run the campaign with the connected pipeline (v2).
    """
    return chain_v2.invoke(product_input)


def generate_and_show(product_input, version):
    """
        Generate the campaign with the chosen version and print the data and the ready-to-post text.
    """
    print(f"\nRunning campaign generator ({version})...\n")

    try:
        if version == "v1":
            result = run_v1(product_input)
        else:
            result = run_v2(product_input)
    except Exception as e:
        print(f"{BOLD}{DIM}\nSomething went wrong while generating the campaign: {e}{RESET}")
        print(f"{BOLD}{DIM}Check your API key in .env and your internet connection, then try again.{RESET}")
        return

    print(json.dumps(result, indent=2, default=str))

    post_text = format_post(result)
    print(f"\n{BOLD}{DIM} Ready to Post on {product_input['platform']} {RESET}")
    print(post_text)
