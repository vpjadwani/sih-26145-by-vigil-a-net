# 🛡️ AI-Based Passive Network Threat Detection System

### SIH 2026 — Problem Statement 145

> **A local, passive AI/ML system for detecting DDoS, DNS Tunneling, Botnet C2, and normal network traffic from PCAP files — without API keys or active network interaction.**

---

## 📌 Overview

This project is a **local AI/ML-based network security analysis system** developed as a prototype for **Smart India Hackathon (SIH) 2026 — Problem Statement 145**.

The system analyzes network traffic captured in **PCAP/PCAPNG files** and detects suspicious behavior using a combination of:

* Network flow analysis
* Feature engineering
* Machine Learning
* Behavioral analysis
* Risk scoring
* Evidence generation

### Current Stage

The first version focuses on four traffic classes:

| Class               | Description                               |
| ------------------- | ----------------------------------------- |
| 🟢 `NORMAL_TRAFFIC` | Normal network activity                   |
| 🔴 `DDOS`           | Volumetric / protocol-based DDoS behavior |
| 🟠 `DNS_TUNNELING`  | Suspicious data transmission through DNS  |
| 🟡 `BOTNET_C2`      | Command-and-control beaconing behavior    |

Future versions will extend the system to additional threats such as reconnaissance, port scanning, DGA, data exfiltration, and encrypted malware detection.

---

# 🎯 Problem Statement

Traditional network security systems may actively communicate with suspicious hosts, perform probes, or send mitigation commands.

However, **SIH Problem Statement 145 requires a strictly passive monitoring architecture**.

The monitoring system must:

* Observe network traffic
* Process traffic incrementally
* Detect threats
* Generate intelligence
* Provide confidence and evidence

But it must **never send traffic back into the monitored network**.

### Core principle

```text
             MONITORED NETWORK
                     │
                     │
                     ▼
              Traffic Mirror
                     │
                     │ READ ONLY
                     ▼
          ┌─────────────────────┐
          │ Passive Monitoring  │
          │      System         │
          └──────────┬──────────┘
                     │
                     ▼
                AI / ML
                     │
                     ▼
              Threat Alert
```

There is **no return path** from the monitoring system to the production network.

---

# 🚀 Key Features

### 🔍 PCAP Analysis

Accepts:

```text
.pcap
.pcapng
```

and extracts network traffic information.

### 🌐 Flow-Based Analysis

Packets are converted into network flows using information such as:

```text
Source IP
Destination IP
Source Port
Destination Port
Protocol
```

### 🧠 Machine Learning

The system uses locally trained ML models.

No external AI API is required.

```text
PCAP
 ↓
Features
 ↓
ML Model
 ↓
Prediction
```

### 🚨 Threat Detection

Currently supports:

```text
NORMAL_TRAFFIC
DDOS
DNS_TUNNELING
BOTNET_C2
```

### 📊 Risk Scoring

Every suspicious detection receives a risk score from:

```text
0 ─────────────── 100
```

Example:

```text
Risk Score: 94
Severity: CRITICAL
Confidence: 96%
```

### 📝 Explainable Evidence

Instead of only saying:

```text
DDOS detected
```

the system provides supporting evidence:

```text
• High packet rate
• Abnormal SYN activity
• Large number of source IPs
• Sudden traffic spike
```

### 🔌 Completely Local

The system does not require:

* API keys
* Cloud AI
* External inference APIs
* Internet access during inference

---

# 🏗️ Architecture

```text
                  PCAP / PCAPNG
                        │
                        ▼
               ┌─────────────────┐
               │  PCAP Reader    │
               └────────┬────────┘
                        ▼
               ┌─────────────────┐
               │  Flow Engine    │
               └────────┬────────┘
                        ▼
               ┌─────────────────┐
               │ Feature Engine  │
               └────────┬────────┘
                        ▼
          ┌─────────────────────────────┐
          │       ML Detection          │
          │                             │
          │  NORMAL                     │
          │  DDOS                       │
          │  DNS TUNNELING              │
          │  BOTNET C2                  │
          └──────────────┬──────────────┘
                         ▼
                ┌─────────────────┐
                │  Risk Engine    │
                └────────┬────────┘
                         ▼
                ┌─────────────────┐
                │ Evidence Engine │
                └────────┬────────┘
                         ▼
                  JSON / CSV Alert
```

