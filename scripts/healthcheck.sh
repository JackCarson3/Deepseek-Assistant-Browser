#!/usr/bin/env bash
# Basic health check script for container
python - <<'PY'
import sys
try:
    import psutil
except Exception as e:
    print(e)
    sys.exit(1)
print('ok')
PY

