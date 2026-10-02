# Converts the final JSON output into a plain, ready-to-post text.

def format_post(result: dict) -> str:
    """
        Join the post copy, call-to-action and hashtags from the result into one plain text post.
    """
    post = result.get("post_copy", {})
    cta = result.get("call_to_action", {})
    hashtags = result.get("hashtags", {})

    lines = []

    lines.append(post.get("opening_attention", ""))
    lines.append("")

    for line in post.get("main_body", []):
        lines.append(line)
    lines.append("")

    lines.append(post.get("emotional_appeal", ""))
    lines.append("")

    lines.append(post.get("social_proof", ""))
    lines.append("")

    lines.append(cta.get("cta_text", ""))
    lines.append("")

    all_tags = (
        hashtags.get("branded_hashtags", [])
        + hashtags.get("niche_hashtags", [])
        + hashtags.get("trending_hashtags", [])
    )
    lines.append(" ".join(all_tags))

    return "\n".join(lines)