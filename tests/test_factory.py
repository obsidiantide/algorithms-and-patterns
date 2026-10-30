"""Unit tests for the Factory Pattern implementation."""
import pytest
from patterns.creational.factory import (
    EmailNotifier,
    NotificationFactory,
    Notifier,
    ObjectFactory,
    SMSNotifier,
)


def test_factory_register_and_create():
    factory: ObjectFactory[str] = ObjectFactory()
    factory.register("upper", lambda text: text.upper())
    assert len(factory) == 1 and "upper" in factory
    assert factory.registered_keys() == ["upper"]
    assert factory.create("upper", "hello") == "HELLO"


def test_factory_decorator_and_case_insensitivity():
    factory: ObjectFactory[int] = ObjectFactory()

    @factory.register_builder("  Answer  ")
    def make_answer() -> int:
        return 42

    assert factory.is_registered("answer")
    assert factory.create("ANSWER") == 42


def test_factory_unregister():
    factory: ObjectFactory[int] = ObjectFactory()
    factory.register("val", lambda: 10)
    assert "val" in factory
    factory.unregister("val")
    assert "val" not in factory and len(factory) == 0


def test_factory_validation_errors():
    factory: ObjectFactory[str] = ObjectFactory()
    with pytest.raises(ValueError, match="Factory key must be non-empty"):
        factory.register("   ", lambda: "x")

    with pytest.raises(ValueError, match="Unknown factory key: 'missing'. Available: none"):
        factory.create("missing")


def test_notification_factory():
    factory = NotificationFactory()
    assert factory.registered_keys() == ["email", "sms"]

    email = factory.create("email")
    assert isinstance(email, EmailNotifier)
    assert email.send("alice@example.com", "Hi") == "Email sent to alice@example.com: Hi"

    sms = factory.create("sms")
    assert isinstance(sms, SMSNotifier)
    assert sms.send("12345", "Code") == "SMS sent to 12345: Code"
