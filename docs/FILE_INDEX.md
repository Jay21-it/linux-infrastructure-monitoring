# File Index

| Path | Purpose |
|---|---|
| README.md | Project overview, architecture, setup, and validation commands |
| docs/PROJECT_WALKTHROUGH.md | Narrative of how the lab was built |
| docs/INSTALLATION_LAYOUT.md | Roles, ports, service templates, bring-up order |
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
| prometheus/prometheus.example.yml | Sanitized Prometheus scrape configuration |
| prometheus/alerts.example.yml | CPU, memory, and scrape-availability rules |
| alertmanager/alertmanager.example.yml | Example webhook route |
| grafana/dashboards/linux-infrastructure-overview.json | Importable starter dashboard |
| grafana/grafana-alert-example.md | Grafana-managed alert guidance |
| webhook/receiver.py | Authenticated standard-library webhook bridge |
| webhook/monitoring-webhook.service | Hardened systemd service |
| webhook/monitoring-webhook.env.example | Non-secret environment template |
| webhook/integration-contract.md | Receiver payload and state contract |
| systemd/prometheus.service.example | Prometheus unit template; edit before use |
| systemd/alertmanager.service.example | Alertmanager unit template; edit before use |
| systemd/node_exporter.service.example | Node Exporter unit template; edit before use |
| scripts/install_webhook_receiver.sh | RHEL/Rocky installer for the receiver |
| scripts/validate_all.sh | Runs available code/config checks |
| scripts/validate_prometheus_examples.sh | Validates examples with promtool |
| scripts/smoke_test_webhook.sh | Guarded synthetic firing/recovery pair |
| scripts/check_repo_hygiene.sh | Heuristic credential/private-key scan |
| tests/test_receiver.py | Unit tests for payload status mapping |
| tests/README.md | Test execution instructions |
| .github/workflows/validate.yml | Automated CI checks |
| zabbix/trapper-integration.md | Trapper item and trigger/recovery guide |
| evidence/README.md | Sanitized evidence capture checklist |
