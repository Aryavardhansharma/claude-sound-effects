# Changelog

## Unreleased

- Added a plugin icon (`.claude-plugin/icon.png`) and the script that draws it (`assets/make_icon.py`).

## 0.1.0 (2026-11-17)

First release.

- Plays the macOS Portal alert tone when Claude finishes, needs your attention, starts a new session, or is about to compact.
- Custom sounds per event from `~/.claude/sounds/<event>.<ext>`.
- Volume with `CLAUDE_SFX_VOLUME`; mute with `~/.claude/sfx-muted` or `CLAUDE_SFX_MUTE=1`.
- Falls back to `/System/Library/Sounds/Glass.aiff` if Portal isn't available.
