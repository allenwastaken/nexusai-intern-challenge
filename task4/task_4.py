from dataclasses import dataclass

@dataclass
class CustomerContext:
    phone: str
    is_vip: bool
    billing_overdue: bool
    ticket_history: list[str]
    data_complete: bool

def should_escalate(context, confidence_score, sentiment_score, intent):

    if intent == "service_cancellation":
        return True, "service_cancellation"

    if confidence_score < 0.65:
        return True, "low_confidence"

    if sentiment_score < -0.6:
        return True, "angry_customer"

    if context.ticket_history.count(intent) >= 3:
        return True, "repeat_complaint"

    if context.is_vip and context.billing_overdue:
        return True, "vip_billing_issue"

    if not context.data_complete and confidence_score < 0.80:
        return True, "incomplete_data"

    return False, "handled_by_ai"
