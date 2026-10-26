# Project Walkthrough: How the Lab Was Built

This narrative explains the implementation clearly for an interview. It separates previously reported lab tests from the additional reference files now provided in this repository.

## 1. Goal and design

The objective was to monitor Linux host health, visualize key metrics, detect important service failures, and trace alert delivery into Zabbix. The lab used a RHEL monitoring server and a Rocky Linux client. Private IPs, internal identifiers, credentials, and screenshots are intentionally not published.

The components have distinct responsibilities:

- **Node Exporter** exposes Linux host metrics.
- **Prometheus** scrapes and stores time series and evaluates Prometheus-managed rules.
- **Grafana** visualizes metrics and independently evaluates Grafana-managed alert rules.
- **Alertmanager** groups and routes Prometheus-managed alerts.
- **Python webhook receiver** accepts selected notifications and calls zabbix_sender.
- **Zabbix** stores a submitted item value and evaluates the associated trigger.

Grafana-managed rules use Grafana notification policies/contact points; they do not automatically pass through Alertmanager.

## 2. Metrics collection

Node Exporter was installed on the client and exposed its metrics endpoint to the monitoring server. Prometheus was configured to scrape at a 15-second interval in the original lab notes. The Prometheus Targets page and this query are first-line checks:

~~~promql
up{job="node"}
~~~

A value of 1 means the latest scrape succeeded; it does not prove the application itself is healthy.

## 3. Rules and dashboard

Prometheus rules were used for host-level conditions such as high CPU/memory and exporter availability. Grafana panels documented CPU, memory, root filesystem utilization, load, network throughput, availability, and service state.

A Grafana-managed rule named **ImportantLinuxServiceNotActive** monitored **httpd.service** in the recorded lab, with a 10-second evaluation interval and 30-second pending duration. These are lab-specific settings, not universal defaults. Inspect the actual systemd collector series before relying on a service-state expression: a series may disappear rather than become zero when the service stops.

## 4. Notification paths

Prometheus-managed: Prometheus rules → Alertmanager route → webhook receiver.

Grafana-managed: Grafana alert rule → notification policy/contact point → webhook receiver.

A contact-point test verifies basic delivery only. A real functional test must cause the rule to fire and confirm the notification path selected by the actual rule labels.

## 5. Webhook-to-Zabbix integration

The recorded lab receiver was a Python systemd service that invoked zabbix_sender. The original integration was reported to use the Zabbix trapper key **prometheus.alert**; a sender result of **processed: 1; failed: 0** was observed during a controlled test.

This repository also includes a **reference receiver** using numeric state values (1 firing, 0 resolved) and item key **prometheus.alert.state**. This is an explicit reference design, not a claim that the original lab item used the new key. A matching numeric trapper item and trigger are required for this reference implementation.

A positive sender summary proves the sender reports a value processed; it does not prove the intended Zabbix trigger opened and later cleared. Confirm both transitions in Latest data and Problems.

## 6. Repeatable validation sequence

1. Validate Prometheus YAML/rules with promtool.
2. Confirm the Node Exporter target is up and the dashboard returns data.
3. Test alert expressions against live metrics.
4. Create a controlled condition on a disposable lab service.
5. Observe the alert move through pending to firing.
6. Confirm notification policy routing and receiver logs.
7. Confirm sender output and inspect Zabbix Latest data.
8. Confirm the expected Zabbix problem opens.
9. Restore the service and wait for alert recovery.
10. Confirm the recovery value arrives and the problem clears.
11. Save sanitized screenshots/logs and update the validation register.

The validation register distinguishes previously reported checks from checks needing fresh evidence. SMTP notification is not marked verified because the earlier attempt encountered a TLS/network reset.

## 7. Interview summary

> I built a Linux monitoring lab with Node Exporter, Prometheus, Grafana, Alertmanager, and Zabbix. I used PromQL for host metrics, built dashboards, tested a service-state alert, and traced notifications through a Python webhook receiver to zabbix_sender. I documented firing and recovery separately because sender acceptance alone is not proof that a Zabbix problem clears correctly.
