# Zabbix Trapper Integration

## Components

- A Zabbix host representing the monitored system or integration source.
- A trapper item with a stable key and compatible value type.
- A trigger expression that interprets firing and recovery values.
- A webhook receiver that calls `zabbix_sender`.

## Integration validation

1. Verify exact host name and item key in the Zabbix frontend.
2. Verify the item type is Zabbix trapper and its data type matches the submitted value.
3. Send a controlled test value from an authorized environment.
4. Check Latest data to confirm the value arrived.
5. Confirm the trigger opens on the intended firing value.
6. Send a distinct recovery value.
7. Confirm the trigger/problem clears according to the configured recovery expression.

## Important design warning

A trigger that opens when the latest value is merely non-empty may not clear if a resolved event is also submitted as a non-empty string. Define a state contract (firing value and recovery value) and align the receiver, item type, and trigger expression. Test the full lifecycle; do not infer recovery from `zabbix_sender` success alone.

Do not include real sender credentials or private server addresses in public documentation.
