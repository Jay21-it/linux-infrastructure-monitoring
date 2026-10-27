# Live Lab Validation Checklist

Use this checklist in your own authorized RHEL/Rocky Linux lab. The addresses below are documentation placeholders; substitute the addresses used in your private lab. Do not commit private IPs or internal hostnames to this public repository.

## 0. Safety and baseline

- [ ] Confirm this is a lab/test service and stopping httpd will not interrupt a real workload.
- [ ] Note the date/time, alert rule name, host name, and current alert state.
- [ ] Capture a sanitized baseline dashboard screenshot.
- [ ] Confirm the existing Zabbix item key and trigger expression before testing. The recorded original lab used prometheus.alert; the separate reference receiver in this repository uses prometheus.alert.state.

## 1. Read-only health checks

Run on the monitoring server. Replace documentation addresses with the actual private values in your own environment.

~~~bash
export PROMETHEUS_URL="http://192.0.2.10:9090"
export ALERTMANAGER_URL="http://192.0.2.10:9093"
export GRAFANA_URL="http://192.0.2.10:3000"
export CLIENT_METRICS_URL="http://192.0.2.20:9100"

curl -fsS "$PROMETHEUS_URL/-/ready"
curl -fsS "$ALERTMANAGER_URL/-/ready"
curl -fsS "$GRAFANA_URL/api/health" | python3 -m json.tool
curl -fsS "$CLIENT_METRICS_URL/metrics" |
  grep -E '^node_(cpu_seconds_total|memory_MemAvailable_bytes|filesystem_avail_bytes|network_receive_bytes_total)' |
  sed -n '1,12p'
~~~

Expected: Prometheus and Alertmanager report readiness, Grafana returns healthy JSON, and Node Exporter exposes host metrics. If an endpoint fails, troubleshoot that component before the alert test.

Query Prometheus target health:

~~~bash
curl -fsSG --data-urlencode 'query=up{job="node"}' \
  "$PROMETHEUS_URL/api/v1/query" | python3 -m json.tool
~~~

Expected: a result for the client with value 1. If your scrape job uses another label, adjust the query to match the live configuration.

## 2. Check service units

On the monitoring server, adjust unit names if the lab uses a different package-provided name:

~~~bash
sudo systemctl --no-pager --full status \
  prometheus alertmanager grafana-server zabbix-server mariadb httpd
sudo systemctl --no-pager --full status alertmanager-webhook.service
~~~

On the client:

~~~bash
sudo systemctl --no-pager --full status node_exporter zabbix-agent2 httpd
~~~

A failed unit may be intentional only during the controlled service-down test. Record unexpected failures and inspect their journal logs before continuing.

## 3. Controlled firing test

Only do this if httpd is the intended disposable lab service.

On the Rocky Linux client console:

~~~bash
sudo systemctl stop httpd
sudo systemctl is-active httpd || true
~~~

Wait long enough for scraping, rule evaluation, and the pending period to elapse. In the recorded lab, the Grafana-managed rule used a 10-second evaluation interval and a 30-second pending period; allow at least 60 seconds as a practical first check.

Verify all layers:

1. In Grafana, confirm the intended rule becomes **Firing** and inspect its query/labels.
2. On the monitoring server, inspect the existing receiver service logs (the original lab unit was alertmanager-webhook.service):

   ~~~bash
   sudo journalctl -u alertmanager-webhook.service --since "10 minutes ago" --no-pager
   ~~~

3. Check whether the logs show the expected event and zabbix_sender result.
4. In Zabbix Monitoring → Latest data, confirm the intended item received a fresh value.
5. In Zabbix Monitoring → Problems, confirm the expected problem opened.

Do not treat processed: 1; failed: 0 as complete proof by itself; it does not prove the expected trigger was opened.

## 4. Recovery test

On the client console:

~~~bash
sudo systemctl start httpd
sudo systemctl is-active httpd
~~~

Wait for the next scrape/evaluation and recovery notification. Then verify:

- [ ] Grafana alert returns to **Normal**.
- [ ] Receiver logs show the resolved event.
- [ ] The intended Zabbix item receives the recovery value.
- [ ] The corresponding Zabbix problem clears.
- [ ] Recovery timestamps and state transitions are consistent.

If Grafana recovers but Zabbix remains in Problems, inspect the Zabbix item type and trigger/recovery expression. A trigger based only on a non-empty text item can stay active when the resolved payload is also non-empty.

## 5. Evidence to capture

Capture only what the test actually proves. Redact private IPs, hostnames, account names, tokens, and other sensitive details before committing evidence.

- [ ] Prometheus Targets page showing the client up.
- [ ] Grafana overview dashboard.
- [ ] Grafana rule showing Firing.
- [ ] Sanitized webhook receiver log for the firing notification.
- [ ] Sanitized zabbix_sender output.
- [ ] Zabbix Latest data and Problems showing the active event.
- [ ] Grafana rule returning to Normal.
- [ ] Zabbix problem clearing after recovery.

Store sanitized evidence in evidence/ and update docs/VALIDATION.md only after the corresponding check passes.

## Important distinction about the reference receiver

The receiver installer and smoke-test script in this repository implement a separate numeric-item contract using prometheus.alert.state (1 = firing, 0 = resolved). The originally recorded lab used prometheus.alert. Do not install the reference receiver on top of the working lab or run its smoke test against the original item unless you have intentionally configured a matching test item and trigger.
