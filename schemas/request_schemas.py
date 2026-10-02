# Request and response models for the API.

from pydantic import BaseModel, Field
from typing import Literal


class CampaignRequest(BaseModel):
    product_name: str = Field(..., min_length=2, description="Name of the product")
    product_description: str = Field(..., min_length=10, description="Short description of the product")
    platform: str = Field(..., description="Target social media platform")
    method: Literal["v1", "v2"] = Field(default="v2", description="Which pipeline version to run")


class CampaignResponse(BaseModel):
    structured_data: dict
    ready_to_post: str