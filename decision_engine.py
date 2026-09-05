def make_decision(message, articles, customer):

    # Customer not found
    if customer is None:
        return "ESCALATE"


    message_lower = message.lower()


    # No knowledge base article
    if not articles:
        return "ESCALATE"


    # Billing conflict
    # Example:
    # Customer says "I already paid"
    # But account says "Outstanding"
    if (
        ("paid" in message_lower or "payment made" in message_lower)
        and customer["billing_status"] == "Outstanding"
    ):
        return "ESCALATE"


    # Account is not active
    if customer["account_status"] != "Active":
        return "ESCALATE"


    # Billing issue
    if articles[0]["category"] == "Billing":

        if customer["billing_status"] == "Outstanding":
            return "NEED_INFO"

        return "RESOLVE"


    # Internet troubleshooting
    if articles[0]["category"] == "Internet":

        return "RESOLVE"


    # Account problems
    if articles[0]["category"] == "Account":

        return "NEED_INFO"


    # Anything unknown
    return "ESCALATE"