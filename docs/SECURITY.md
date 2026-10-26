# Security and Public Repository Hygiene

## Before publishing

- Replace internal IPs, DNS names, private hostnames, customer names, and employer-specific identifiers.
- Never commit passwords, tokens, private keys, webhook secrets, session cookies, or database dumps.
- Remove secrets from terminal screenshots and logs.
- Check whether employer policies permit publishing project details, code, and screenshots.
- Publish only material you created or have explicit permission to share.
- Use `.gitignore` for local environment files and generated evidence.
- Prefer sanitized examples and placeholder values.

## Operational recommendations

- Restrict management UIs and metrics endpoints to authorized networks.
- Keep webhook receivers private and validate payload structure.
- Use least-privilege service accounts and restrictive file permissions.
- Back up configurations before upgrades.
- Define retention and recovery objectives for metric and alert data.
- Test both firing and recovery paths.
- Do not claim production readiness until security, availability, backup, and capacity requirements have been assessed.

## Public portfolio disclaimer

This repository is a sanitized, lab-oriented demonstration of monitoring concepts. It does not include credentials or claim to reproduce an employer's full production environment.
