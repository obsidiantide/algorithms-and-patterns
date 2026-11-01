"""Unit tests for the Adapter Pattern implementation."""
import pytest
from patterns.structural.adapter import (
    Adapter,
    LegacyPayPalGateway,
    LegacyStripeGateway,
    PayPalAdapter,
    PaymentProcessor,
    StripeAdapter,
)


def test_stripe_adapter():
    gateway = LegacyStripeGateway()
    adapter = StripeAdapter(gateway)
    assert isinstance(adapter, PaymentProcessor)
    result = adapter.process_payment(49.99, "usd")
    assert result == "Stripe charge: 4999 cents USD"


def test_paypal_adapter():
    gateway = LegacyPayPalGateway()
    adapter = PayPalAdapter(gateway)
    assert isinstance(adapter, PaymentProcessor)
    result = adapter.process_payment(12.5, "eur")
    assert result == "PayPal sent: EUR:12.50"


def test_payment_processor_polymorphism():
    processors: list[PaymentProcessor] = [
        StripeAdapter(LegacyStripeGateway()),
        PayPalAdapter(LegacyPayPalGateway()),
    ]
    results = [p.process_payment(10.0, "usd") for p in processors]
    assert results == [
        "Stripe charge: 1000 cents USD",
        "PayPal sent: USD:10.00",
    ]


def test_generic_adapter_method_mapping():
    class Dog:
        def bark(self) -> str:
            return "woof"

        @property
        def legs(self) -> int:
            return 4

    dog = Dog()
    adapter = Adapter(dog, make_sound=dog.bark)

    assert adapter.adaptee is dog
    assert adapter.make_sound() == "woof"
    assert adapter.legs == 4
    assert adapter.bark() == "woof"


def test_generic_adapter_attribute_error():
    class Cat:
        def meow(self) -> str:
            return "meow"

    adapter = Adapter(Cat(), speak=lambda: "purr")
    assert adapter.speak() == "purr"
    with pytest.raises(AttributeError):
        _ = adapter.fly
