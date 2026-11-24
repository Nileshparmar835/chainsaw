---
name: brainrot-voice
description: Direct expressive local Kokoro narration, character dialogue, bracket cues, captions, music and Foley for an animated Short. Use when scripting performances, casting speakers or checking the audio mix.
---
# Perform one thought per cue

Use am_michael for the English narrator unless the brief calls for another voice. Cast distinct local voices only when that distinction helps the joke. The included demo uses am_onyx and am_fenrir for supporting parts. A recurring character keeps its voice across scenes. The current English preset uses en-us. Use short clauses, contractions, concrete stress words, changes of pace and deliberate silence. Avoid putting a direction on every line.

| Mark | Performed result |
|---|---|
| [laughing] | Insert a voiced "Ha, ha!" at that position; give the following words a brighter pace. |
| [whispering] | Softer, slower speech with breath texture. |
| [shouting] | Faster, compressed, more forceful delivery. |
| [panicked], [excited] | Distinct faster pace/gain presets. |
| [deadpan] | Slower, restrained delivery. |
| [gasp], [sighing] | Insert a short breath or longer exhale, then apply the matching delivery. |
| [beat], [pause] | Add roughly 150 or 300 ms of silence at the exact position. |
| [normal] | Restore normal delivery for following words. |

Examples: `Hello[laughing] you actually paid the toaster?` and `[whispering] That's my signature. [pause] [panicked] Who signed it?` Tags are local stage directions. The parser removes the brackets and the renderer performs each resulting segment. Laughter is synthesized "ha, ha"; a breath is a shaped noise, and pace/gain provide the stylization. Write the line so it still feels expressive without an effect.

Synthesis leads the timeline. Use separate short lines when a second speaker interrupts; keep every tag-free phrase within two caption lines. Insert a short hold for a silent stare. SFX choices are none, thump, stamp, swish, ping, glitch, crunch. Use hit in [0,1) to position the effect in its beat; match visual contact to the same value. The original score ducks below speech. Set music to false for a joke that needs silence, or author a more fitting original motif in the project. Check the voice, music and Foley stems independently if the mix masks a line. Listen on available playback; when unavailable, record that limitation separately from the decode checks.
