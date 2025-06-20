#!/usr/bin/env bash
# Install DeepSeek Browser Automation dependencies on Linux
set -e

if ! command -v python3 &> /dev/null; then
  echo "Python 3 is required" >&2
  exit 1
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

