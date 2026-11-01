"""Decorator Pattern implementation for dynamically extending object behaviors."""
from __future__ import annotations

from abc import ABC, abstractmethod
import base64
import zlib


class DataSource(ABC):
    """Component interface defining read and write operations."""

    @abstractmethod
    def write_data(self, data: str) -> None:
        """Write string data to the source."""

    @abstractmethod
    def read_data(self) -> str:
        """Read and return string data from the source."""


class MemoryDataSource(DataSource):
    """Concrete component storing data in memory."""

    def __init__(self, initial_data: str = "") -> None:
        self._data: str = initial_data

    @property
    def data(self) -> str:
        """Return the raw stored data."""
        return self._data

    def write_data(self, data: str) -> None:
        self._data = data

    def read_data(self) -> str:
        return self._data


class DataSourceDecorator(DataSource):
    """Base decorator delegating operations to the wrapped component."""

    def __init__(self, wrappee: DataSource) -> None:
        self._wrappee = wrappee

    @property
    def wrappee(self) -> DataSource:
        """Return the wrapped component."""
        return self._wrappee

    def write_data(self, data: str) -> None:
        self._wrappee.write_data(data)

    def read_data(self) -> str:
        return self._wrappee.read_data()


class Base64Decorator(DataSourceDecorator):
    """Decorator encoding data in Base64 on write and decoding on read."""

    def write_data(self, data: str) -> None:
        encoded = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        super().write_data(encoded)

    def read_data(self) -> str:
        raw = super().read_data()
        if not raw:
            return ""
        return base64.b64decode(raw.encode("utf-8")).decode("utf-8")


class CompressionDecorator(DataSourceDecorator):
    """Decorator compressing data with zlib on write and decompressing on read."""

    def write_data(self, data: str) -> None:
        compressed = zlib.compress(data.encode("utf-8")).hex()
        super().write_data(compressed)

    def read_data(self) -> str:
        raw = super().read_data()
        if not raw:
            return ""
        return zlib.decompress(bytes.fromhex(raw)).decode("utf-8")


class EncryptionDecorator(DataSourceDecorator):
    """Decorator applying symmetric XOR obfuscation on write and reversal on read."""

    def __init__(self, wrappee: DataSource, key: int = 42) -> None:
        super().__init__(wrappee)
        if not (0 <= key <= 255):
            raise ValueError("Key must be between 0 and 255")
        self.key = key

    def _transform(self, text: str) -> str:
        return "".join(chr(ord(c) ^ self.key) for c in text)

    def write_data(self, data: str) -> None:
        super().write_data(self._transform(data))

    def read_data(self) -> str:
        raw = super().read_data()
        return self._transform(raw)
