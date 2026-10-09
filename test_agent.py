
import agent


def test_find_existing_order():
    result = agent.find_order("ORD-1001")

    assert result["found"] is True
    assert result["order"]["order_id"] == "ORD-1001"


def test_find_missing_order():
    result = agent.find_order("ORD-9999")

    assert result["found"] is False


def test_analyze_orders_returns_statistics():
    result = agent.analyze_orders(
        category="",
        status="",
        month=""
    )

    assert result["order_count"] > 0
    assert result["revenue_inr"] >= 0
    assert result["quantity_sold"] >= 0


def test_analyze_orders_no_matching_status():
    result = agent.analyze_orders(
        category="",
        status="no-such-status",
        month=""
    )

    assert result["order_count"] == 0
    assert result["revenue_inr"] == 0