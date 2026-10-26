# Operations Runbook

## Daily health checks

```bash
sudo systemctl status prometheus --no-pager
sudo systemctl status alertmanager --no-pager
sudo systemctl status grafana-server --no-pager
sudo systemctl status alertmanager-webhook --no-pager
```

Check recent logs:

```bash
sudo journalctl -u prometheus --since "30 minutes ago" --no-pager
sudo journalctl -u alertmanager --since "30 minutes ago" --no-pager
sudo journalctl -u grafana-server --since "30 minutes ago" --no-pager
sudo journalctl -u alertmanager-webhook --since "30 minutes ago" --no-pager
```

Confirm listening ports only where the services are expected to listen:

```bash
sudo ss -lntp
```

## Controlled alert test

> Use only a disposable lab service or an approved maintenance window. Stopping a service can disrupt workloads.

1. Record baseline service state, dashboard, alert state, and Zabbix Problems.
2. Confirm the service is active.
3. Stop the test service.
4. Confirm the service is inactive and wait for scrape/evaluation/pending intervals.
5. Verify the correct rule fires.
6. Inspect the notification policy and receiver logs.
7. Verify sender result, Zabbix latest item data, and expected problem.
8. Restore the service.
9. Wait for fresh metrics and alert recovery.
10. Verify the resolved event and confirm Zabbix clears the correct problem.
11. Capture timestamps, sanitized screenshots, and test results.

## Troubleshooting matrix

| Symptom | First checks |
|---|---|
| Grafana unavailable | systemd status, logs, port, config |
| Data source fails | Prometheus health, configured URL, reachability |
| Target down | target page, Node Exporter service, firewall/network |
| Panel shows No data | time range, metric name, labels, query inspector |
| Alert never fires | rule type, query result, pending period, evaluation |
| No notification | policy matchers, contact point, silences, delivery logs |
| Receiver gets event but Zabbix not updated | payload parser, sender args, host/item key |
| Zabbix problem does not clear | resolved value, latest item data, trigger expression |
| SMTP fails | approved relay, TLS configuration, network access |

## Change procedure

1. Back up current configuration.
2. Make one logical change.
3. Validate configuration syntax.
4. Apply change using the supported reload/restart procedure.
5. Run a health check and targeted functional test.
6. Record outcome and rollback instructions.
