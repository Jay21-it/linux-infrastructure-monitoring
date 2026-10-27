# Dashboards and PromQL Reference

These queries assume Node Exporter labels similar to the example. Verify metric names and labels in your own Prometheus instance before using them.

## Target availability

```promql
up{job="node"}
```

`1` means the most recent scrape succeeded; `0` means the scrape failed. It does not confirm application-level health.

## CPU utilization

```promql
100 - (
  avg by (instance) (
    rate(node_cpu_seconds_total{mode="idle"}[5m])
  ) * 100
)
```

## Memory utilization

```promql
100 * (
  1 - (
    node_memory_MemAvailable_bytes
    / node_memory_MemTotal_bytes
  )
)
```

## Root filesystem utilization

```promql
100 * (
  1 - (
    node_filesystem_avail_bytes{mountpoint="/",fstype!~"tmpfs|overlay"}
    /
    node_filesystem_size_bytes{mountpoint="/",fstype!~"tmpfs|overlay"}
  )
)
```

Confirm the filesystem labels on the target; the filter may need adjustment.

## Network throughput

Receive bytes per second:

```promql
rate(node_network_receive_bytes_total{device!="lo"}[5m])
```

Transmit bytes per second:

```promql
rate(node_network_transmit_bytes_total{device!="lo"}[5m])
```

Multiply by 8 for bits per second. Use Grafana units that match the query.

## Service state

With Node Exporter's systemd collector enabled, a query pattern for a service active-state series is:

```promql
node_systemd_unit_state{
  name="httpd.service",
  state="active"
}
```

For a service-down alert, confirm how the metric behaves when the unit is inactive and whether the series disappears or returns zero. A query ending in `== 0` only works when a matching series exists and has value zero. Configure No Data behavior separately.

The starter dashboard includes CPU, memory, root filesystem, scrape health, load average, network receive/transmit, and an HTTPD active-state panel. The service panel will show no data until the systemd collector exposes `httpd.service` and the Prometheus instance label matches the dashboard variable.

## Dashboard standards

- Use consistent dashboard variables and labels.
- Label panels with host/service and measurement.
- Set units, decimals, legends, and thresholds intentionally.
- Distinguish no data from zero.
- Use time ranges appropriate for troubleshooting.
- Avoid unbounded/high-cardinality labels.
- Do not use a metric sample timestamp as definitive alert start time; inspect alert details or Alertmanager/Grafana alert metadata.
