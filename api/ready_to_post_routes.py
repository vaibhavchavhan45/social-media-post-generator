# API route that generates a campaign and returns only the ready-to-post text as plain text.

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from schemas.request_schemas import CampaignRequest
from chains.chain_v1_orchestrated import run_campaign_pipeline
from chains.chain_v2_pipeline import chain as chain_v2
from services.formatter import format_post
from validations.input_validation import validate_input

router = APIRouter()


@router.post("/generate-campaign/ready-to-post", response_class=PlainTextResponse)
def generate_campaign_plain_text(request: CampaignRequest):
    """Check the inputs, generate the campaign, and return the ready-to-post text as plain text."""
    validation = validate_input(
        request.product_name,
        request.product_description,
        request.platform,
    )

    if not (
        validation["product_name_valid"]
        and validation["product_description_valid"]
        and validation["platform_valid"]
    ):
        errors = []
        if not validation["product_name_valid"]:
            errors.append(f"product_name: {validation['product_name_reason']}")
        if not validation["product_description_valid"]:
            errors.append(f"product_description: {validation['product_description_reason']}")
        if not validation["platform_valid"]:
            errors.append(f"platform: {validation['platform_reason']}")

        raise HTTPException(status_code=400, detail="; ".join(errors))

    product_input = {
        "product_name": request.product_name,
        "product_description": request.product_description,
        "platform": request.platform,
    }

    try:
        if request.method == "v1":
            result = run_campaign_pipeline(product_input)
        else:
            result = chain_v2.invoke(product_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Campaign generation failed: {e}")

    return format_post(result)