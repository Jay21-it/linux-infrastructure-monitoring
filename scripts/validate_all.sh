#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT"
echo "== Python syntax and unit tests =="
python3 -m py_compile webhook/receiver.py tests/test_receiver.py tests/test_http_receiver.py scripts/check_markdown_links.py
python3 -m unittest discover -s tests -v
echo "== Shell syntax =="
bash -n scripts/*.sh
echo "== Dashboard JSON =="
python3 -m json.tool grafana/dashboards/linux-infrastructure-overview.json >/dev/null
echo "Dashboard JSON syntax OK."
echo "== YAML syntax (requires PyYAML) =="
if python3 -c 'import yaml' >/dev/null 2>&1; then
  python3 - <<'PY'
import yaml
from pathlib import Path
for f in [Path("prometheus/prometheus.example.yml"), Path("prometheus/alerts.example.yml"), Path("alertmanager/alertmanager.example.yml"), Path("prometheus/alerts.test.yml")]:
    yaml.safe_load(f.read_text(encoding="utf-8"))
    print("YAML syntax OK:", f)
PY
else
  echo "SKIP: PyYAML not installed."
fi
echo "== Markdown link check =="
python3 scripts/check_markdown_links.py
echo "== Repository hygiene heuristic =="
bash scripts/check_repo_hygiene.sh
echo "== Prometheus tool validation =="
if command -v promtool >/dev/null 2>&1; then
  bash scripts/validate_prometheus_examples.sh
else
  echo "SKIP: promtool not installed. Run this step on a host with promtool."
fi
echo "All available local validations completed."
