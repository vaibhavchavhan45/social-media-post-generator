# Asks the user for the product details and keeps asking until they are valid.

from validations.input_validation import validate_input


def get_product_input():
    """
        Ask for the 3 inputs, re-ask only the invalid one, and return them once all are valid.
    """
    print("Enter product details (all 3 fields will be validated together):")
    product_name = input("Product name: ").strip()
    product_description = input("Product description: ").strip()
    platform = input("Platform: ").strip()

    while True:
        result = validate_input(product_name, product_description, platform)

        if result["product_name_valid"] and result["product_description_valid"] and result["platform_valid"]:
            break

        if not result["product_name_valid"]:
            print(f"Product name invalid: {result['product_name_reason']}")
            product_name = input("Product name: ").strip()
            continue

        if not result["product_description_valid"]:
            print(f"Product description invalid: {result['product_description_reason']}")
            product_description = input("Product description: ").strip()
            continue

        if not result["platform_valid"]:
            print(f"Platform invalid: {result['platform_reason']}")
            platform = input("Platform: ").strip()
            continue

    return {
        "product_name": product_name,
        "product_description": product_description,
        "platform": platform,
    }
