#!/bin/bash
set -e

# Fix workspace ownership if needed (node has sudo for this)
if [ ! -w /workspace ]; then
    sudo /bin/chown -R node:node /workspace 2>/dev/null || true
fi

# Execute the CMD passed to the container (or default to jupyter lab)
if [ $# -eq 0 ]; then
    exec jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
else
    exec "$@"
fi