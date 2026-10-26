#!/usr/bin/env bash
set -Eeuo pipefail
# This can open/close a Zabbix problem. Run only on a safe lab/test item.
if [[ "$(printenv ALLOW_TEST_ALERT || true)" != "YES" ]]; then
  echo "Refusing to send. Set ALLOW_TEST_ALERT=YES only for a safe lab/test item." >&2
  exit 2
fi
WEBHOOK_URL="$(printenv WEBHOOK_URL || true)"
WEBHOOK_TOKEN="$(printenv WEBHOOK_TOKEN || true)"
if [[ -z "$WEBHOOK_URL" ]]; then WEBHOOK_URL="http://127.0.0.1:5001/alertmanager"; fi
if [[ -z "$WEBHOOK_TOKEN" ]]; then echo "Set WEBHOOK_TOKEN from a protected local secret file." >&2; exit 2; fi
command -v curl >/dev/null || { echo "curl is required" >&2; exit 127; }
post() {
  local state="$1"
  curl --fail --silent --show-error \
    -H "Authorization: Bearer $WEBHOOK_TOKEN" \
    -H 'Content-Type: application/json' \
    --data "{\"receiver\":\"portfolio-smoke-test\",\"status\":\"$state\",\"alerts\":[{\"status\":\"$state\",\"labels\":{\"alertname\":\"PortfolioWebhookSmokeTest\",\"severity\":\"info\"}}]}" \
    "$WEBHOOK_URL"
  printf '\n'
}
echo "Sending test firing state; inspect the intended Zabbix item/problem."
post firing
echo "Sending test resolved state; confirm that same problem clears."
post resolved
echo "Pair sent; inspect Zabbix Latest data and Problems to confirm lifecycle."
