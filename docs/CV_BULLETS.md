# CV and Interview Summary

Use only statements that accurately reflect your contribution and that you can explain in an interview.

## Project title

**Linux Infrastructure Monitoring and Alert Integration**

## CV bullet options

- Built a lab-based Linux monitoring stack using Prometheus, Alertmanager, Grafana, Node Exporter, and Zabbix to observe host resources and selected systemd service states.
- Created Grafana dashboards for CPU, memory, filesystem utilization, host availability, load, and network throughput using PromQL.
- Configured and tested a Grafana-managed alert for Linux service availability and traced notification delivery through a Python webhook receiver and `zabbix_sender`.
- Documented monitoring operations, alert-routing differences, troubleshooting workflows, and end-to-end validation criteria.
- Investigated the distinction between successful sender processing and confirmation that a Zabbix trigger opens and clears correctly.

## Short portfolio description

Designed and documented a Linux monitoring and alerting lab that combines Prometheus, Alertmanager, Grafana, and Zabbix. The project demonstrates metrics collection, dashboarding, service-state alerting, webhook-based notification integration, troubleshooting, and structured validation.

## Interview talking points

Be prepared to explain:
- Why Prometheus and Grafana serve different roles.
- How scrape health differs from application/service health.
- The difference between Prometheus-managed and Grafana-managed alert rules.
- How notification labels route to contact points.
- How the webhook maps alert state to a Zabbix trapper item.
- What evidence proves a firing event and what additional evidence proves recovery.
- What remains incomplete and how you would close the gap.

Avoid claiming email notification or full Zabbix recovery unless you have direct successful evidence.
