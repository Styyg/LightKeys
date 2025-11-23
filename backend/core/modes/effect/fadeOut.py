from .base import EffectMode
import time
import logging

log = logging.getLogger("EFFECT")

class FadeOutEffect(EffectMode):
    name = "Fade Out"
    description = "The note fades out after being released."
    min_fade_time = 0.1
    max_fade_time = 5.0
    schema = {
        "duration": {"type": "float", "min": min_fade_time, "max": max_fade_time}
    }

    def __init__(self, fade_time=0.5):
        super().__init__()
        self.fade_time = fade_time
        self.fading_notes = {}

    def apply(self, notes_state: dict, frame_note_events: list) -> list:
        now = time.monotonic()
        self._cleanup_notes_to_render()

        # add new notes to fading_notes
        for note_key in frame_note_events:
            note_data = notes_state.get(note_key, {})
            state = note_data["state"]

            if state == 1:  # note pressed
                self.fading_notes.pop(note_key, None)
                self.notes_to_render.pop(note_key, None)
                continue

            start_time = note_data["start_time"]
            color = note_data.get("color", (0, 0, 255, 0))

            # note released
            self.fading_notes[note_key] = {
                "start_time": start_time,
                "end_time": start_time + self.fade_time,
                "fade_value": 1.0,
                "color": color
            }

        # update fading notes
        fade_to_delete = []
        for note_key, note_data in self.fading_notes.items():
            elapsed = now - note_data["start_time"]
            factor = max(0, 1 - elapsed / self.fade_time)
            if factor <= 0:
                fade_to_delete.append(note_key)
                continue

            r, g, b, w = note_data["color"]
            self.notes_to_render[note_key] = (
                int(r * factor), 
                int(g * factor), 
                int(b * factor), 
                int(w * factor))
            
        for note in fade_to_delete:
            self.fading_notes.pop(note, None)
            self.notes_to_render[note] = (0, 0, 0, 0)
    
    def _cleanup_notes_to_render(self):
        notes_to_delete = []
        for note, color in self.notes_to_render.items():
            if color == (0, 0, 0, 0):
                notes_to_delete.append(note)
        
        for note in notes_to_delete:
            del self.notes_to_render[note]
