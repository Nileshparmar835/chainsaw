# Brainrot Studio for Claude Code

Give Claude one topic. It chooses a story route, writes and performs the script, designs the characters and sets, animates each beat, mixes sound and delivers a captioned vertical MP4.

## Start on your computer

1. Extract the whole ZIP. Keep the **brainrot-studio** folder intact, including its hidden **.claude** folder, models and fonts.
2. Open a terminal in the folder that contains **CLAUDE.md**. Start `claude` using your existing Claude Code access.
3. Enter just a topic, for example **My alarm clock hired a lawyer to stop me pressing snooze**. You can explicitly run the same workflow with:

   ```text
   /brainrot My alarm clock hired a lawyer to stop me pressing snooze
   ```

Claude selects the project skills, runs first-time setup, authors original episode files, renders a draft, checks it and renders the final. Find it under **episodes/<topic-slug>/output/final.mp4**. The same folder includes the complete script with performance tags, scene-by-scene direction, SRT captions, audio stems and a contact sheet. The editable art and episode data sit one level above it.

## What you need

Use a desktop with Claude Code access and Python 3.11 or 3.12. The initial setup needs internet for Python packages. The ZIP already includes the free Kokoro voice model, voice library and caption font. The media pipeline runs on CPU. It needs no paid media API, key, GPU subscription or stock footage. Claude Code authentication, usage limits and any system permission dialogs are managed by your own installation.

If you want to prepare the environment yourself, use one command:

| System | Setup command | Example render after setup |
|---|---|---|
| Windows with Python 3.12 | `py -3.12 setup_studio.py` | `.\.venv\Scripts\python.exe studio/render.py examples/last-pizza` |
| macOS or Linux with Python 3.12 | `python3.12 setup_studio.py` | `.venv/bin/python studio/render.py examples/last-pizza` |

Use the equivalent 3.11 launcher when applicable. FFmpeg comes from your PATH or the imageio-ffmpeg Python wheel. Open the **project root** in Claude Code so its project skills resolve. The package can also be extracted into a separate working copy of the upstream repository; copy the contents of brainrot-studio, including .claude, into its root, and preserve any existing project instructions when combining CLAUDE.md.

## Try the included episode

Play **examples/last-pizza/output/final.mp4**. *The People v. One Hungry Guy* follows a slice of pizza, twelve garlic-knot jurors and an oven judge. Its **episode.json**, **art.py**, **storyboard.md**, timing, stems and contact sheet are included. It demonstrates six sets, three speaking voices, a stage-directed laugh and a callback. New topics get new scripts and original art.

## How creative choices work

| Director chooses | What the package does |
|---|---|
| The story | Selects object comedy, a trap, a countdown, an explanatory cutaway or another structure suited to the premise. Builds a hook, escalating consequences and a visual payoff. |
| The cast and scenes | Defines every character's role, silhouette, colors and voice, plus the location, camera, props, action and transition for each scene. |
| The animation | Authors a Python scene module for this story, times each beat against synthesized speech and draws at the final resolution. The example uses layered 2D art, poses, reactions and finite camera moves. |
| The performance | Interprets `Hello[laughing]`, `[whispering]`, `[panicked]`, `[gasp]`, pauses and other documented cues. Uses local voices, effects and timing to approximate delivery. |
| The tools | Runs the bundled story, animation and voice skills. Selects extra local skills when useful and can create a reusable project specialist for a recurring need. |
| The finish | Delivers a 1080×1920 H.264/AAC video at 30 fps, with burned-in phrase captions, original music and Foley. Runs a full decode and generates review frames. |

**Project guide:** studio/FORMAT.md. **Source and credits:** THIRD_PARTY.md.
