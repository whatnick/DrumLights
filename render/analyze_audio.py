"""Decode audio with Blender's aud and write per-frame loudness + spectral hue as JSON.
Run: blender -b -P analyze_audio.py -- <audio> <out.json> <fps> <start_s> <dur_s>
"""
import sys, json
import aud
import numpy as np

src, out, fps, start, dur = sys.argv[sys.argv.index("--") + 1:]
fps, start, dur = float(fps), float(start), float(dur)
SR = 22050

snd = aud.Sound(src).resample(SR, False).rechannel(1)
data = snd.data().astype(np.float32).reshape(-1)
total = len(data) / SR
print("duration_s", round(total, 2))
if dur <= 0:  # report only
    hop = int(SR)
    rms = [float(np.sqrt(np.mean(data[i:i + hop] ** 2))) for i in range(0, len(data) - hop, hop)]
    print("rms_per_s", [round(r, 3) for r in rms])
    sys.exit(0)

seg = data[int(start * SR):int((start + dur) * SR)]
n = int(dur * fps)
win = 2048
freqs = np.fft.rfftfreq(win, 1 / SR)
# Bands: low (drums/surdo) -> red, mid -> green, high (agogo/whistle/snare) -> blue
bands = [(30, 200), (200, 1500), (1500, 8000)]
env, bandE = [], []
for f in range(n):
    c = int((f + 0.5) / fps * SR)
    chunk = seg[max(0, c - win // 2):c + win // 2]
    if len(chunk) < win:
        chunk = np.pad(chunk, (0, win - len(chunk)))
    spec = np.abs(np.fft.rfft(chunk * np.hanning(win)))
    be = [float(np.sum(spec[(freqs >= lo) & (freqs < hi)] ** 2)) for lo, hi in bands]
    bandE.append(be)
    env.append(float(np.sqrt(np.mean(chunk ** 2))))
env = np.array(env)
bandE = np.array(bandE)
env = env / (np.percentile(env, 98) + 1e-9)
bandE = np.sqrt(bandE)
bandE = bandE / (bandE.max(axis=0) + 1e-9)
# Spectral centroid on log-frequency scale -> hue 0 (red, low) .. 0.75 (blue/violet, high)
cent = (bandE * np.array([0, 1, 2])).sum(1) / (bandE.sum(1) + 1e-9)  # 0..2
lo_c, hi_c = np.percentile(cent, 3), np.percentile(cent, 97)
hue = np.clip((cent - lo_c) / (hi_c - lo_c + 1e-9), 0, 1) * 0.75  # stretch to the clip's range
json.dump({"fps": fps, "start": start, "dur": dur, "env": np.clip(env, 0, 1.5).tolist(),
           "hue": hue.tolist(), "bands": bandE.tolist()}, open(out, "w"))
print("frames", n)