---

# 🧩 Technology Stack

### Programming Language

* Python 3.11+

### Packet Processing

* Scapy

### Data Processing

* NumPy
* pandas

### Machine Learning

* scikit-learn
* Random Forest

### Model Persistence

* joblib

### Testing

* pytest

---

# 📁 Project Structure

```text
network-threat-ai/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── test_pcaps/
│
├── models/
│   └── network_threat_model.pkl
│
├── src/
│   ├── pcap_reader.py
│   ├── flow_engine.py
│   ├── feature_engine.py
│   ├── predictor.py
│   ├── risk_engine.py
│   └── evidence_engine.py
│
├── training/
│   ├── prepare_dataset.py
│   ├── train.py
│   └── evaluate.py
│
├── tests/
│   ├── test_features.py
│   ├── test_prediction.py
│   └── test_pipeline.py
│
├── outputs/
│
├── analyze.py
├── requirements.txt
├── config.yaml
└── README.md
```

---

# 📥 Input

The primary input is a network capture:

```text
sample.pcap
```

Example:

```bash
python analyze.py sample.pcap
```

The system reads the traffic and extracts:

### Basic Features

```text
Flow duration
Packet count
Byte count
Packets/sec
Bytes/sec
Average packet size
Packet-size variance
```

### TCP Features

```text
SYN count
ACK count
RST count
FIN count
SYN/ACK ratio
```

### Directional Features

```text
Forward packets
Backward packets
Forward bytes
Backward bytes
Packet ratio
Byte ratio
```

### Behavioral Features

```text
Unique destination IPs
Unique destination ports
Connection frequency
```

### DNS Features

```text
DNS query count
Query length
Domain entropy
Unique domains
NXDOMAIN count
TXT query count
Response ratio
```

---

# 🤖 Detection Approach

## 1. DDoS Detection

The system analyzes:

```text
Packet rate
Byte rate
SYN activity
UDP activity
Source-IP distribution
Traffic spikes
Flow volume
```

Example:

```text
Packets/sec: 85,421
Unique sources: 1,824
SYN rate: Extremely High

→ Possible DDoS
```

---

## 2. DNS Tunneling Detection

The system analyzes DNS behavior without performing external DNS queries.

Features include:

```text
Query length
Domain entropy
Query frequency
TXT activity
Domain structure
DNS response behavior
```

Example:

```text
Average query length: 87
Entropy: High
Queries/minute: 2,140

→ Possible DNS Tunneling
```

---

## 3. Botnet C2 Detection

The system looks for behavioral patterns such as:

```text
Repeated connections
Periodic communication
Inter-arrival timing
Repeated destinations
Connection frequency
Packet-size patterns
```

Example:

```text
Connection interval:
60.1 sec
59.8 sec
60.2 sec
60.0 sec

→ Possible C2 Beaconing
```

---

## 4. Normal Traffic

Traffic without significant indicators of the supported threats is classified as:

```text
NORMAL_TRAFFIC
```

---

# 🧠 Machine Learning Pipeline

```text
Labeled Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Train / Test Split
      │
      ▼
Random Forest
      │
      ▼
Model Evaluation
      │
      ▼
network_threat_model.pkl
```

During inference:

```text
New PCAP
   │
   ▼
Feature Extraction
   │
   ▼
Saved ML Model
   │
   ▼
Prediction
   │
   ▼
Confidence
   │
   ▼
Risk Score
```

---

# 📊 Output

The system produces structured JSON and CSV results.

Example:

```json
{
  "file": "sample.pcap",
  "total_packets": 152340,
  "total_flows": 4821,
  "overall_risk_score": 94,
  "detections": [
    {
      "timestamp": "2026-09-03T10:42:31Z",
      "source_ip": "192.168.1.20",
      "destination_ip": "10.0.0.5",
      "source_port": 45120,
      "destination_port": 80,
      "protocol": "TCP",
      "attack_type": "DDOS",
      "confidence": 0.96,
      "risk_score": 94,
      "packet_count": 45210,
      "byte_count": 38492010,
      "evidence": [
        "High packet rate",
        "Abnormal SYN activity",
        "Large number of source IPs"
      ]
    }
  ]
}
```

