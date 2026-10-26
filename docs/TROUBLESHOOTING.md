# Troubleshooting Reference

## Collection path

1. Check exporter service and listener on the monitored host.
2. Check firewall/network access from Prometheus to the exporter.
3. Open Prometheus Targets and inspect scrape errors.
4. Query the metric directly and inspect labels.
5. Check dashboard time range, data source, and query inspector.

## Prometheus-managed alert path

1. Confirm the rule is loaded and the expression returns expected series.
2. Check pending/firing state in Prometheus.
3. Inspect Alertmanager alerts, route matchers, silences, and receiver status.
4. Inspect receiver logs using journalctl for monitoring-webhook.service.

## Grafana-managed alert path

1. Inspect rule evaluation and query data in Grafana.
2. Review No Data and Error separately from a real zero result.
3. Inspect labels and notification-policy matchers.
4. Check contact-point delivery, then run a real rule-triggered test.

## Receiver path

~~~bash
sudo systemctl status monitoring-webhook.service --no-pager
sudo journalctl -u monitoring-webhook.service --since '15 minutes ago' --no-pager
curl -fsS http://127.0.0.1:5001/healthz
~~~

A healthy endpoint only proves HTTP process health; it does not validate token authentication, sender connectivity, the trapper item, or trigger recovery.

## Zabbix path

1. Confirm server address/port, host name, item key, and value type.
2. Confirm the item is a Zabbix trapper item.
3. Check Latest data for a fresh value.
4. Inspect trigger and recovery expressions and the Problems view.
5. Verify firing and recovery in a controlled test.

## Recovery pitfall

A trigger based only on a non-empty text item may remain active if the resolved event is also non-empty. Define explicit firing/recovery values and test the full problem lifecycle.
