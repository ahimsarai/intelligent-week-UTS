import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import time

# Fungsi buat nada
def generate_tone(freq, duration=400, volume=-10):
    sample_rate = 44100
    t = np.linspace(0, duration / 1000, int(sample_rate * duration / 1000), False)
    tone = np.sin(freq * t * 2 * np.pi) * (2**15 - 1)
    tone = tone.astype(np.int16)
    audio = AudioSegment(
        tone.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )
    return audio + volume

# Nada
notes = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88,
}

# Lirik dan nada untuk setiap bait
lyrics_and_notes = [
    ("Sudah terbiasa terjadi tante", ['C', 'D', 'E', 'F']),
    ("Teman datang ketika lagi butuh saja", ['E', 'F', 'G', 'A']),
    ("Coba kalau lagi susah", ['F', 'E', 'D', 'C']),
    ("Mereka semua menghilang", ['G', 'A', 'F', 'E']),
]

# Main lagu bait per bait
for lyric, melody in lyrics_and_notes:
    print(f"\n🎤 {lyric}")
    bait = AudioSegment.silent(duration=300)
    for note in melody:
        bait += generate_tone(notes[note])
        bait += AudioSegment.silent(duration=100)
    play(bait)
    time.sleep(0.5)

print("\n✅ Lagu selesai diputar.")
