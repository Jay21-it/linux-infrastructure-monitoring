# Installation Layout and Service Templates

These files are examples for planning a lab layout, not scripts that install the full software stack automatically. Review product-specific installation guidance and replace every documentation address and path with values for your own lab.

## Example roles

| Role | Components | Common ports |
|---|---|---|
| Monitoring server | Prometheus, Alertmanager, Grafana, webhook receiver, Zabbix Server/Frontend as needed | 9090, 9093, 3000, 5001, 10051 |
| Linux client | Node Exporter, optionally Zabbix Agent 2 | 9100, 10050 |

The actual port requirements depend on whether Zabbix Agent checks are active/passive, where Grafana runs, and which components share a host. Do not expose admin web UIs to the public internet.

## Service templates

The systemd directory contains templates for Prometheus, Alertmanager, and Node Exporter:

- prometheus.service.example
- alertmanager.service.example
- node_exporter.service.example

They use example documentation addresses from the TEST-NET ranges and will not work unchanged. Edit binary paths, configuration paths, data directories, service accounts, and listen addresses before installing. Run each service under its own unprivileged account and make sure directories are owned by that account.

For a target endpoint such as Node Exporter, allow TCP/9100 only from the authorized monitoring server or network. For Prometheus, Alertmanager, Grafana, and Zabbix, limit access to the management network. A loopback listener is appropriate only when all required callers share the same host/network namespace.

## Suggested bring-up order

1. Install and verify Node Exporter on the client.
2. Verify the client endpoint from the monitoring server.
3. Install Prometheus and validate its configuration/rules with promtool.
4. Confirm the Prometheus target is UP and useful metrics are queryable.
5. Install Alertmanager and validate receiver routing for Prometheus-managed alerts.
6. Configure the Grafana Prometheus data source and import the starter dashboard.
7. Add Grafana-managed alert rules and notification policies if required.
8. Configure the Zabbix trapper item/trigger before enabling the webhook-to-Zabbix path.
9. Install the webhook receiver and protect its token.
10. Test firing and recovery end to end, then capture sanitized evidence.

## Important limitations

- The service unit templates are not drop-in package units. Compare them with the unit files installed by your package manager.
- The example Alertmanager config assumes the receiver shares a host with Alertmanager and is reachable at loopback.
- The included receiver uses a numeric Zabbix item contract, which differs from the original lab's reported text key; see the walkthrough and Zabbix guide.
- A health check or syntax test is not an end-to-end validation.
