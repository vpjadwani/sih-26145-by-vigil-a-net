
# SIH 2026 — Model 1 + JSON-native Model 2

Model 1 converts raw network captures into one standardized JSON schema.
Model 2 is rebuilt to consume ONLY that JSON schema. It does not use CIC-IDS CSV column names during inference.

Pipeline:
RAW PCAP/PCAPNG/packet CSV -> Model 1 -> standardized JSON -> Model 2 -> threat alert JSON

Classes:
NORMAL_TRAFFIC, DDOS, BOTNET_C2, DNS_TUNNELING, ENCRYPTED_MALWARE, RECON_SCAN, DATA_EXFILTRATION

## Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

## Run everything
python run_pipeline.py "C:\path\capture.pcap"

## Existing Model 1 JSON
python model2\src\threat_analyzer.py "model1\output\capture_network.json"

## Output
model1\output\<name>_network.json
model2\output\<name>_network_threat_results.json

IMPORTANT: the included Model 2 is a demonstration classifier trained on synthetic feature distributions. It is not production security accuracy. For SIH evaluation, retrain it with real labeled network data converted to the exact same JSON schema.

The system is passive/read-only: it analyzes supplied/captured traffic and emits alerts; it does not probe endpoints, initiate sessions, send mitigation commands, or write back to production.

Author : Yuvraj Oza
