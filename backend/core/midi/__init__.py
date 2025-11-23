import platform
if platform.machine().startswith("arm"):
    from .mido_listener import MidoListener
    MidiListener = MidoListener
else:
    from .listener import MockListener
    MidiListener = MockListener