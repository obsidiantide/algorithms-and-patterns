"""Unit tests for the Facade Pattern implementation."""
import pytest
from patterns.structural.facade import (
    InventoryService,
    NotificationService,
    OrderProcessingFacade,
    PaymentService,
    ShippingService,
)


def test_place_order_success():
    inventory = InventoryService({"item-1": 10})
    facade = OrderProcessingFacade(inventory=inventory)

    result = facade.place_order("cust-1", "item-1", quantity=2, amount=49.99)
    assert result.success is True
    assert result.order_id and result.tracking_number
    assert inventory.get_stock("item-1") == 8
    assert len(facade.payment.transactions) == 1
    assert len(facade.shipping.shipments) == 1
    assert len(facade.notification.messages) == 1


def test_place_order_insufficient_stock():
    inventory = InventoryService({"item-1": 1})
    facade = OrderProcessingFacade(inventory=inventory)

    result = facade.place_order("cust-1", "item-1", quantity=5, amount=100.0)
    assert result.success is False
    assert "Insufficient inventory" in str(result.error)
    assert inventory.get_stock("item-1") == 1
    assert not facade.payment.transactions


def test_place_order_payment_failure_rollback():
    inventory = InventoryService({"item-1": 5})

    class FailingPaymentService(PaymentService):
        def charge(self, customer_id: str, amount: float) -> bool:
            return False

    facade = OrderProcessingFacade(inventory=inventory, payment=FailingPaymentService())
    result = facade.place_order("cust-1", "item-1", quantity=2, amount=50.0)

    assert result.success is False
    assert result.error == "Payment processing failed"
    assert inventory.get_stock("item-1") == 5
    assert not facade.shipping.shipments


def test_place_order_invalid_inputs():
    facade = OrderProcessingFacade()
    with pytest.raises(ValueError, match="Quantity and amount must be positive"):
        facade.place_order("cust-1", "item-1", quantity=0, amount=10.0)
    with pytest.raises(ValueError, match="Quantity and amount must be positive"):
        facade.place_order("cust-1", "item-1", quantity=1, amount=-5.0)


def test_custom_subsystem_injection():
    inv, pay, ship, notify = InventoryService(), PaymentService(), ShippingService(), NotificationService()
    facade = OrderProcessingFacade(inv, pay, ship, notify)
    assert facade.inventory is inv and facade.payment is pay
    assert facade.shipping is ship and facade.notification is notify
