from task_4 import should_escalate , CustomerContext

def test_rule1_low_confidence():
    """Escalate when confidence < 0.65 because AI answer is unreliable."""

    ctx = CustomerContext("123", False, False, [], True)

    result = should_escalate(ctx, 0.5, 0.2, "billing_question")

    assert result== (True,"low_confidence")

def test_rule2_angry_customer():
    """Escalate when sentiment < -0.6 as customer might be too frustrated for AI to handle"""
    ctx = CustomerContext("123", False, False, [], True)

    result = should_escalate(ctx, 0.8, -0.7 , "billing_question")

    assert result== (True,"angry_customer")
    
def test_rule3_repeat_complaint():
    """Escalate when repeated complaint ~3+ times, human takeover necessary as unresolved recurring issue"""
    ctx = CustomerContext("123", False, False, ["billing_question","billing_question","billing_question"], True)

    result = should_escalate(ctx, 0.8, 0.7 , "billing_question")

    assert result==(True,"repeat_complaint")

def test_rule4_service_cancellation():
    """Checks intent for cancellation, always escalate, no exception"""
    ctx = CustomerContext("123", False, False, [], True)

    result = should_escalate(ctx, 0.8, 0.7 , "service_cancellation")

    assert result==(True,"service_cancellation")

def test_rule5_vip_overdue():
    """Checks if user is VIP and billing is overdue"""
    ctx = CustomerContext("123", True, True, [], True)

    result = should_escalate(ctx, 0.8, 0.7 , "billing_question")

    assert result==(True,"vip_billing_issue")

def test_rule6_data_confidence():
    """Checks both data completion and confidence score,if incomplete AND confidence below 0.8"""
    ctx = CustomerContext("123", False, False, [], False)

    result = should_escalate(ctx, 0.7, 0.7 , "data_issue")

    assert result==(True,"incomplete_data")

def test_rule_edge_1():
    """Checks for confidence and intent, intent overrides confidence(even if it is high) if it is Service Cancellation"""
    ctx = CustomerContext("123", False, False, [], True)

    result = should_escalate(ctx, 0.9, 0.7 , "service_cancellation")

    assert result==(True,"service_cancellation")

def test_rule_edge_2():
    """If multiple rules trigger, return the first rule encountered"""
    ctx = CustomerContext("123", False, False, [], True)

    result = should_escalate(ctx, 0.5, -0.7 , "billing_question")

    assert result==(True,"low_confidence")
