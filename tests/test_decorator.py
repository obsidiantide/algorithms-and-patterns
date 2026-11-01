"""Unit tests for the Decorator Pattern implementation."""
import pytest
from patterns.structural.decorator import (
    Base64Decorator,
    CompressionDecorator,
    DataSource,
    DataSourceDecorator,
    EncryptionDecorator,
    MemoryDataSource,
)


def test_cannot_instantiate_abstract_data_source():
    with pytest.raises(TypeError):
        DataSource()  # type: ignore[abstract]


def test_memory_data_source():
    source = MemoryDataSource("initial")
    assert source.read_data() == "initial"
    assert source.data == "initial"
    source.write_data("updated")
    assert source.read_data() == "updated"
    assert source.data == "updated"


def test_base_decorator_delegation():
    source = MemoryDataSource("hello")
    dec = DataSourceDecorator(source)
    assert dec.wrappee is source
    assert dec.read_data() == "hello"
    dec.write_data("world")
    assert dec.read_data() == "world"
    assert source.read_data() == "world"


def test_base64_decorator():
    source = MemoryDataSource()
    decorated = Base64Decorator(source)
    decorated.write_data("hello world")
    assert source.data != "hello world"
    assert decorated.read_data() == "hello world"


def test_compression_decorator():
    source = MemoryDataSource()
    decorated = CompressionDecorator(source)
    payload = "repeat_" * 50
    decorated.write_data(payload)
    assert source.data != payload
    assert len(source.data) < len(payload) * 2
    assert decorated.read_data() == payload


def test_encryption_decorator():
    source = MemoryDataSource()
    decorated = EncryptionDecorator(source, key=123)
    decorated.write_data("secret message")
    assert source.data != "secret message"
    assert decorated.read_data() == "secret message"

    with pytest.raises(ValueError, match="Key must be between 0 and 255"):
        EncryptionDecorator(source, key=300)


def test_stacked_decorators():
    source = MemoryDataSource()
    pipeline = Base64Decorator(CompressionDecorator(EncryptionDecorator(source, key=99)))
    message = "Decorator pattern allows dynamic behavior composition!"
    pipeline.write_data(message)

    assert source.data != message
    assert pipeline.read_data() == message


def test_empty_data_handling():
    source = MemoryDataSource()
    pipeline = CompressionDecorator(Base64Decorator(source))
    assert pipeline.read_data() == ""
