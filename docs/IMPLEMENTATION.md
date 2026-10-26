# Implementation Guide

This guide describes the implementation pattern. Commands and example files must be adapted to the installed versions and local service names.

## 1. Pre-flight checklist

- Confirm hostnames, static addresses/DNS, routing, and time synchronization.
- Decide which host runs each component.
- Confirm firewall rules only allow required source/destination pairs.
- Create a backup of existing configuration before changing it.
- Record versions and configuration locations in a private inventory.

## 2. Node Exporter

Install Node Exporter on the monitored Linux client using a trusted source and a dedicated unprivileged service account. Configure it with systemd and expose the metrics endpoint only to the monitoring network.

Validate on the client:

```bash
sudo systemctl status node_exporter --no-pager
sudo ss -lntp | grep ':9100'
curl -fsS http://127.0.0.1:9100/metrics | head
```

Service names may differ by installation method. Use the actual unit name in your environment.

## 3. Prometheus

Create a scrape job for the client endpoint and load the required rule files. The examples in `prometheus/` use documentation-only addresses and should be customized.

Validate before applying configuration:

```bash
promtool check config /etc/prometheus/prometheus.yml
promtool check rules /etc/prometheus/alerts.yml
sudo systemctl status prometheus --no-pager
```

Then open the Prometheus Targets page and verify the intended target is `UP`. A successful configuration parse does not prove that targets are reachable or metrics are correct.

## 4. Alertmanager

Configure routes and receivers deliberately. Verify which Prometheus alert labels should route to which destination. Review grouping, repeat intervals, silences, and inhibition rules to avoid notification storms.

```bash
sudo systemctl status alertmanager --no-pager
curl -fsS http://127.0.0.1:9093/-/healthy
```

Do not assume Grafana-managed alerts pass through Alertmanager; Grafana uses its own alerting engine and notification policies.

## 5. Grafana

Configure Prometheus as a data source using a URL reachable from the Grafana server process. When both run on the same host and namespace, `http://localhost:9090` may be suitable.

- Save and test the data source.
- Use Explore to validate metric names and labels.
- Build dashboard panels with correct units and meaningful legends.
- Configure alert rules with intentional evaluation, pending, No Data, and Error behavior.
- Add severity and service labels that match notification policy routing.

## 6. Zabbix and webhook integration

Create or verify the Zabbix host, trapper item, and trigger. The webhook receiver should validate payload shape and map notification states to a documented item value.

- Confirm `zabbix_sender` destination, host name, item key, and value type.
- Inspect receiver logs after a real alert.
- Verify the latest item value in Zabbix.
- Verify that the expected trigger opens.
- Test recovery and verify the problem clears.

`processed: 1; failed: 0` indicates the sender reports one value processed; it is not sufficient proof that the expected trigger lifecycle occurred.

## 7. Configuration management

- Keep sanitized example files under version control.
- Keep live credentials and production configurations outside the public repository.
- Validate YAML before reload/restart.
- Document each change, reason, test, result, and rollback plan.
