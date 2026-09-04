
import csv, math
from collections import defaultdict
from datetime import datetime, timezone

def _f(v, d=0.0):
    try: return float(v)
    except Exception: return d
def _i(v, d=0):
    try: return int(float(v))
    except Exception: return d
def _mean(x): return sum(x)/len(x) if x else 0.0
def _entropy(s):
    if not s: return 0.0
    counts=defaultdict(int)
    for c in s: counts[c]+=1
    n=len(s)
    return -sum((v/n)*math.log2(v/n) for v in counts.values())

def _make_flow(fid, packets):
    if not packets: return None
    first=packets[0]
    src,dst=first["src_ip"],first["dst_ip"]
    times=[_f(p["timestamp"]) for p in packets]
    duration=max(0.0,max(times)-min(times))
    fwd=[p for p in packets if p["src_ip"]==src and p["dst_ip"]==dst]
    bwd=[p for p in packets if p["src_ip"]==dst and p["dst_ip"]==src]
    sizes=[_i(p["length"]) for p in packets]
    fs=[_i(p["length"]) for p in fwd]; bs=[_i(p["length"]) for p in bwd]
    total_bytes=sum(sizes)
    pps=len(packets)/duration if duration>0 else float(len(packets))
    bps=total_bytes/duration if duration>0 else float(total_bytes)
    iats=[times[i]-times[i-1] for i in range(1,len(times)) if times[i]>=times[i-1]]
    flags=defaultdict(int)
    for p in packets:
        raw=str(p.get("tcp_flags","")).upper()
        for name,tok in [("syn","SYN"),("ack","ACK"),("fin","FIN"),("rst","RST"),("psh","PSH"),("urg","URG")]:
            if tok in raw: flags[name]+=1
    names=[str(p["dns_qry_name"]).rstrip(".") for p in packets if p.get("dns_qry_name")]
    nlen=[len(x) for x in names]
    return {
        "flow_id":fid,
        "timestamp":datetime.fromtimestamp(min(times),tz=timezone.utc).isoformat() if times else datetime.now(timezone.utc).isoformat(),
        "network":{"src_ip":src,"src_port":first.get("src_port"),"dst_ip":dst,"dst_port":first.get("dst_port"),"protocol":first.get("protocol","UNKNOWN")},
        "traffic":{
            "duration":duration,"total_packets":len(packets),"forward_packets":len(fwd),"backward_packets":len(bwd),
            "forward_bytes":sum(_i(p["length"]) for p in fwd),"backward_bytes":sum(_i(p["length"]) for p in bwd),
            "total_bytes":total_bytes,"packets_per_second":pps,"bytes_per_second":bps,
            "forward_packet_mean":_mean(fs),"backward_packet_mean":_mean(bs)
        },
        "packet_statistics":{
            "min_size":min(sizes) if sizes else 0,"max_size":max(sizes) if sizes else 0,
            "mean_size":_mean(sizes),
            "std_size":(sum((x-_mean(sizes))**2 for x in sizes)/len(sizes))**0.5 if sizes else 0,
            "mean_iat":_mean(iats)
        },
        "tcp":dict(flags),
        "dns":{
            "query_count":len(names),"unique_domains":len(set(names)),
            "average_query_length":_mean(nlen),"maximum_query_length":max(nlen) if nlen else 0,
            "domain_entropy":_entropy("".join(names))
        },
        "behavior":{
            "unique_destination_ips":len({p["dst_ip"] for p in packets if p["dst_ip"]}),
            "unique_destination_ports":len({p.get("dst_port") for p in packets if p.get("dst_port") not in ("",None)}),
            "connection_rate":1.0/max(duration,0.001),
            "forward_backward_packet_ratio":len(fwd)/max(1,len(bwd)),
            "forward_backward_byte_ratio":sum(_i(p["length"]) for p in fwd)/max(1,sum(_i(p["length"]) for p in bwd))
        }
    }

def _group(rows, max_flows=None):
    groups={}
    for p in rows:
        key=(p["src_ip"],p["dst_ip"],str(p.get("src_port")),str(p.get("dst_port")),p["protocol"])
        rev=(p["dst_ip"],p["src_ip"],str(p.get("dst_port")),str(p.get("src_port")),p["protocol"])
        groups.setdefault(rev if rev in groups else key,[]).append(p)
    out=[]
    for i,packets in enumerate(groups.values(),1):
        if max_flows and i>max_flows: break
        f=_make_flow(f"F-{i:06d}",packets)
        if f: out.append(f)
    return out

def parse_packet_csv(path,max_flows=None):
    with open(path,newline="",encoding="utf-8-sig",errors="replace") as f:
        reader=csv.DictReader(f); rows=[]
        for r in reader:
            def g(*ks):
                for k in ks:
                    if k in r and r[k] not in ("",None): return r[k]
                return ""
            rows.append({
                "timestamp":g("frame.time_epoch","timestamp","time"),
                "src_ip":g("ip.src","src_ip","Source IP"),
                "dst_ip":g("ip.dst","dst_ip","Destination IP"),
                "src_port":g("tcp.srcport","udp.srcport","src_port","Source Port"),
                "dst_port":g("tcp.dstport","udp.dstport","dst_port","Destination Port"),
                "protocol":g("ip.proto","protocol","Protocol"),
                "tcp_flags":g("tcp.flags","tcp_flags","TCP Flags"),
                "length":g("frame.len","length","Length","Packet Length"),
                "dns_qry_name":g("dns.qry.name","dns.query","dns_qry_name")
            })
    return _group(rows,max_flows)

def parse_pcap(path,max_flows=None):
    from scapy.all import rdpcap,IP,IPv6,TCP,UDP,DNS,DNSQR
    rows=[]
    for p in rdpcap(path):
        if IP in p: src,dst,proto=p[IP].src,p[IP].dst,str(p[IP].proto)
        elif IPv6 in p: src,dst,proto=p[IPv6].src,p[IPv6].dst,str(p[IPv6].nh)
        else: continue
        r={"timestamp":float(getattr(p,"time",0)),"src_ip":src,"dst_ip":dst,"src_port":"","dst_port":"","protocol":proto,"tcp_flags":"","length":len(p),"dns_qry_name":""}
        if TCP in p:
            r["src_port"],r["dst_port"]=int(p[TCP].sport),int(p[TCP].dport); r["tcp_flags"]=str(p[TCP].flags)
        elif UDP in p:
            r["src_port"],r["dst_port"]=int(p[UDP].sport),int(p[UDP].dport)
        if DNS in p and DNSQR in p:
            try: r["dns_qry_name"]=p[DNSQR].qname.decode(errors="ignore").rstrip(".")
            except Exception: pass
        rows.append(r)
    return _group(rows,max_flows)
