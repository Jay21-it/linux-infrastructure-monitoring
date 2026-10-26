# Webhook Integration Contract

This document defines the behavior the receiver should implement; it is not a substitute for reviewing the actual receiver source code.

## Expected responsibilities

1. Accept POST requests from authorized alerting systems.
2. Validate content type and payload structure.
3. Parse alert identity, status, labels, and relevant metadata.
4. Map firing and resolved states to explicit Zabbix item values.
5. Invoke `zabbix_sender` safely without shell-injection risk.
6. Log enough context for troubleshooting without exposing secrets.
7. Return appropriate HTTP status codes and handle malformed payloads.

## State mapping

| Incoming status | Required behavior |
|---|---|
| firing | Send the documented active/firing value |
| resolved | Send the documented recovery value |
| test payload | Handle safely; do not mistake a test for a production incident |

## Reliability and security

- Authenticate or restrict sender access where possible.
- Apply request timeouts and input size limits.
- Avoid logging credentials or full sensitive payloads.
- Handle duplicate notifications idempotently where feasible.
- Monitor receiver service health.
- Test malformed payloads and both firing/recovery paths.
