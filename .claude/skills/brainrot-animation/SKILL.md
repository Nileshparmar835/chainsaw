---
name: brainrot-animation
description: Choose and implement topic-specific visual acting, character rigs, props, camera and speech-linked animation for a portrait comedy Short. Use when producing or repairing art.py.
---
# Animate the evidence for each punchline

Design the dominant silhouette and readable prop first. For each scene specify the set, foreground, background, cast, initial pose, direction of travel, contact pose, reaction, camera target and outgoing state. Give the opening a physical event on its first frames. Show the named object when the corresponding spoken cue begins. Split the line into beats at the reveal word when needed. Inspect the measured timeline after synthesis.

| Performance need | Technique |
|---|---|
| Slapstick or handoff | Anticipation, short fast travel, contact pose, impact hold, small recoil and settle. Bind the item to the active hand, then switch ownership at visible contact. |
| Deadpan accusation | Give the listener a delayed eye shift. Hold the camera when the tiny reaction carries the joke. |
| Gross-out or science gag | Cut from exterior to a distinct cross-section; retain position, color and scale cues to make the return readable. |
| Chaotic chase | Ground the feet, layer depth at different speeds, cut on action and keep travel direction consistent. |
| Receipt, timer or rule reveal | Insert framed close enough to read the decisive value; hold after it changes. |
| Object actor | Let balance, hinge motion, squash, rotation or a change of shape express intention. Maintain its identifiable outline. |

Write a fresh art.py with draw(canvas, q) for this episode. Translate the shot list into real drawing routines or locally created layers. Use q.id and the measured performance, animate the hero as well as the camera. The bundled ink.Canvas supplies resolution-independent primitives and camera transforms. For spatial staging use vendor/kaomei/b6_space.py. For fitted character handoffs consult b6-character-binding.md, b6-actions.md and b6_actions.py; the optional b6_puppet.py helper requires opencv-python-headless. Install that free package into .venv only when choosing its rig. Choose richer hand-drawn sprites or custom local rendering when they clarify the story.

Keep faces and meaningful gestures in the central action area; leave the caption strip centered at y=493 on the 360×640 design canvas. Extend background art across camera travel. Convey at least one purposeful change per beat. Read the draft contact sheet; inspect several surrounding decoded frames for any interaction. When animation and audio disagree, adjust the visual's timing or split and resynthesize that specific delivery. Preserve identity across cuts. Reference footage and its story belong outside the new film.
