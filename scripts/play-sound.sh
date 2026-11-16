#!/bin/sh
# Plays a sound for a Claude Code hook event.
# Usage: play-sound.sh <session-start|stop|notification|pre-compact>
#
# It never blocks Claude and never fails: the sound plays in the background
# and the script always exits 0.

event="$1"

# Claude sends the hook's JSON on stdin. Read it so the pipe closes cleanly.
cat >/dev/null 2>&1

# Mute with CLAUDE_SFX_MUTE=1, or by creating ~/.claude/sfx-muted
[ -n "$CLAUDE_SFX_MUTE" ] && exit 0
[ -f "$HOME/.claude/sfx-muted" ] && exit 0

case "$event" in
  session-start|stop|notification|pre-compact) ;;
  *) exit 0 ;;
esac

# Default: the "Portal" alert tone that ships with macOS
default="/System/Library/PrivateFrameworks/ToneLibrary.framework/Versions/A/Resources/AlertTones/EncoreInfinitum/Portal-EncoreInfinitum.caf"
# Fallback if a future macOS moves it
fallback="/System/Library/Sounds/Glass.aiff"

# Your own sound wins: ~/.claude/sounds/<event>.<ext>
file=""
for ext in aiff wav mp3 m4a caf m4r; do
  if [ -f "$HOME/.claude/sounds/$event.$ext" ]; then
    file="$HOME/.claude/sounds/$event.$ext"
    break
  fi
done
[ -z "$file" ] && [ -f "$default" ] && file="$default"
[ -z "$file" ] && file="$fallback"

[ -f "$file" ] || exit 0
command -v afplay >/dev/null 2>&1 || exit 0

volume="${CLAUDE_SFX_VOLUME:-1.0}"
afplay -v "$volume" "$file" >/dev/null 2>&1 &

exit 0
