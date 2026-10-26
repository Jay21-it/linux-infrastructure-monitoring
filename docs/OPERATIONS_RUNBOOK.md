# Operations Runbook

## Daily health checks

~~~bash
sudo systemctl status prometheus --no-pager
sudo systemctl status alertmanager --no-pager
sudo systemctl status grafana-server --no-pager
sudo systemctl status monitoring-webhook.service --no-pager
~~~

Check logs:

~~~bash
sudo journalctl -u prometheus --since "30 minutes ago" --no-pager
sudo journalctl -u alertmanager --since "30 minutes ago" --no-pager
sudo journalctl -u grafana-server --since "30 minutes ago" --no-pager
sudo journalctl -u monitoring-webhook.service --since "30 minutes ago" --no-pager
~~~

## Controlled alert test

Use only a disposable lab service or approved maintenance window. Stopping a service can disrupt workloads.

1. Record baseline service state, dashboard, alert state, and Zabbix Problems.
2. Confirm the service is active.
3. Stop the test service.
4. Wait for scrape/evaluation/pending intervals and verify the rule fires.
5. Inspect notification routing and receiver logs.
6. Verify sender result, Zabbix latest item data, and expected problem.
7. Restore the service and wait for the source alert to resolve.
8. Verify the recovery event and confirm Zabbix clears the correct problem.
9. Capture timestamps and sanitized evidence.

## Webhook endpoint

~~~bash
curl -fsS http://127.0.0.1:5001/healthz
~~~

Health only proves the HTTP service responds; it does not validate token authentication, Zabbix connectivity, item existence, or recovery.

## Troubleshooting matrix

| Symptom | First checks |
|---|---|
| Grafana unavailable | systemd status, logs, port, config |
| Data source fails | Prometheus health, URL, reachability |
| Target down | targets page, exporter service, firewall |
| Panel shows No data | time range, metric name, labels, query inspector |
| Alert never fires | rule type, query result, pending period |
| No notification | policy matchers, contact point, silences, delivery logs |
| Receiver receives but Zabbix not updated | payload, sender args, host/item key |
| Zabbix problem does not clear | resolved value, item data, trigger expression |
| SMTP fails | approved relay, TLS, network access |

## Change procedure

Back up, make one logical change, validate syntax, apply through the supported reload/restart path, run targeted tests, and record rollback steps.
