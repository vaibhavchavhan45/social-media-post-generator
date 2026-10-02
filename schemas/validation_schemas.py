# Response structure for the LLM-based input validation check.
from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    product_name_valid: bool = Field(description="True if the product name is meaningful, not gibberish")
    product_name_reason: str = Field(description="Short reason if invalid, empty string if valid")
    product_description_valid: bool = Field(description="True if the product description is meaningful, not gibberish")
    product_description_reason: str = Field(description="Short reason if invalid, empty string if valid")
    platform_valid: bool = Field(description="True if the platform is a real, existing social media platform")
    platform_reason: str = Field(description="Short reason if invalid, empty string if valid")