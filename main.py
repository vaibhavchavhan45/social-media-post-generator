# CLI entry point that asks for the product details and generates the campaign.

import argparse

from cli.product_input import get_product_input
from cli.campaign_runner import generate_and_show


def main():
    """
        Read the version option, get valid inputs from the user, and generate the campaign.
    """
    parser = argparse.ArgumentParser(description="Run the social campaign generator")
    parser.add_argument("--version", choices=["v1", "v2"], default="v2")
    args = parser.parse_args()

    product_input = get_product_input()
    generate_and_show(product_input, args.version)


if __name__ == "__main__":
    main()
