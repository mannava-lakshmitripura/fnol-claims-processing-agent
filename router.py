def route_claim(extracted, missing_fields):
    description = (extracted.get("description") or "").lower()
    estimated_damage = extracted.get("estimated_damage")
    claim_type = extracted.get("claim_type")

    if missing_fields:
        return "Manual Review", "Mandatory fields are missing"

    if any(word in description for word in ["fraud", "staged", "inconsistent"]):
        return "Investigation Flag", "Suspicious keywords found in description"

    if claim_type == "injury":
        return "Specialist Queue", "Injury-related claim"

    if isinstance(estimated_damage, int) and estimated_damage < 25000:
        return "Fast-track", "Low estimated damage"

    return "Standard Processing", "Default routing applied"
