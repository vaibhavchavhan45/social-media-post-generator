# API route that generates a campaign and returns the full campaign data and ready-to-post text as JSON.

from fastapi import APIRouter, HTTPException

from schemas.request_schemas import CampaignRequest, CampaignResponse
from chains.chain_v1_orchestrated import run_campaign_pipeline
from chains.chain_v2_pipeline import chain as chain_v2
from services.formatter import format_post
from validations.input_validation import validate_input

router = APIRouter()


@router.post("/generate-campaign", response_model=CampaignResponse, summary="Generate Campaign JSON")
def generate_campaign(request: CampaignRequest):
    """Check the inputs, generate the campaign, and return the full data and ready-to-post text as JSON."""
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
        errors = {}
        if not validation["product_name_valid"]:
            errors["product_name"] = validation["product_name_reason"]
        if not validation["product_description_valid"]:
            errors["product_description"] = validation["product_description_reason"]
        if not validation["platform_valid"]:
            errors["platform"] = validation["platform_reason"]

        raise HTTPException(
            status_code=400,
            detail={"message": "Invalid input. Please resend all fields corrected.", "errors": errors},
        )

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

    post_text = format_post(result)

    return CampaignResponse(structured_data=result, ready_to_post=post_text)