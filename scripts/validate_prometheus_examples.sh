#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PROMTOOL="$(printenv PROMTOOL || true)"
if [[ -z "$PROMTOOL" ]]; then PROMTOOL=promtool; fi
command -v "$PROMTOOL" >/dev/null || { echo "promtool not found; install a Prometheus release containing promtool." >&2; exit 127; }
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cp "$ROOT/prometheus/prometheus.example.yml" "$TMP/prometheus.example.yml"
cp "$ROOT/prometheus/alerts.example.yml" "$TMP/alerts.example.yml"
(cd "$TMP" && "$PROMTOOL" check config prometheus.example.yml && "$PROMTOOL" check rules alerts.example.yml)
echo "Prometheus example config and rules passed promtool validation."
