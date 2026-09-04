import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

print("\n=== SYSTEM MANUAL SCANNING INITIALIZED ===")

# Target filename
target_name = "normal_traffic_network_threat_results.json"

# Search directories manually
search_paths = [
    target_name,  # Right next to the script
    os.path.join("..", target_name),  # One folder up
    os.path.join("..", "..", target_name),  # Two folders up
]

resolved_file_path = None
for path in search_paths:
    if os.path.exists(path):
        resolved_file_path = path
        break

if not resolved_file_path:
    print(f"\n[!] FILE ACCESSIBILITY ERROR")
    print(f"    The engine looked everywhere but could not find: {target_name}")
    print(f"    Current Active Working Directory: {os.getcwd()}")
    print(f"    Files actually present in this folder: {os.listdir('.')}")
    print("\n💡 FIX: Please look at your drive and verify exactly which folder holds that JSON dataset.")
    exit()

print(f"[+] Dataset located at verified path: {os.path.abspath(resolved_file_path)}")

# Load the file dataset safely
with open(resolved_file_path, 'r') as file_handler:
    raw_json = json.load(file_handler)

# Convert structured JSON metrics into flattened matrix logs
flows = raw_json.get('results', raw_json.get('flows', raw_json if isinstance(raw_json, list) else []))
print(f"[*] Extracting behavioral parameters from {len(flows)} connection events...")

features_list = []
for flow_record in flows:
    row_data = {'threat_target': flow_record.get('threat_class', 'UNKNOWN')}
    evidence_metrics = flow_record.get('evidence_features', {})
    for metric_key, metric_val in evidence_metrics.items():
        row_data[metric_key] = metric_val
    features_list.append(row_data)

dataframe = pd.DataFrame(features_list).fillna(0)

# Break logic paths down to attributes and targets
X_matrix = dataframe.drop(columns=['threat_target'], errors='ignore')
y_vector = dataframe['threat_target']

print(f"[*] Detected distinct threat types: {list(y_vector.unique())}")

if len(y_vector.unique()) < 2:
    print("\n[!] ARREST: Dataset contains less than two separate threat classes. Training halted.")
    exit()

# Run target vector scalar mappings
encoder_engine = LabelEncoder()
y_encoded = encoder_engine.fit_transform(y_vector)

# Set up an 80/20 verification framework split
X_train, X_test, y_train, y_test = train_test_split(
    X_matrix, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print("[*] Processing mathematical calculations on Random Forest Pipeline...")
classification_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
classification_model.fit(X_train, y_train)

# Execute predictions against verify holdouts
predictions_output = classification_model.predict(X_test)

print("\n" + "="*55)
print(f"🎯 UNIFIED DATASET PREDICTION ACCURACY: {accuracy_score(y_test, predictions_output) * 100:.2f}%")
print("="*55 + "\n")

print("📊 Granular Attack Classification Performance Matrix:")
print(classification_report(y_test, predictions_output, target_names=encoder_engine.classes_))
