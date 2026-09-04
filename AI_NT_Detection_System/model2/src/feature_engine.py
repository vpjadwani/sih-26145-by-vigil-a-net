from __future__ import annotations


def _number(value, default=0.0):
    """
    Safely convert a value to a float.
    """
    if value is None:
        return float(default)

    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def extract_features(flow):
    """
    Convert one Model-1 standardized JSON flow into
    the exact 28 numerical features required by Model 2.
    """

    traffic = flow.get("traffic") or {}
    packet_statistics = flow.get("packet_statistics") or {}
    tcp = flow.get("tcp") or {}
    dns = flow.get("dns") or {}
    behavior = flow.get("behavior") or {}

    features = {

        # -------------------------------------------------
        # Traffic
        # -------------------------------------------------

        "duration":
            _number(traffic.get("duration")),

        "total_packets":
            _number(traffic.get("total_packets")),

        "forward_packets":
            _number(traffic.get("forward_packets")),

        "backward_packets":
            _number(traffic.get("backward_packets")),

        "forward_bytes":
            _number(traffic.get("forward_bytes")),

        "backward_bytes":
            _number(traffic.get("backward_bytes")),

        "packets_per_second":
            _number(traffic.get("packets_per_second")),

        "bytes_per_second":
            _number(traffic.get("bytes_per_second")),

        "forward_packet_mean":
            _number(traffic.get("forward_packet_mean")),

        "backward_packet_mean":
            _number(traffic.get("backward_packet_mean")),

        # -------------------------------------------------
        # Packet statistics
        # -------------------------------------------------

        "packet_min":
            _number(packet_statistics.get("min_size")),

        "packet_max":
            _number(packet_statistics.get("max_size")),

        "packet_mean":
            _number(packet_statistics.get("mean_size")),

        "packet_std":
            _number(packet_statistics.get("std_size")),

        "mean_iat":
            _number(packet_statistics.get("mean_iat")),

        # -------------------------------------------------
        # TCP
        # -------------------------------------------------

        "syn":
            _number(tcp.get("syn")),

        "ack":
            _number(tcp.get("ack")),

        "rst":
            _number(tcp.get("rst")),

        # -------------------------------------------------
        # DNS
        # -------------------------------------------------

        "dns_query_count":
            _number(dns.get("query_count")),

        "dns_unique_domains":
            _number(dns.get("unique_domains")),

        "dns_avg_query_length":
            _number(dns.get("average_query_length")),

        "dns_max_query_length":
            _number(dns.get("maximum_query_length")),

        "dns_entropy":
            _number(dns.get("domain_entropy")),

        # -------------------------------------------------
        # Behaviour
        # -------------------------------------------------

        "unique_destination_ips":
            _number(behavior.get("unique_destination_ips")),

        "unique_destination_ports":
            _number(behavior.get("unique_destination_ports")),

        "connection_rate":
            _number(behavior.get("connection_rate")),

        "fb_packet_ratio":
            _number(
                behavior.get(
                    "forward_backward_packet_ratio"
                )
            ),

        "fb_byte_ratio":
            _number(
                behavior.get(
                    "forward_backward_byte_ratio"
                )
            )
    }

    return features