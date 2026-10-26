# File Index

| Path | Purpose |
|---|---|
| README.md | Overview, architecture, repository navigation, security notes |
| docs/PROJECT_WALKTHROUGH.md | Narrative of how the lab was built |
| docs/ARCHITECTURE.md | Component roles, data flows, network boundaries |
| docs/IMPLEMENTATION.md | Setup and configuration workflow |
| docs/DASHBOARDS_AND_PROMQL.md | Metric and dashboard query examples |
| docs/ALERTING_AND_INTEGRATION.md | Alert engine distinction and notification paths |
| docs/OPERATIONS_RUNBOOK.md | Health checks and controlled testing |
| docs/TROUBLESHOOTING.md | Diagnostics from collection through Zabbix recovery |
| docs/REFERENCE_IMPLEMENTATION.md | Receiver install and numeric trapper contract |
| docs/VALIDATION.md | Evidence and validation matrix |
| docs/SECURITY.md | Public repository hygiene |
| docs/CV_BULLETS.md | Resume descriptions and interview prompts |
| prometheus/ | Sanitized scrape config and example rules |
| alertmanager/ | Webhook route example |
| grafana/dashboards/ | Importable starter dashboard JSON |
| webhook/receiver.py | Standard-library webhook bridge |
| webhook/monitoring-webhook.service | Receiver systemd unit |
| webhook/monitoring-webhook.env.example | Example settings without a real token |
| scripts/ | Installer, validators, smoke test, hygiene check |
| tests/ | Unit tests for payload-state mapping |
| .github/workflows/validate.yml | Automated syntax and unit checks |
| zabbix/ | Trapper item and trigger/recovery guide |
| evidence/README.md | Sanitized evidence capture checklist |
