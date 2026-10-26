# Grafana-managed service alert example

## Intended query pattern

With Node Exporter's systemd collector enabled, first inspect the series:

```promql
node_systemd_unit_state{
  name="httpd.service",
  state="active"
}
```

For an inactive-service alert, validate actual series behavior when the unit stops. Depending on collector behavior and labels, the series may become zero or disappear. Do not assume `== 0` catches a missing series.

## Suggested rule design checklist

- Rule type: Grafana-managed, if using Grafana contact points/policies.
- Query: verified against live metrics.
- Evaluation interval and pending duration: chosen for the service's needs.
- No Data / Error handling: explicitly reviewed.
- Labels: include severity and service; match notification policy.
- Contact point: test delivery.
- Real test: stop a lab service, observe firing, restore it, observe recovery.
- Zabbix: independently confirm the problem opens and clears.

The values above are a configuration checklist, not a claim that a public example has been applied to any specific Grafana version.
