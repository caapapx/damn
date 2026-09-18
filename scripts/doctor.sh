#!/usr/bin/env bash
# damn toolchain doctor: probe → suggest → opt-in install → re-check.
# Never prints secret values. Default is probe-only (no install).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JSON=0
SUGGEST=0
INSTALL=""
WRITE_PROFILE=""
QUIET=0

usage() {
  cat <<'EOF'
Usage: bash scripts/doctor.sh [options]

  (default)     Probe required/optional tools; exit 0 if required_local ok
  --json        Machine-readable summary on stdout
  --suggest     Print install / login hints for missing optionals
  --install charts
                Opt-in: pip install matplotlib numpy (optional_export only)
  --write-profile PATH
                Write CapabilityProfile-like JSON (no secrets) to PATH
  --quiet       Less human chatter (still prints JSON if --json)

See references/toolchain-matrix.md
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON=1; shift ;;
    --suggest) SUGGEST=1; shift ;;
    --install)
      INSTALL="${2:-}"
      [[ -n "$INSTALL" ]] || { echo "error: --install needs charts" >&2; exit 2; }
      shift 2
      ;;
    --write-profile)
      WRITE_PROFILE="${2:-}"
      [[ -n "$WRITE_PROFILE" ]] || { echo "error: --write-profile needs PATH" >&2; exit 2; }
      shift 2
      ;;
    --quiet) QUIET=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

have_cmd() { command -v "$1" >/dev/null 2>&1; }

# key status: unset | set | invalid_shape (non-empty but suspiciously short)
key_status() {
  local name="$1" val="${!1-}"
  if [[ -z "${val}" ]]; then
    echo unset
  elif [[ ${#val} -lt 8 ]]; then
    echo invalid_shape
  else
    echo set
  fi
}

probe_python_mod() {
  python3 -c "import $1" >/dev/null 2>&1
}

log() { [[ "$QUIET" -eq 1 ]] || echo "$*"; }

# --- optional install (explicit only) ---
if [[ -n "$INSTALL" ]]; then
  case "$INSTALL" in
    charts)
      log "install: pip install matplotlib numpy"
      python3 -m pip install --user matplotlib numpy
      ;;
    *)
      echo "error: unsupported --install '$INSTALL' (only: charts)" >&2
      echo "hint: Agent Reach / search API keys are manual; see --suggest" >&2
      exit 2
      ;;
  esac
fi

# --- probes ---
PY=missing; have_cmd python3 && PY=ok
CURL=missing; have_cmd curl && CURL=ok
AR=missing
AR_DETAIL=""
if have_cmd agent-reach; then
  if OUT="$(agent-reach doctor --json 2>/dev/null)"; then
    AR=ok
    AR_DETAIL="doctor_json_ok"
  else
    AR=warn
    AR_DETAIL="binary_present_doctor_failed"
  fi
fi
GH=missing
GH_DETAIL=""
if have_cmd gh; then
  if gh auth status >/dev/null 2>&1; then
    GH=ok
    GH_DETAIL="authenticated"
  else
    GH=warn
    GH_DETAIL="installed_not_logged_in"
  fi
fi
FC=missing; have_cmd firecrawl && FC=ok
MPL=missing; [[ "$PY" == ok ]] && probe_python_mod matplotlib && probe_python_mod numpy && MPL=ok

BRAVE="$(key_status BRAVE_API_KEY)"
EXA="$(key_status EXA_API_KEY)"
TAVILY="$(key_status TAVILY_API_KEY)"
FCKEY="$(key_status FIRECRAWL_API_KEY)"

REQUIRED_OK=1
[[ "$PY" == ok && "$CURL" == ok ]] || REQUIRED_OK=0

TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

profile_json() {
  python3 - <<PY
import json
print(json.dumps({
  "skill": "damn",
  "probed_at": "$TS",
  "root": "$ROOT",
  "required_local": {
    "python3": "$PY",
    "curl": "$CURL",
  },
  "required_host": {
    "agent_runtime": "host_assumed",
    "web_search_or_fetch": "host_assumed",
  },
  "optional_enhance": {
    "agent_reach": {"status": "$AR", "detail": "$AR_DETAIL"},
    "gh": {"status": "$GH", "detail": "$GH_DETAIL"},
    "firecrawl_cli": "$FC",
    "keys": {
      "BRAVE_API_KEY": "$BRAVE",
      "EXA_API_KEY": "$EXA",
      "TAVILY_API_KEY": "$TAVILY",
      "FIRECRAWL_API_KEY": "$FCKEY",
    },
  },
  "optional_export": {
    "matplotlib_numpy": "$MPL",
  },
  "required_local_ok": bool($REQUIRED_OK),
  "policy": "probe_default_no_auto_install_no_secret_echo",
}, ensure_ascii=False, indent=2))
PY
}

SUMMARY="$(profile_json)"

if [[ -n "$WRITE_PROFILE" ]]; then
  mkdir -p "$(dirname "$WRITE_PROFILE")"
  printf '%s\n' "$SUMMARY" >"$WRITE_PROFILE"
  log "wrote profile: $WRITE_PROFILE"
fi

if [[ "$JSON" -eq 1 ]]; then
  printf '%s\n' "$SUMMARY"
else
  log "damn doctor @ $TS"
  log "required_local:  python3=$PY  curl=$CURL  → ok=$REQUIRED_OK"
  log "required_host:   agent_runtime=host_assumed  web=host_assumed"
  log "optional:        agent-reach=$AR ($AR_DETAIL)  gh=$GH ($GH_DETAIL)  firecrawl=$FC  charts=$MPL"
  log "keys (presence): BRAVE=$BRAVE EXA=$EXA TAVILY=$TAVILY FIRECRAWL=$FCKEY"
  log "matrix: $ROOT/references/toolchain-matrix.md"
fi

if [[ "$SUGGEST" -eq 1 ]]; then
  log ""
  log "suggestions (manual; damn will not run these unless you pass --install):"
  [[ "$PY" != ok ]] && log "  - install Python 3 (required_local)"
  [[ "$CURL" != ok ]] && log "  - install curl (required_local)"
  [[ "$AR" == missing ]] && log "  - install Agent Reach CLI, then: agent-reach doctor --json"
  [[ "$AR" == warn ]] && log "  - fix Agent Reach backends/login: agent-reach doctor --json"
  [[ "$GH" == missing ]] && log "  - brew install gh && gh auth login"
  [[ "$GH" == warn ]] && log "  - gh auth login"
  [[ "$FC" == missing ]] && log "  - install Firecrawl CLI if you want crawl/search adapters"
  [[ "$BRAVE" != set ]] && log "  - export BRAVE_API_KEY=…  (optional search adapter)"
  [[ "$EXA" != set ]] && log "  - export EXA_API_KEY=…  (optional)"
  [[ "$TAVILY" != set ]] && log "  - export TAVILY_API_KEY=…  (optional)"
  [[ "$FCKEY" != set && "$FC" == ok ]] && log "  - export FIRECRAWL_API_KEY=… or complete CLI login"
  [[ "$MPL" != ok ]] && log "  - bash scripts/doctor.sh --install charts"
  log "  - host MCP (GitHub/Firecrawl/…): Cursor Settings → MCP → authenticate"
fi

if [[ "$REQUIRED_OK" -ne 1 ]]; then
  [[ "$JSON" -eq 1 ]] || log "FAIL: required_local incomplete"
  exit 1
fi
[[ "$JSON" -eq 1 ]] || log "PASS: required_local ok (optionals may still be missing)"
exit 0
