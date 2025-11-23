from .base import EffectMode

class NoteOnEffect(EffectMode):
    name = "Note On Effect"
    description = "The note lights up when pressed and turns off when released."

    def __init__(self):
        super().__init__()
    
    def apply(self, notes_state: dict, frame_note_events: list) -> list:
        self.notes_to_render = {}
        for note_key in frame_note_events:
            note_data = notes_state.get(note_key, {})
            state = note_data["state"]

            if state == 1:  # note pressed
                color = note_data.get("color", (0, 0, 255, 0))
                self.notes_to_render[note_key] = color
            else:
                self.notes_to_render[note_key] = (0, 0, 0, 0)
