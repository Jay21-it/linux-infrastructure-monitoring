# Alerting and Integration

## Two separate alert engines

### Prometheus-managed path

`Metrics → Prometheus rule evaluation → Alertmanager → configured receiver`

Prometheus evaluates rules in its rule files. Alertmanager groups, routes, silences, and delivers notifications.

### Grafana-managed path

`Prometheus data source → Grafana rule evaluation → notification policy → contact point → receiver`

Grafana evaluates its own alert rules and uses Grafana notification policies/contact points. Check the rule type before troubleshooting routing.

## Alert lifecycle

- **Normal:** condition is not firing.
- **Pending:** condition is true but its pending duration has not elapsed.
- **Firing:** firing criteria have been met.
- **Resolved/Normal:** condition is no longer firing; notification behavior depends on configuration.
- **No Data / Error:** evaluation did not return a usable normal result; handling is configuration-dependent.

## Recommended alert labels

Use stable labels such as:

```yaml
labels:
  severity: warning
  team: infrastructure
  service: httpd
```

Do not copy this example blindly into a live rule; ensure your notification policies match the exact labels.

## Grafana webhook contact point

A local URL such as `http://127.0.0.1:5001/` is appropriate only when Grafana and the receiver share the same host/network namespace. Otherwise use a reachable, access-controlled endpoint.

Test notifications are useful for basic connectivity but do not prove:
- the real alert rule fires,
- its labels match the policy,
- firing and resolved payloads are parsed correctly,
- the intended Zabbix trigger opens and clears.

## Webhook-to-Zabbix state contract

Define the state mapping explicitly before implementing it. Example conceptual contract:

| Notification state | Value sent to trapper item | Expected Zabbix behavior |
|---|---|---|
| Firing | A documented firing state/value | Trigger opens |
| Resolved | A distinct recovery state/value | Trigger clears |

The actual values and trigger expression must match the item type and Zabbix configuration. If the trigger is simply “latest value is non-empty,” a non-empty resolved message may keep the problem active. Validate in the Zabbix frontend.

## Troubleshooting order

1. Confirm alert rule type and actual state.
2. Inspect query evaluation and labels.
3. Verify notification policy match and silences/mute timings.
4. Inspect contact-point delivery result.
5. Inspect webhook receiver logs and payload state.
6. Check sender command result and target host/item key.
7. Verify Zabbix Latest data and Problems.
8. Restore the service and repeat recovery verification.
