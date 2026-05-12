#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_HOST="${AMANIPULSE_LOCAL_API_HOST:-127.0.0.1}"
API_PORT="${AMANIPULSE_LOCAL_API_PORT:-8000}"
API_URL="http://${API_HOST}:${API_PORT}"
SIM_NAME="${AMANIPULSE_SIMULATOR_NAME:-AmaniPulse iPhone 16 Pro Max}"
SIM_TYPE="${AMANIPULSE_SIMULATOR_TYPE:-com.apple.CoreSimulator.SimDeviceType.iPhone-16-Pro-Max}"
DERIVED_DATA="${AMANIPULSE_DERIVED_DATA:-${ROOT_DIR}/ios/build/DerivedDataLocalMVP}"
APP_BUNDLE="${DERIVED_DATA}/Build/Products/Debug-iphonesimulator/AmaniPulseCitizenApp.app"
LOG_DIR="${ROOT_DIR}/artifacts/local-mvp"
BACKEND_LOG="${LOG_DIR}/backend.log"
BACKEND_PID_FILE="${LOG_DIR}/backend.pid"
BUNDLE_ID="org.amanipulse.citizen"

need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

health_check() {
  python3 - "$API_URL" <<'PY'
import json
import sys
from urllib.error import URLError
from urllib.request import urlopen

url = f"{sys.argv[1].rstrip('/')}/v1/health"
try:
    with urlopen(url, timeout=2) as response:
        payload = json.loads(response.read().decode("utf-8"))
        raise SystemExit(0 if response.status == 200 and payload.get("status") == "ok" else 1)
except (OSError, URLError, json.JSONDecodeError):
    raise SystemExit(1)
PY
}

wait_for_api() {
  for _ in $(seq 1 40); do
    if health_check; then
      return 0
    fi
    sleep 0.5
  done

  echo "Local API did not become healthy. Backend log: ${BACKEND_LOG}" >&2
  exit 1
}

latest_ios_runtime() {
  xcrun simctl list runtimes available | awk '/iOS .*com.apple.CoreSimulator.SimRuntime.iOS-/ { runtime=$NF } END { print runtime }'
}

simulator_udid() {
  python3 - "$SIM_NAME" <<'PY'
import re
import subprocess
import sys

name = sys.argv[1]
result = subprocess.run(
    ["xcrun", "simctl", "list", "devices", "available"],
    check=True,
    capture_output=True,
    text=True,
)
for line in result.stdout.splitlines():
    if name in line:
        match = re.search(r"\(([0-9A-F-]{36})\)", line)
        if match:
            print(match.group(1))
            raise SystemExit(0)
raise SystemExit(1)
PY
}

start_backend_if_needed() {
  if health_check; then
    echo "Local API already healthy at ${API_URL}"
    return 0
  fi

  echo "Starting local AmaniPulse API at ${API_URL}"
  mkdir -p "$LOG_DIR"
  (
    cd "${ROOT_DIR}/backend"
    nohup uv run uvicorn app.main:app --host "$API_HOST" --port "$API_PORT" >"$BACKEND_LOG" 2>&1 &
    echo "$!" >"$BACKEND_PID_FILE"
  )
  wait_for_api
}

ensure_simulator() {
  local udid
  if udid="$(simulator_udid)"; then
    echo "$udid"
    return 0
  fi

  local runtime
  runtime="$(latest_ios_runtime)"
  if [[ -z "$runtime" ]]; then
    echo "No available iOS simulator runtime found." >&2
    exit 1
  fi

  xcrun simctl create "$SIM_NAME" "$SIM_TYPE" "$runtime"
}

need python3
need uv
need xcodebuild
need xcrun
need open

start_backend_if_needed

echo "Verifying local API endpoints"
python3 "${ROOT_DIR}/scripts/staging_smoke.py" "$API_URL"

echo "Building iPhone simulator app"
xcodebuild build \
  -project "${ROOT_DIR}/ios/AmaniPulseCitizenApp/AmaniPulseCitizenApp.xcodeproj" \
  -scheme AmaniPulseCitizenApp \
  -destination "generic/platform=iOS Simulator" \
  -derivedDataPath "$DERIVED_DATA" \
  CODE_SIGNING_ALLOWED=NO

UDID="$(ensure_simulator)"
echo "Using simulator ${SIM_NAME} (${UDID})"
xcrun simctl boot "$UDID" >/dev/null 2>&1 || true
xcrun simctl bootstatus "$UDID" -b

echo "Installing and launching AmaniPulse"
xcrun simctl install "$UDID" "$APP_BUNDLE"
open -a Simulator
SIMCTL_CHILD_AMANIPULSE_API_PROFILE=local \
  SIMCTL_CHILD_AMANIPULSE_API_BASE_URL="$API_URL" \
  xcrun simctl launch --terminate-running-process "$UDID" "$BUNDLE_ID"

cat <<EOF

Local MVP is running.
- API: ${API_URL}
- Simulator: ${SIM_NAME}
- Backend log: ${BACKEND_LOG}

To stop the local API later:
kill \$(cat "${BACKEND_PID_FILE}")
EOF
