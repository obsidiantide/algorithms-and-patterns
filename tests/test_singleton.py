"""Unit tests for the Singleton Pattern implementation."""
import threading
from patterns.creational.singleton import SingletonMeta, singleton


def test_singleton_meta_basic():
    class Database(metaclass=SingletonMeta):
        def __init__(self, name: str = "default") -> None:
            self.name = name

    try:
        assert not Database.is_instantiated()
        db1, db2 = Database("primary"), Database("secondary")
        assert db1 is db2 and db1.name == "primary"
        assert Database.is_instantiated()
    finally:
        Database.clear()
        assert not Database.is_instantiated()


def test_singleton_meta_distinct_classes():
    class ServiceA(metaclass=SingletonMeta):
        pass

    class ServiceB(metaclass=SingletonMeta):
        pass

    try:
        assert ServiceA() is not ServiceB()
    finally:
        ServiceA.clear()
        ServiceB.clear()


def test_singleton_meta_thread_safety():
    class Registry(metaclass=SingletonMeta):
        pass

    instances: list[Registry] = []
    barrier = threading.Barrier(10)

    def worker():
        barrier.wait()
        instances.append(Registry())

    try:
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(instances) == 10 and all(i is instances[0] for i in instances)
    finally:
        Registry.clear()


def test_singleton_decorator_basic():
    @singleton
    class Config:
        VERSION = "1.0.0"

        def __init__(self, env: str = "prod") -> None:
            self.env = env

    try:
        assert not Config.is_instantiated() and Config.VERSION == "1.0.0"
        c1, c2 = Config("prod"), Config("dev")
        assert c1 is c2 and c1.env == "prod"
        assert Config.is_instantiated() and isinstance(c1, Config._wrapped)
    finally:
        Config.clear()
        assert not Config.is_instantiated()


def test_singleton_decorator_thread_safety():
    @singleton
    class Counter:
        pass

    instances: list[Counter] = []
    barrier = threading.Barrier(10)

    def worker():
        barrier.wait()
        instances.append(Counter())

    try:
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(instances) == 10 and all(i is instances[0] for i in instances)
    finally:
        Counter.clear()
