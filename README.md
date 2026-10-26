# Linux Infrastructure Monitoring & Alert Integration

A portfolio project documenting a Linux monitoring lab built around **Prometheus, Node Exporter, Grafana, Alertmanager, a Python webhook receiver, and Zabbix**. This repository contains sanitized configuration examples, an importable dashboard, receiver source code, an installer, tests, an implementation walkthrough, and an evidence-based validation checklist.

> **Scope and disclosure:** This is a sanitized lab/portfolio reference. It avoids private IP addresses, credentials, and employer-confidential configuration. It distinguishes previously reported lab tests from checks still requiring direct evidence. Confirm authorization before publishing employer-owned details.

## What it demonstrates

- Linux metrics collection with Node Exporter and Prometheus.
- PromQL and Grafana dashboards for CPU, memory, filesystem, load, network, and scrape health.
- Different alert paths for Prometheus-managed and Grafana-managed rules.
- A Python webhook receiver that maps firing/recovery to a Zabbix trapper item via zabbix_sender.
- systemd deployment, bearer-token authentication, request limits, safe subprocess execution, unit tests, and validation automation.

## Architecture

~~~mermaid
flowchart LR
  A[Linux host] --> B[Node Exporter]
  B --> C[Prometheus]
  C --> D[Grafana dashboards]
  C --> E[Prometheus rules]
  E --> F[Alertmanager]
  D --> G[Grafana alert rules / policies]
  F --> H[Python webhook receiver]
  G --> H
  H --> I[zabbix_sender]
  I --> J[Zabbix trapper item]
  J --> K[Zabbix trigger/problem]
~~~

Prometheus-managed alerts route through Alertmanager. Grafana-managed alerts use Grafana's notification policies and contact points; the two paths are not interchangeable.

## Start here

| Need | Document |
|---|---|
| Full project story | [Project walkthrough](docs/PROJECT_WALKTHROUGH.md) |
| Architecture | [Architecture](docs/ARCHITECTURE.md) |
| Implementation sequence | [Implementation guide](docs/IMPLEMENTATION.md) |
| Dashboard / PromQL examples | [Dashboard queries](docs/DASHBOARDS_AND_PROMQL.md) |
| Alert routing | [Alerting and integration](docs/ALERTING_AND_INTEGRATION.md) |
| Receiver source and setup | [Reference implementation](docs/REFERENCE_IMPLEMENTATION.md) |
| Troubleshooting | [Troubleshooting](docs/TROUBLESHOOTING.md) |
| Validation and evidence | [Validation register](docs/VALIDATION.md) |
| CV bullets | [CV wording](docs/CV_BULLETS.md) |
| Complete file list | [File index](docs/FILE_INDEX.md) |

## Repository contents

- **prometheus/** — sanitized scrape configuration and alert rules.
- **alertmanager/** — example webhook route using a protected bearer-token file.
- **grafana/dashboards/** — importable starter dashboard JSON.
- **webhook/receiver.py** — standard-library webhook bridge.
- **webhook/monitoring-webhook.service** — systemd service unit.
- **scripts/** — installer, Prometheus validator, guarded smoke test, and repository hygiene check.
- **tests/** — webhook payload state unit tests.
- **.github/workflows/validate.yml** — automated syntax and unit checks.
- **docs/** — implementation narrative, operations, troubleshooting, security, and validation.

## Validate locally

Run from the repository root:

~~~bash
python3 -m unittest discover -s tests -v
python3 -m py_compile webhook/receiver.py
bash -n scripts/*.sh
python3 -m json.tool grafana/dashboards/linux-infrastructure-overview.json >/dev/null
bash scripts/check_repo_hygiene.sh
~~~

If promtool is installed:

~~~bash
bash scripts/validate_prometheus_examples.sh
~~~

To import the dashboard, select **Dashboards → New → Import** in Grafana, upload **grafana/dashboards/linux-infrastructure-overview.json**, and select your Prometheus data source. Confirm that the job label **node** and instance labels match your lab.

## Install the reference webhook (lab only)

On a RHEL/Rocky Linux host with Python 3, systemd, curl, and zabbix_sender:

~~~bash
sudo bash scripts/install_webhook_receiver.sh
~~~

This installer does not configure Grafana, Alertmanager, or Zabbix. Review the [reference implementation](docs/REFERENCE_IMPLEMENTATION.md) first and create a matching numeric Zabbix trapper item with key **prometheus.alert.state**.

The recorded original lab integration used a trapper key named **prometheus.alert**. The included source is a separate reference design using **prometheus.alert.state** with numeric values (1 = firing, 0 = resolved). Do not mix the contracts without matching changes to item type, key, and trigger.

## Validation caveat

A configuration file in Git is not proof it works with every software version or was applied successfully. A successful zabbix_sender result is not proof that the expected Zabbix problem opened and recovered. Verify both in Latest data and Problems. SMTP email is not marked verified in the project notes.

## Security

- Never commit secrets, tokens, private keys, or private configuration.
- Use a high-entropy token and restrict endpoint reachability.
- Keep the receiver on loopback unless a secured remote topology is intentionally configured.
- Validate configs against installed versions before applying them.
- Use synthetic tests only where generating a test problem is safe.
- Review [security guidance](docs/SECURITY.md) before adding screenshots or logs.

## Technologies

Linux (RHEL/Rocky Linux lab), Prometheus, Node Exporter, Grafana, Alertmanager, Zabbix, PromQL, Python, systemd, YAML, JSON, Bash, Git, GitHub Actions.

## License

No license has been selected for this repository yet. Until a license is added, do not assume others have permission to reuse or redistribute the project files.
