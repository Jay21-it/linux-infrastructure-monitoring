# Validation and Evidence Register

This file intentionally distinguishes previously reported results from items requiring direct evidence. Before claiming a test as complete in a CV, interview, or public repository, capture the evidence and update this register.

## Status definitions

- **Previously reported:** The project record says the test was observed, but the current public repository does not contain the raw evidence.
- **Pending evidence:** Must not be described as fully verified until the specified check is captured.
- **Not verified:** No successful test is recorded.

## Validation matrix

| ID | Test | Current status | Evidence to attach |
|---|---|---|---|
| V-01 | Prometheus config/rules validation | Previously reported as validated | Sanitized `promtool` output |
| V-02 | Node Exporter target healthy | Previously monitored | Targets page and `up` query |
| V-03 | Grafana Prometheus data source | Previously reported Save & test OK | Current Save & test screenshot |
| V-04 | Dashboard panels | Dashboard recorded as created | Screenshot with units/time range |
| V-05 | Grafana-managed rule fires | Previously observed in controlled lab test | Rule state, query result, timestamp |
| V-06 | Webhook receives real firing event | Previously observed in receiver logs | Sanitized receiver log |
| V-07 | `zabbix_sender` firing value | Previously reported `processed: 1; failed: 0` | Sanitized sender result |
| V-08 | Zabbix trigger opens as expected | Pending direct UI evidence | Latest data and Problems view |
| V-09 | Grafana returns to Normal after recovery | Recovery was reported in lab context; capture fresh evidence | Rule state and timestamps |
| V-10 | Zabbix problem clears after recovery | Pending direct end-to-end evidence | Before/after Problems and Latest data |
| V-11 | SMTP email notification | Not verified; earlier test encountered TLS/network issue | Successful delivery through approved relay |

## Evidence capture checklist

- [ ] Screenshot of Prometheus targets and `up` query.
- [ ] Screenshot of Grafana dashboard with readable units and time range.
- [ ] Screenshot of Grafana-managed alert rule and labels.
- [ ] Sanitized log showing actual firing notification received.
- [ ] Sanitized `zabbix_sender` result.
- [ ] Zabbix Latest data and Problems view showing alert active.
- [ ] Grafana rule returned to Normal after service recovery.
- [ ] Zabbix problem cleared after recovery.
- [ ] No internal IPs, customer names, secrets, or sensitive details in public evidence.

## Test report template

```text
Test ID:
Date/time and timezone:
Environment:
Preconditions:
Action performed:
Expected result:
Actual result:
Evidence file:
Status: Pass / Fail / Blocked
Notes and follow-up:
```

Do not mark a test as Passed until the acceptance criteria are met. Sender acceptance is not the same as trigger lifecycle validation.