---

# ⚠️ Risk Levels

```text
0 – 29     LOW
30 – 59    MEDIUM
60 – 79    HIGH
80 – 100   CRITICAL
```

The risk score is an analytical score and should not be interpreted as a guaranteed probability of malicious activity.

---

# 🧪 Testing

The system should be evaluated using controlled PCAP test cases.

```text
test_normal.pcap
test_ddos.pcap
test_dns_tunnel.pcap
test_botnet.pcap
```

Expected classifications:

```text
test_normal.pcap
        ↓
NORMAL_TRAFFIC

test_ddos.pcap
        ↓
DDOS

test_dns_tunnel.pcap
        ↓
DNS_TUNNELING

test_botnet.pcap
        ↓
BOTNET_C2
```

Evaluation metrics include:

```text
Accuracy
Precision
Recall
F1 Score
Confusion Matrix
False Positive Rate
False Negative Rate
Detection Latency
```

---

# ▶️ Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd network-threat-ai
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🚀 Usage

After the model has been trained:

```bash
python analyze.py sample.pcap
```

Specify an output file:

```bash
python analyze.py sample.pcap --output outputs/result.json
```

CSV output:

```bash
python analyze.py sample.pcap --format csv
```

---

# 🏋️ Training

Prepare the dataset:

```bash
python training/prepare_dataset.py
```

Train the model:

```bash
python training/train.py
```

Evaluate:

```bash
python training/evaluate.py
```

The trained model will be saved locally:

```text
models/network_threat_model.pkl
```

---

# 🔐 Security & Privacy

This project follows the passive-monitoring concept required by SIH Problem Statement 145.

The analyzer:

```text
✓ Reads PCAP data
✓ Extracts traffic metadata
✓ Builds network flows
✓ Performs local ML inference
✓ Generates alerts
```

It does not:

```text
✗ Send packets
✗ Scan external hosts
✗ Perform active reconnaissance
✗ Query external DNS servers
✗ Decrypt encrypted payloads
✗ Send mitigation commands
```

---

# 📈 Future Roadmap

### Stage 1 — Current

* [x] PCAP input
* [x] Flow extraction
* [x] Feature engineering
* [ ] DDoS detection
* [ ] DNS tunneling detection
* [ ] Botnet C2 detection
* [ ] Normal traffic classification
* [ ] Risk scoring
* [ ] Evidence generation

### Stage 2

Planned additional detections:

```text
Port Scanning
Reconnaissance
DGA Domains
Data Exfiltration
```

### Stage 3

Encrypted traffic analysis:

```text
JA3
JA3S
JA4
TLS metadata
QUIC metadata
Packet-size sequences
Timing sequences
```

### Stage 4

Real-time architecture:

```text
Network Mirror / Data Diode
          ↓
      Stream Input
          ↓
    Feature Engine
          ↓
      ML Inference
          ↓
      Alert Engine
          ↓
       Dashboard
```

---

# 🎯 SIH 2026 Compliance

This prototype is designed around the following requirements of Problem Statement 145:

| Requirement                  | Implementation |
| ---------------------------- | -------------- |
| Read-only ingest             | ✅              |
| No return path               | ✅              |
| No payload decryption        | ✅              |
| Streaming-ready architecture | ✅              |
| Threat classification        | ✅              |
| Confidence score             | ✅              |
| Supporting evidence          | ✅              |
| Structured alerts            | ✅              |
| Throughput benchmarking      | Planned        |
| Live dashboard               | Planned        |

---

# ⚠️ Limitations

This is a research/prototype system and should not be considered a complete enterprise security product.

Machine-learning detection can produce:

* False positives
* False negatives
* Dataset-dependent performance
* Reduced accuracy against previously unseen traffic

Performance should therefore be evaluated on traffic that is separate from the training data.

---

# 📜 Disclaimer

This project is intended for **cybersecurity research, education, network defense, and authorized testing only**.

Only analyze network traffic that you are authorized to monitor.

---

# 👨‍💻 Project

Developed as a prototype for:

**Smart India Hackathon 2026**

**Problem Statement: 145**

### Focus

> Passive AI/ML-based network threat detection using network traffic metadata.

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ star and following the project as it evolves through the next development stages.
