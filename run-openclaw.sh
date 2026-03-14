#!/bin/bash
export HOME=/Users/hung-weichen/openclaw-local/.home
export XDG_CONFIG_HOME=/Users/hung-weichen/openclaw-local/.xdg-config
export XDG_CACHE_HOME=/Users/hung-weichen/openclaw-local/.xdg-cache
export XDG_STATE_HOME=/Users/hung-weichen/openclaw-local/.local-state

cd /Users/hung-weichen/openclaw-local
npx openclaw "$@"
