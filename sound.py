import pygame
import soundfile as sf
import numpy as np
import config

def load_sounds():
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    sounds = {}
    
    # Load regular chords
    for chord in config.CHORDS:
        if chord:  # Skip empty chords
            _load_single_sound(sounds, chord, config.SOUND_OFFSET_S)
        
    # Load open strings sound
    _load_single_sound(sounds, config.OPEN_SOUND_NAME, config.OPEN_SOUND_OFFSET_S)
        
    return sounds

def _load_single_sound(sounds, name, offset_s):
    path = f"{config.SOUND_FOLDER}/{name}.wav"
    try:
        data, sr = sf.read(path)
        start_idx = int(offset_s * sr)
        data = data[start_idx:]
        if data.dtype in (np.float32, np.float64):
            data = np.int16(data * 32767)
        elif data.dtype != np.int16:
            data = data.astype(np.int16)
        if len(data.shape) == 1:
            data = np.column_stack((data, data))
        data = np.ascontiguousarray(data)
        snd = pygame.sndarray.make_sound(data)
        snd.set_volume(config.SOUND_VOLUME)
        sounds[name] = snd
    except Exception as e:
        print(f"Could not load {path}: {e}")

def play_chord(sounds, chord_name):
    if chord_name is None or chord_name == -1:
        return
    for snd in sounds.values():
        snd.stop()
    if chord_name in sounds:
        sounds[chord_name].play()
