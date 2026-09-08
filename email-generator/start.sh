#!/usr/bin/env bash
# Email Template Generator - macOS / Linux launcher
cd "$(dirname "$0")" || exit 1
echo "Starting Email Template Generator..."
if command -v python3 >/dev/null 2>&1; then
  python3 server.py
else
  python server.py
fi
