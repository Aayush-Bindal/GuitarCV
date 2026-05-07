# GuitarCV

A real-time hand-tracked guitar simulator inspired by the guitar mechanic in The Last of Us Part II. Play guitar chords using only your hands and a webcam — no controller required.

Built with Python, OpenCV, and MediaPipe.

---

## How It Works

Your left hand selects a chord from a six-segment wheel displayed on screen. The direction your index finger points — calculated from wrist to fingertip — maps to one of six chords arranged in a circle. Your right hand strums by sweeping vertically across the string area on the right side of the screen. When a strum is detected, the active chord plays instantly.

If no chord is selected and you strum, an open guitar strum plays.

---

## Controls

| Action | Gesture |
|---|---|
| Select chord | Point left index finger in direction of chord on wheel |
| Strum | Sweep right hand up or down over the string area |
| Open strum | Strum with no chord selected |
| Quit | Press Q |

---

## Chord Wheel Layout

Six chords arranged clockwise starting from the 9-11 o'clock position:

C, G, Am, Em, F, D

These chords are all in the key of C major and are guaranteed to sound musical together regardless of the order you play them.

---

## Project Structure

```
GuitarCV/
├── main.py          # Webcam loop and application entry point
├── hands.py         # MediaPipe hand detection and landmark reading
├── wheel.py         # Chord wheel rendering and active segment detection
├── strings.py       # Guitar string rendering and strum detection
├── sound.py         # Audio loading and playback engine
├── config.py        # All constants, colors, sizes, and chord definitions
└── assets/
    ├── base.png              # Base wheel image
    ├── glow.png              # Glow overlay for active segment
    └── sounds/
        ├── C.wav
        ├── G.wav
        ├── Am.wav
        ├── Em.wav
        ├── F.wav
        ├── D.wav
        └── Open.wav
```

---

## Setup

Requires Python 3.10 or higher and uv for package management.

```bash
git clone https://github.com/yourusername/GuitarCV
cd GuitarCV
uv sync
uv run main.py
```

Dependencies are managed via uv and defined in pyproject.toml:
- opencv-python
- mediapipe
- pygame
- soundfile
- numpy

---

## Technical Details

**Hand Tracking** uses the MediaPipe HandLandmarker Tasks API — not the deprecated solutions.hands API. Detection runs at 720p resolution with confidence thresholds of 0.7 for detection, presence, and tracking.

**Chord Selection** is determined by the angle between the midpoint of the wrist and index knuckle, pointing toward the index fingertip. This vector is mapped to one of six 60-degree segments starting at 212 degrees in screen angle space.

**Strum Detection** tracks the vertical velocity of the right hand palm center across frames. A delta of 18px or more in a single frame triggers a strum, with a 400ms cooldown to prevent double triggering.

**Audio** files are pre-loaded at startup with a configurable offset to skip the silent lead-in present in recorded samples. All sounds are trimmed, converted to stereo int16, and held in memory as pygame Sound objects for low-latency playback.

**Rendering** runs at 1280x720. The chord wheel is composited from two PNG layers — a base wheel and a rotated glow overlay. Guitar strings are drawn procedurally with a glow pass and vibration animation on strum.

---

## Configuration

All tunable values live in `config.py`:

| Constant | Purpose |
|---|---|
| CHORDS | The six chord names, clockwise from segment 0 |
| SOUND_OFFSET_S | Seconds to skip at the start of each audio file |
| STRUM_THRESHOLD | Minimum hand movement in px to trigger a strum |
| STRUM_COOLDOWN_MS | Minimum time between strums in milliseconds |
| VIBRATION_DURATION_MS | How long string vibration animation lasts |
| WHEEL_DISPLAY_SIZE | Rendered size of the chord wheel in pixels |
| SEGMENT_0_CENTER_ANGLE | Angle of the first chord segment in screen degrees |

---

## Future Features

- Chord wheel customization — choose which chords appear on the wheel before playing
- Multiple wheel presets — switch between different chord sets mid-play
- Partial string strumming — detect which strings the right hand crosses for individual note plucking

---

## Credits

Chord wheel artwork designed in Canva.
Audio samples sourced from samplefocus.com kalcua.
Inspired by the guitar minigame in The Last of Us Part II by Naughty Dog.