#!/usr/bin/env bash
set -Eeuo pipefail
if [[ "$EUID" -ne 0 ]]; then echo "Run with sudo: sudo bash $0" >&2; exit 1; fi
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
SOURCE="$ROOT/webhook/receiver.py"
UNIT_SOURCE="$ROOT/webhook/monitoring-webhook.service"
for f in "$SOURCE" "$UNIT_SOURCE"; do [[ -f "$f" ]] || { echo "Missing source file: $f" >&2; exit 1; }; done
for cmd in python3 systemctl curl zabbix_sender; do command -v "$cmd" >/dev/null || { echo "Required command missing: $cmd" >&2; exit 1; }; done
if ! id monitoring-webhook >/dev/null 2>&1; then useradd --system --no-create-home --shell /sbin/nologin monitoring-webhook; fi
install -d -o root -g root -m 0755 /opt/monitoring-webhook
install -o root -g root -m 0755 "$SOURCE" /opt/monitoring-webhook/receiver.py
install -o root -g root -m 0644 "$UNIT_SOURCE" /etc/systemd/system/monitoring-webhook.service
if [[ ! -e /etc/monitoring-webhook.env ]]; then
  TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
  cat > /etc/monitoring-webhook.env <<EOF
WEBHOOK_TOKEN=$TOKEN
WEBHOOK_LISTEN_HOST=127.0.0.1
WEBHOOK_LISTEN_PORT=5001
MAX_BODY_BYTES=1048576
LOG_LEVEL=INFO
ZABBIX_SERVER_ADDR=127.0.0.1
ZABBIX_SERVER_PORT=10051
ZABBIX_HOST=linux-client01
ZABBIX_ITEM_KEY=prometheus.alert.state
ZABBIX_SENDER_BIN=$(command -v zabbix_sender)
EOF
  chown root:monitoring-webhook /etc/monitoring-webhook.env
  chmod 0640 /etc/monitoring-webhook.env
  printf '%s' "$TOKEN" > /etc/monitoring-webhook-token
  if getent group alertmanager >/dev/null 2>&1; then
    chown root:alertmanager /etc/monitoring-webhook-token
    chmod 0640 /etc/monitoring-webhook-token
  else
    chmod 0600 /etc/monitoring-webhook-token
    echo "WARNING: configure safe read access for the Alertmanager service account before using its example config." >&2
  fi
else
  echo "Keeping existing /etc/monitoring-webhook.env; it was not overwritten."
fi
systemctl daemon-reload
systemctl enable --now monitoring-webhook.service
sleep 1
if ! systemctl is-active --quiet monitoring-webhook.service; then
  systemctl --no-pager --full status monitoring-webhook.service || true
  echo "Receiver did not start. Review journalctl -u monitoring-webhook.service" >&2
  exit 1
fi
curl --fail --silent --show-error http://127.0.0.1:5001/healthz
printf '\nReceiver installed and health check passed.\n'
echo "Review /etc/monitoring-webhook.env for Zabbix host, item key, and address."
echo "Configure alerting with a Bearer token matching WEBHOOK_TOKEN."
echo "Create a matching numeric Zabbix trapper item before sending test alerts."
