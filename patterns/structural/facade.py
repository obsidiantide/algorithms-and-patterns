"""Facade Pattern implementation providing a unified interface to a subsystem."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
import uuid


class InventoryService:
    """Manages product stock levels and reservations."""

    def __init__(self, initial_stock: Optional[Dict[str, int]] = None) -> None:
        self._stock: Dict[str, int] = dict(initial_stock or {})

    def get_stock(self, item_id: str) -> int:
        return self._stock.get(item_id, 0)

    def reserve(self, item_id: str, quantity: int) -> bool:
        if self._stock.get(item_id, 0) >= quantity:
            self._stock[item_id] -= quantity
            return True
        return False

    def release(self, item_id: str, quantity: int) -> None:
        self._stock[item_id] = self._stock.get(item_id, 0) + quantity


class PaymentService:
    """Handles payment validation and charging."""

    def __init__(self) -> None:
        self.transactions: List[dict] = []

    def charge(self, customer_id: str, amount: float) -> bool:
        if amount <= 0:
            return False
        self.transactions.append({"customer_id": customer_id, "amount": amount})
        return True


class ShippingService:
    """Schedules dispatch and tracking for fulfilled orders."""

    def __init__(self) -> None:
        self.shipments: List[dict] = []

    def dispatch(self, customer_id: str, item_id: str, quantity: int) -> str:
        tracking_num = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        self.shipments.append({"customer_id": customer_id, "item_id": item_id, "tracking": tracking_num})
        return tracking_num


class NotificationService:
    """Sends status messages and confirmations to customers."""

    def __init__(self) -> None:
        self.messages: List[tuple[str, str]] = []

    def send(self, customer_id: str, message: str) -> None:
        self.messages.append((customer_id, message))


@dataclass(frozen=True)
class OrderResult:
    """Result of an order placement attempt via the facade."""

    success: bool
    order_id: Optional[str] = None
    tracking_number: Optional[str] = None
    error: Optional[str] = None


class OrderProcessingFacade:
    """Unified facade coordinating inventory, payment, shipping, and notification."""

    def __init__(
        self,
        inventory: Optional[InventoryService] = None,
        payment: Optional[PaymentService] = None,
        shipping: Optional[ShippingService] = None,
        notification: Optional[NotificationService] = None,
    ) -> None:
        self.inventory = inventory or InventoryService()
        self.payment = payment or PaymentService()
        self.shipping = shipping or ShippingService()
        self.notification = notification or NotificationService()

    def place_order(
        self, customer_id: str, item_id: str, quantity: int, amount: float
    ) -> OrderResult:
        """Place an order through the coordinated subsystem workflow."""
        if quantity <= 0 or amount <= 0:
            raise ValueError("Quantity and amount must be positive")

        if not self.inventory.reserve(item_id, quantity):
            return OrderResult(success=False, error=f"Insufficient inventory for '{item_id}'")

        if not self.payment.charge(customer_id, amount):
            self.inventory.release(item_id, quantity)
            return OrderResult(success=False, error="Payment processing failed")

        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        tracking = self.shipping.dispatch(customer_id, item_id, quantity)
        self.notification.send(customer_id, f"Order {order_id} confirmed. Tracking: {tracking}")

        return OrderResult(success=True, order_id=order_id, tracking_number=tracking)
