"""Unit tests for the Observer Pattern implementation."""
import pytest
from patterns.behavioral.observer import HistoryObserver, Observer, Subject


def test_cannot_instantiate_abstract_observer():
    with pytest.raises(TypeError):
        Observer()  # type: ignore[abstract]


def test_subject_initial_state():
    subject = Subject(42)
    assert subject.state == 42
    assert len(subject) == 0


def test_attach_and_detach():
    subject = Subject("initial")
    observer1 = HistoryObserver()
    observer2 = HistoryObserver()

    subject.attach(observer1)
    subject.attach(observer2)
    assert len(subject) == 2

    # Duplicate attach is idempotent
    subject.attach(observer1)
    assert len(subject) == 2

    subject.detach(observer1)
    assert len(subject) == 1

    # Detaching an unregistered observer is a no-op
    subject.detach(observer1)
    assert len(subject) == 1


def test_state_change_notifies_observers():
    subject = Subject("idle")
    obs1 = HistoryObserver()
    obs2 = HistoryObserver()

    subject.attach(obs1)
    subject.attach(obs2)

    subject.state = "running"
    subject.state = "completed"

    assert obs1.history == ["running", "completed"]
    assert obs2.history == ["running", "completed"]


def test_manual_notify():
    subject = Subject(10)
    obs = HistoryObserver()
    subject.attach(obs)

    subject.notify()
    assert obs.history == [10]


def test_custom_observer():
    class AlertObserver(Observer[str]):
        def __init__(self) -> None:
            self.alerts: list[str] = []

        def update(self, subject: Subject[str]) -> None:
            if "CRITICAL" in subject.state:
                self.alerts.append(subject.state)

    subject = Subject("INFO: all good")
    alert_obs = AlertObserver()
    subject.attach(alert_obs)

    subject.state = "WARN: memory usage"
    assert len(alert_obs.alerts) == 0

    subject.state = "CRITICAL: server unreachable"
    assert alert_obs.alerts == ["CRITICAL: server unreachable"]


def test_self_detaching_observer():
    class OneTimeObserver(Observer[int]):
        def __init__(self) -> None:
            self.triggered = 0

        def update(self, subject: Subject[int]) -> None:
            self.triggered += 1
            subject.detach(self)

    subject = Subject(0)
    one_time = OneTimeObserver()
    persistent = HistoryObserver()

    subject.attach(one_time)
    subject.attach(persistent)

    subject.state = 1
    assert one_time.triggered == 1
    assert len(subject) == 1

    subject.state = 2
    assert one_time.triggered == 1
    assert persistent.history == [1, 2]
