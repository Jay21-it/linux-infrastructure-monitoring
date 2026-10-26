# Zabbix Trapper Integration

## Original lab note

The original lab integration was reported to use trapper key prometheus.alert. Verify its item type and trigger logic before reuse.

## Reference receiver in this repository

The included reference receiver uses key prometheus.alert.state and numeric unsigned values (1 = firing, 0 = resolved). Configure the same key and host name in /etc/monitoring-webhook.env and Zabbix. Do not mix this contract with the original text item without adapting the receiver and trigger.

## Zabbix UI checklist

1. Open the correct Zabbix host.
2. Create a Zabbix trapper item.
3. Set key prometheus.alert.state and information type Numeric (unsigned).
4. Create a trigger with problem condition latest value 1 and recovery condition latest value 0.
5. Ensure ZABBIX_HOST exactly matches the Zabbix host name.
6. Send a controlled firing value and verify Latest data and Problems.
7. Send recovery and confirm the same problem clears.

Exact expression syntax varies by Zabbix version; validate it in the installed release.

## Recovery warning

A trigger based only on a non-empty text item may remain active when the resolved event is also non-empty. A zabbix_sender result of processed: 1; failed: 0 does not alone prove that a trigger opened or cleared.
