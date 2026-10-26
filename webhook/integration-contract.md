# Webhook Integration Contract

The included receiver accepts common Alertmanager and Grafana webhook payloads and converts known states to numeric Zabbix trapper values.

| Input condition | Value | Meaning |
|---|---:|---|
| Alertmanager firing / Grafana alerting | 1 | Active/problem |
| All listed alerts resolved / Grafana OK | 0 | Recovery/normal |
| No Data, Error, malformed, unknown | No value | Reject and investigate |

The receiver sends one state to one configured item. Use this only for one alert stream or a deliberately aggregated condition. Independent concurrent alert streams need separate keys or an event-aware integration so one alert's recovery cannot clear another alert.

## Endpoints

- GET /healthz: simple process health response.
- POST /alertmanager: Alertmanager JSON webhook.
- POST /grafana: Grafana JSON webhook.
- POST /: compatibility endpoint.

## Security and reliability

- Bind to loopback by default.
- Require a bearer token for POST requests.
- Enforce JSON content type and a maximum request size.
- Never log payloads or authorization headers.
- Use subprocess arguments rather than shell interpolation.
- Reject unknown states rather than silently treating them as recovery.
