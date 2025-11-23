from abc import ABC, abstractmethod
import logging

log = logging.getLogger("MOCK_STRIP")

class BaseStrip(ABC):

    @abstractmethod
    def set_led(self, index, color):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def clear(self):
        pass

class MockStrip(BaseStrip):
    def __init__(self):
        log.debug("Mock Strip initialized.")

    def set_led(self, index, color):
        pass

    def show(self):
        pass

    def clear(self):
        pass