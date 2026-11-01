"""Adapter Pattern implementations allowing incompatible interfaces to work together."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Generic, TypeVar

T = TypeVar("T")


class Adapter(Generic[T]):
    """Generic object adapter that dynamically maps method calls to an adaptee."""

    def __init__(self, adaptee: T, **method_mappings: Callable[..., Any]) -> None:
        self._adaptee = adaptee
        self._mappings: Dict[str, Callable[..., Any]] = dict(method_mappings)

    @property
    def adaptee(self) -> T:
        """Return the wrapped adaptee object."""
        return self._adaptee

    def __getattr__(self, name: str) -> Any:
        """Delegate to mapped callable if registered; otherwise forward to adaptee."""
        if name in self._mappings:
            return self._mappings[name]
        return getattr(self._adaptee, name)


class PaymentProcessor(ABC):
    """Target interface expected by client payment workflows."""

    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> str:
        """Process a payment and return a confirmation message."""


class LegacyStripeGateway:
    """Legacy payment provider expecting amount in cents and currency code."""

    def charge(self, amount_in_cents: int, cur: str) -> str:
        return f"Stripe charge: {amount_in_cents} cents {cur.upper()}"


class LegacyPayPalGateway:
    """Legacy payment provider expecting formatted total string."""

    def send_payment(self, formatted_total: str) -> str:
        return f"PayPal sent: {formatted_total}"


class StripeAdapter(PaymentProcessor):
    """Adapts LegacyStripeGateway to the unified PaymentProcessor interface."""

    def __init__(self, stripe: LegacyStripeGateway) -> None:
        self._stripe = stripe

    def process_payment(self, amount: float, currency: str) -> str:
        cents = int(round(amount * 100))
        return self._stripe.charge(cents, currency)


class PayPalAdapter(PaymentProcessor):
    """Adapts LegacyPayPalGateway to the unified PaymentProcessor interface."""

    def __init__(self, paypal: LegacyPayPalGateway) -> None:
        self._paypal = paypal

    def process_payment(self, amount: float, currency: str) -> str:
        formatted = f"{currency.upper()}:{amount:.2f}"
        return self._paypal.send_payment(formatted)
