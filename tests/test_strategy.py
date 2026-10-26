"""Unit tests for Strategy Pattern serialization implementations."""
import json
import pytest
from patterns.behavioral.strategy import (
    JSONStrategy,
    KeyValueStrategy,
    SerializationStrategy,
    SerializerContext,
)


def test_cannot_instantiate_abstract_strategy():
    with pytest.raises(TypeError):
        SerializationStrategy()  # type: ignore[abstract]


def test_json_strategy_serialization():
    strategy = JSONStrategy()
    data = {"name": "Alice", "role": "admin", "active": True}
    result = strategy.serialize(data)
    assert json.loads(result) == data
    assert result == json.dumps(data, indent=2)


def test_json_strategy_empty():
    strategy = JSONStrategy()
    assert strategy.serialize({}) == "{}"


def test_key_value_strategy_serialization():
    strategy = KeyValueStrategy()
    data = {"host": "localhost", "port": 8080}
    result = strategy.serialize(data)
    assert result == "host=localhost\nport=8080"


def test_key_value_strategy_empty():
    strategy = KeyValueStrategy()
    assert strategy.serialize({}) == ""


def test_serializer_context_export():
    context = SerializerContext(JSONStrategy())
    data = {"key": "value"}
    assert context.export(data) == json.dumps(data, indent=2)


def test_serializer_context_set_strategy():
    data = {"key": "value"}
    context = SerializerContext(JSONStrategy())
    assert context.export(data) == json.dumps(data, indent=2)

    context.set_strategy(KeyValueStrategy())
    assert context.export(data) == "key=value"


def test_custom_strategy_implementation():
    class CSVHeaderStrategy(SerializationStrategy):
        def serialize(self, data: dict) -> str:
            keys = ",".join(data.keys())
            values = ",".join(str(v) for v in data.values())
            return f"{keys}\n{values}"

    context = SerializerContext(CSVHeaderStrategy())
    result = context.export({"a": 1, "b": 2})
    assert result == "a,b\n1,2"
