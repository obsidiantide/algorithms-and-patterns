"""Observer Pattern implementation for state change notifications."""
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class Observer(ABC, Generic[T]):
    """Abstract base class for observers listening to Subject updates."""

    @abstractmethod
    def update(self, subject: "Subject[T]") -> None:
        """Receive update notification from the subject."""
        pass


class Subject(Generic[T]):
    """Subject that maintains a list of observers and notifies them of state changes."""

    def __init__(self, initial_state: T) -> None:
        self._state: T = initial_state
        self._observers: List[Observer[T]] = []

    @property
    def state(self) -> T:
        """Current state of the subject."""
        return self._state

    @state.setter
    def state(self, new_state: T) -> None:
        """Set a new state and notify all attached observers."""
        self._state = new_state
        self.notify()

    def attach(self, observer: Observer[T]) -> None:
        """Attach an observer if not already registered."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer[T]) -> None:
        """Detach an observer if currently registered."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers of the current state."""
        for observer in list(self._observers):
            observer.update(self)

    def __len__(self) -> int:
        """Return the count of attached observers."""
        return len(self._observers)


class HistoryObserver(Observer[T]):
    """Concrete observer that records the sequence of observed states."""

    def __init__(self) -> None:
        self.history: List[T] = []

    def update(self, subject: Subject[T]) -> None:
        """Append the current subject state to history."""
        self.history.append(subject.state)
