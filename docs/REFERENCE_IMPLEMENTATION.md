# Reference Implementation: Receiver and Zabbix State Item

The Python standard-library receiver accepts common Alertmanager/Grafana webhook shapes and converts firing/recovery to a numeric trapper state.

## State contract

- Firing / alerting: send numeric 1.
- Resolved / OK: send numeric 0.
- No Data, Error, malformed, or unknown states: reject without sending a value.

Create a Zabbix item with Type **Zabbix trapper**, key **prometheus.alert.state**, and information type **Numeric (unsigned)**. Create a trigger that opens when the latest value is 1 and recovers when the latest value is 0. Use the actual Zabbix host name and confirm trigger syntax against your installed version.

The receiver sends state to a single configured item. This is suitable only for one alert stream or one deliberately aggregated condition. Independent concurrent alerts need separate items/keys or an event-aware design so one alert's recovery cannot clear another alert.

## Install

From a repository checkout on the monitoring server:

~~~bash
sudo bash scripts/install_webhook_receiver.sh
~~~

The installer requires Python 3, systemd, curl, and zabbix_sender. It creates a service account, protected environment file, token, systemd unit, and starts the service. It does not automatically configure Zabbix, Grafana, or Alertmanager.

Review **/etc/monitoring-webhook.env**, including the Zabbix host, address, and item key. The generated token is stored in **/etc/monitoring-webhook-token**; keep it secret. Ensure the Alertmanager service account can read it before using the example Alertmanager config. For Grafana, configure the webhook Authorization header as Bearer followed by the token through the UI. Never put a real token in Git.

## Validate

~~~bash
python3 -m unittest discover -s tests -v
curl -fsS http://127.0.0.1:5001/healthz
~~~

The health endpoint proves only that the HTTP service responds. It does not prove authentication, sender connectivity, item existence, or trigger recovery.

The guarded synthetic pair sends firing and resolved states and may open/close a Zabbix problem. Use it only after confirming the target is a disposable test item:

~~~bash
ALLOW_TEST_ALERT=YES WEBHOOK_URL=http://127.0.0.1:5001/alertmanager WEBHOOK_TOKEN='your-token' bash scripts/smoke_test_webhook.sh
~~~

Avoid leaving secrets in shell history or process listings. Inspect Latest data and Problems manually after testing.
