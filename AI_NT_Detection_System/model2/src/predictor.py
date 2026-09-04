from __future__ import annotations

import json
from pathlib import Path

import joblib


# =========================================================
# PATHS
# =========================================================

BASE = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE / "model" / "network_threat_model_json.pkl"

SCHEMA_PATH = BASE / "feature_schema.json"


# =========================================================
# LOAD MODEL
# =========================================================

loaded_model = joblib.load(MODEL_PATH)


# Support both:
#
# RandomForestClassifier
#
# and:
#
# {
#     "model": RandomForestClassifier(...)
# }

if isinstance(loaded_model, dict):

    if "model" in loaded_model:
        model = loaded_model["model"]

    elif "classifier" in loaded_model:
        model = loaded_model["classifier"]

    elif "estimator" in loaded_model:
        model = loaded_model["estimator"]

    else:
        raise RuntimeError(
            "Model file contains a dictionary but no "
            "'model', 'classifier', or 'estimator' key was found.\n"
            f"Available keys: {list(loaded_model.keys())}"
        )

else:

    model = loaded_model


# =========================================================
# LOAD FEATURE SCHEMA
# =========================================================

with open(
    SCHEMA_PATH,
    "r",
    encoding="utf-8"
) as f:

    FEATURE_SCHEMA = json.load(f)


# =========================================================
# VALIDATE MODEL
# =========================================================

if not hasattr(model, "predict"):

    raise RuntimeError(
        "Loaded object is not a valid ML model.\n"
        f"Loaded type: {type(model)}"
    )


# =========================================================
# VALIDATE FEATURE COUNT
# =========================================================

EXPECTED_FEATURE_COUNT = 28

if len(FEATURE_SCHEMA) != EXPECTED_FEATURE_COUNT:

    raise RuntimeError(
        "Feature schema error.\n"
        f"Expected: {EXPECTED_FEATURE_COUNT}\n"
        f"Found: {len(FEATURE_SCHEMA)}"
    )


if hasattr(model, "n_features_in_"):

    if model.n_features_in_ != len(FEATURE_SCHEMA):

        raise RuntimeError(
            "Model/schema mismatch.\n"
            f"ML model expects: {model.n_features_in_} features\n"
            f"Schema contains: {len(FEATURE_SCHEMA)} features"
        )


# =========================================================
# PREDICTION
# =========================================================

def predict(flow):

    from feature_engine import extract_features

    features = extract_features(flow)

    # -----------------------------------------------------
    # Build EXACT 28-feature vector
    # -----------------------------------------------------

    X = [
        [
            float(features.get(feature, 0.0))
            for feature in FEATURE_SCHEMA
        ]
    ]

    # -----------------------------------------------------
    # Safety check
    # -----------------------------------------------------

    if len(X[0]) != model.n_features_in_:

        raise RuntimeError(
            "Feature vector size mismatch.\n"
            f"Generated: {len(X[0])}\n"
            f"Expected: {model.n_features_in_}"
        )

    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    predicted_class = model.predict(X)[0]

    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(X)[0]

        confidence = float(max(probabilities))

    else:

        confidence = 1.0

    # -----------------------------------------------------
    # Risk base
    # -----------------------------------------------------

    risk_base = {

        "NORMAL_TRAFFIC": 10,

        "DDOS": 90,

        "BOTNET_C2": 70,

        "DNS_TUNNELING": 80,

        "ENCRYPTED_MALWARE": 75,

        "RECON_SCAN": 65,

        "DATA_EXFILTRATION": 85
    }

    base_risk = risk_base.get(
        str(predicted_class),
        50
    )

    # -----------------------------------------------------
    # Risk score
    # -----------------------------------------------------

    risk_score = round(
        base_risk *
        (
            0.6 +
            0.4 * confidence
        ),
        2
    )

    # -----------------------------------------------------
    # Severity
    # -----------------------------------------------------

    if risk_score >= 80:

        severity = "CRITICAL"

    elif risk_score >= 60:

        severity = "HIGH"

    elif risk_score >= 35:

        severity = "MEDIUM"

    else:

        severity = "LOW"

    # -----------------------------------------------------
    # Evidence
    # -----------------------------------------------------

    evidence = {}

    for feature in FEATURE_SCHEMA:

        value = features.get(feature, 0)

        if value != 0:

            evidence[feature] = value

    # -----------------------------------------------------
    # Result
    # -----------------------------------------------------

    return {

        "threat_class":
            str(predicted_class),

        "confidence":
            round(confidence, 4),

        "risk_score":
            risk_score,

        "severity":
            severity,

        "evidence_features":
            evidence
    }