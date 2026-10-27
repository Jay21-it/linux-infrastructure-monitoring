# Validation and Evidence Register

This register separates tests previously reported in lab notes from checks requiring fresh evidence.

## Status definitions

- **Previously reported:** project notes say the test was observed; raw evidence is not included here.
- **Pending evidence:** do not claim it fully verified until the evidence is captured.
- **Not verified:** no successful test is recorded.

## Validation matrix

| ID | Test | Status | Evidence |
|---|---|---|---|
| V-01 | Prometheus config/rules validation | Previously reported validated | Sanitized promtool output |
| V-02 | Node Exporter target healthy | Previously monitored | Targets page and up query |
| V-03 | Grafana data source | Previously reported Save & test OK | Current screenshot |
| V-04 | Dashboard panels | Dashboard recorded as created | Screenshot with units/time range |
| V-05 | Grafana-managed rule fires | Previously observed in controlled test | Rule state, query, timestamp |
| V-06 | Webhook receives firing event | Previously observed in logs | Sanitized receiver log |
| V-07 | Sender firing value | Previously reported processed: 1; failed: 0 | Sanitized sender output |
| V-08 | Zabbix trigger opens | Pending direct UI evidence | Latest data and Problems |
| V-09 | Grafana rule recovers | Recovery reported; capture fresh evidence | Rule state and timestamps |
| V-10 | Zabbix problem clears | Pending direct end-to-end evidence | Before/after Problems and Latest data |
| V-11 | SMTP email | Not verified; earlier attempt hit TLS/network reset | Successful delivery through approved relay |

## Evidence checklist

- [ ] Prometheus Targets and up query.
- [ ] Grafana dashboard with readable units and time range.
- [ ] HTTPD active-state panel has data after enabling the Node Exporter systemd collector and including httpd.service.
- [ ] Grafana rule labels and firing state.
- [ ] Sanitized log showing a real firing notification.
- [ ] Sanitized zabbix_sender result.
- [ ] Zabbix Latest data and Problems showing the active event.
- [ ] Grafana rule returns to Normal after recovery.
- [ ] Zabbix problem clears after recovery.
- [ ] No internal IPs, secrets, customer names, or private details in public evidence.

## Repository checks

GitHub Actions runs Python syntax checks and unit/HTTP-handler tests, shell syntax checks, local Markdown-link checks, a repository hygiene heuristic, dashboard JSON validation, YAML parsing, `promtool check config`, `promtool check rules`, and `promtool test rules` cases for exporter-down, high-memory, and high-CPU alerts using a pinned Prometheus container. These checks do not prove compatibility with every installed product version or demonstrate the live Zabbix problem lifecycle.

~~~bash
python3 -m unittest discover -s tests -v
python3 -m py_compile webhook/receiver.py
bash -n scripts/*.sh
python3 -m json.tool grafana/dashboards/linux-infrastructure-overview.json >/dev/null
bash scripts/check_repo_hygiene.sh
bash scripts/validate_prometheus_examples.sh  # requires promtool; checks config, rules, and rule unit test
~~~

## Test report template

~~~text
Test ID:
Date/time and timezone:
Environment:
Preconditions:
Action:
Expected result:
Actual result:
Evidence:
Status: Pass / Fail / Blocked
Notes/follow-up:
~~~

Do not mark a test passed until acceptance criteria are met. Sender acceptance is not the same as trigger lifecycle validation.
