# Sources and scope

This standalone Claude Code adaptation draws on the B6 Code Engine in **kaomei/stickman-video-director**. It bundles the action, space and puppet helpers plus the selected direction references used by this workflow. The new entry point, skill routing, local voice performance, renderer, film art and episode are part of this adaptation. The original project's other style packs and showcase videos remain available in the pinned source.

- Upstream baseline: https://github.com/kaomei/stickman-video-director/tree/10287822ba47579321068da1b93801face9160dd
- The files in vendor/kaomei retain their original MIT license and attribution in vendor/kaomei/LICENSE. The renderer uses the upstream smooth interpolation in b6_space.py. b6_actions.py and b6_puppet.py are optional rigging tools for new episodes.
- Kokoro-82M by hexgrad: https://huggingface.co/hexgrad/Kokoro-82M . Model license: Apache 2.0; see licenses/Apache-2.0.txt. Voice list and model credits: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
- Bundled int8 ONNX model and voice data: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 . The hashes used by setup_studio.py pin the exact downloaded files. The kokoro-onnx Python runtime is installed during setup.
- Archivo Black by Omnibus-Type: https://github.com/google/fonts/tree/main/ofl/archivoblack . Original font file and SIL Open Font License are in fonts/.
- FFmpeg: https://ffmpeg.org/ . imageio-ffmpeg: https://github.com/imageio/imageio-ffmpeg . Python wheels are resolved for the host OS during setup.
- Claude Code project skills: https://code.claude.com/docs/en/skills .
