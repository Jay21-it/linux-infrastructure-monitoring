# Tests

Run the receiver payload mapping tests from the repository root:

~~~bash
python3 -m unittest discover -s tests -v
~~~

These unit tests verify status normalization only. They do not start the HTTP server, invoke zabbix_sender, or prove Zabbix trigger/recovery behavior.
