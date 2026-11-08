import sys

from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
segments, info = model.transcribe(sys.argv[1], vad_filter=True)
print(f"language: {info.language}, audio: {info.duration:.0f} s")
for s in segments:
    m, sec = divmod(int(s.start), 60)
    h, m = divmod(m, 60)
    print(f"[{h:02d}:{m:02d}:{sec:02d}] {s.text.strip()}")
