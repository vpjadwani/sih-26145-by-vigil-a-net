from __future__ import annotations

import sys
import json
from pathlib import Path
from datetime import datetime, timezone


# =========================================================
# PATHS
# =========================================================

MODEL2_DIR = Path(__file__).resolve().parent.parent

SRC_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = MODEL2_DIR / "output"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# IMPORT PREDICTOR
# =========================================================

sys.path.insert(
    0,
    str(SRC_DIR)
)

from predictor import predict


# =========================================================
# INPUT
# =========================================================

if len(sys.argv) < 2:

    print(
        "Usage:\n"
        "python threat_analyzer.py <model1_json>"
    )

    sys.exit(1)


input_path = Path(sys.argv[1])


if not input_path.exists():

    print(
        f"[ERROR] Input JSON does not exist:\n"
        f"{input_path}"
    )

    sys.exit(1)


# =========================================================
# LOAD MODEL 1 JSON
# =========================================================

try:

    data = json.loads(
        input_path.read_text(
            encoding="utf-8"
        )
    )

except Exception as e:

    print(
        f"[ERROR] Could not read Model 1 JSON:\n{e}"
    )

    sys.exit(1)


# =========================================================
# VALIDATE
# =========================================================

flows = data.get("flows")

if not isinstance(flows, list):

    print(
        "[ERROR] Model 1 JSON does not contain "
        "a valid 'flows' array."
    )

    sys.exit(1)


print()
print("========================================")
print(" MODEL 2 - NETWORK THREAT DETECTION")
print("========================================")
print(f"Input : {input_path}")
print(f"Flows : {len(flows)}")
print("----------------------------------------")


# =========================================================
# PROCESS FLOWS
# =========================================================

results = []

for flow in flows:

    flow_id = flow.get(
        "flow_id",
        "UNKNOWN"
    )

    try:

        prediction = predict(flow)

        result = {

            "timestamp":
                flow.get(
                    "timestamp",
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                ),

            "flow_id":
                flow_id,

            "network":
                flow.get(
                    "network",
                    {}
                ),

            "threat_class":
                prediction[
                    "threat_class"
                ],

            "confidence":
                prediction[
                    "confidence"
                ],

            "risk_score":
                prediction[
                    "risk_score"
                ],

            "severity":
                prediction[
                    "severity"
                ],

            "evidence_features":
                prediction[
                    "evidence_features"
                ]
        }

        results.append(result)

        print(
            f"[OK] {flow_id} -> "
            f"{prediction['threat_class']} "
            f"({prediction['confidence']:.2%})"
        )

    except Exception as e:

        print(
            f"[ERROR] {flow_id}: {e}"
        )

        results.append({

            "timestamp":
                flow.get("timestamp"),

            "flow_id":
                flow_id,

            "error":
                str(e)
        })


# =========================================================
# SUMMARY
# =========================================================

threat_counts = {}

for result in results:

    threat = result.get(
        "threat_class"
    )

    if threat:

        threat_counts[threat] = (
            threat_counts.get(
                threat,
                0
            ) + 1
        )


# =========================================================
# FINAL OUTPUT
# =========================================================

output = {

    "schema_version":
        "1.0",

    "engine":
        "Model 2 - Network Threat Detection",

    "source_file":
        input_path.name,

    "processed_at":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "flow_count":
        len(results),

    "threat_summary":
        threat_counts,

    "results":
        results
}


# =========================================================
# SAVE
# =========================================================

output_path = (
    OUTPUT_DIR /
    f"{input_path.stem}_threat_results.json"
)


output_path.write_text(

    json.dumps(
        output,
        indent=2
    ),

    encoding="utf-8"
)


print("----------------------------------------")
print(f"JSON  : {output_path}")
print("----------------------------------------")
print("MODEL 2 COMPLETED SUCCESSFULLY")
print("========================================")