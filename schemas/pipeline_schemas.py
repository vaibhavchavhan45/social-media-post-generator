# Data models for each step of the campaign pipeline used to check/parse what the model returns at every stage.

from pydantic import BaseModel, Field


class AudienceAnalysis(BaseModel):
    target_age_group: str = Field(description="Age range of the audience")
    primary_interest: str = Field(description="Hobbies, topics they like, topics they care about")
    pain_points: list[str] = Field(description="Common problems they face on the platform")
    platform_habits: str = Field(description="How they use the social platform")
    purchase_motivation: list[str] = Field(description="What drives them to purchase")


class CampaignStrategy(BaseModel):
    campaign_goal: list[str] = Field(description="Main objective: awareness, engagement, conversion, sales etc.")
    content_tone: str = Field(description="Voice/style per age group (GenZ vs Millennial vs Boomer etc.)")
    key_messages: list[str] = Field(description="Core messages to communicate about the product")
    content_angle: str = Field(description="Unique hook or approach for the campaign")
    posting_recommendations: str = Field(description="Best time/frequency to post for this audience")


class PostCopy(BaseModel):
    opening_attention: str = Field(description="Attention-grabbing first line to stop the scroll")
    main_body: list[str] = Field(description="Core content: value props, benefits, why the product matters")
    emotional_appeal: str = Field(description="Line that connects emotionally with the audience")
    social_proof: str = Field(description="Credibility element: testimonial, stats, achievements")
    call_to_action: str = Field(description="Clear action we want the audience to take")


class Hashtags(BaseModel):
    trending_hashtags: list[str] = Field(description="Currently popular hashtags relevant to the product")
    niche_hashtags: list[str] = Field(description="Specific, targeted hashtags for the audience")
    branded_hashtags: list[str] = Field(description="Product/company-specific hashtags")
    hashtags_count: int = Field(description="Recommended number of hashtags for this platform")
    hashtags_strategy: list[str] = Field(description="Why these hashtags were selected")


class CallToAction(BaseModel):
    cta_text: str = Field(description="The CTA phrase, e.g. SHOP NOW, LEARN MORE")
    cta_placement: str = Field(description="Where to place it: bio, mid-post, end, button etc.")
    urgency_element: str = Field(description="Time-sensitive or scarcity element, if applicable")
    link_destination: str = Field(description="Where the CTA should redirect: website/DM/landing page")
    conversion_optimization: str = Field(description="Tips to maximize click-through rate")


class FinalCampaign(BaseModel):
    audience_analysis: AudienceAnalysis
    campaign_strategy: CampaignStrategy
    post_copy: PostCopy
    hashtags: Hashtags
    call_to_action: CallToAction