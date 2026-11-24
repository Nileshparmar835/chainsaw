# Episode interface

Each new episode lives in its own directory with episode.json and art.py. The example in examples/last-pizza is a complete pair. Create both from the user's topic.

| JSON field | Type and use |
|---|---|
| topic, title, route, hook, payoff | Strings identifying the brief, story approach and twist |
| music | Optional boolean, defaults to true |
| cast | Array of objects with unique id, role, design, voice, and optional lang (defaults to en-us). A silent character still has a continuity entry. |
| scenes | Ordered array of setting, camera and action strings, elements and cast arrays, and a nonempty beats array |
| beat.id | Unique string used by the drawing code |
| beat.speaker, beat.line | Cast id and expressive line. Split at reaction or reveal boundaries. Square-bracket tags are parsed by studio/sound.py. |
| beat.visual | What actually moves, where, why and how it ends |
| beat.sfx, beat.hit | Optional sound name and fractional time in the beat; zero is its start |
| beat.hold | Optional seconds to hold the picture after the line, defaults to 0.12, maximum 2 |

A minimal real beat:

```json
{"id":"tip","speaker":"Dex","line":"[whispering] The toaster wants a tip.","visual":"A till swings out of the crumb tray just as Dex reaches for the toast.","sfx":"ping","hit":0.35,"hold":0.18}
```

In art.py implement `draw(c, q)`. The renderer calls it once per frame. Canvas coordinates range from (0,0) to (360,640); drawing occurs directly at output resolution. Use c.box, c.oval, c.line, c.poly and c.text, or composite your own original Pillow layers using c.image. The default font is bundled. Inspect studio/ink.py for exact arguments. c.camera(zoom, focus, shake) moves subsequent drawing calls; the caption stage resets the camera. Persistent background layers can be cached per output size. Avoid mutable state that depends on previous renders.

| Field | Meaning |
|---|---|
| q.id, q.scene, q.beat | Beat id, zero-based scene index and beat index within the scene |
| q.t, q.local, q.scene_t | Seconds from movie start, beat start and scene start |
| q.u, q.scene_u | Normalized progress through beat and scene |
| q.direction | The original beat dictionary, including the sound hit fraction |
| smooth(start,end,t) | Upstream eased progress in [0,1], available from ink |

```python
from ink import smooth

def draw(c, q):
    c.box((0, 0, 360, 640), '#26415a', None)
    c.box((56, 250, 290, 352), '#e69552', r=17)
    v = smooth(0, .35, q.u)
    c.box((210, 288, 222 + 67*v, 320), '#f4c270', r=4)
    if v > .8:
        c.text((249, 304), 'TIP?', 15, '#221b28')
```

The short snippet illustrates one beat. Author specific scenes, casts and staging for a whole episode. The voice engine synthesizes each phrase separately, measures its duration, and uses those timings for picture, captions and mix. A tag in the middle of a line also creates a phrase boundary. Use a new beat to land a prop on the first syllable of a noun. Within a beat, SFX and animation can share a normalized hit time. This is phrase-level synchronization.

A run writes storyboard.md, timeline.json, captions.srt, voice.wav, foley.wav, music.wav, mix.wav, final.mp4, contact-sheet.jpg and qa.json. The MP4 adds loudness normalization to the premaster mix. A draft is 360×640 with the same frame rate and audio as the final. The project-local .cache/voice speeds up revisions. The final candidate is decoded and checked before replacing final.mp4. After any failed command, check the exit status and rerun before presenting an older output.
