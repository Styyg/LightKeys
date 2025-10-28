from abc import ABC, abstractmethod
import logging

log = logging.getLogger("MOCK_MIDI")

class BaseListener(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class MockListener(BaseListener):
    def __init__(self, event_queue):
        log.warning("Mock MidiListener initialized.")

    def start(self):
        log.warning("Mock MidiListener started.")

    def stop(self):
        log.warning("Mock MidiListener stopped.")