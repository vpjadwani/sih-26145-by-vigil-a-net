import argparse
import json
from pathlib import Path

from network_parser import parse_packet_csv, parse_pcap


def main():
    parser = argparse.ArgumentParser(
        description="Model 1: Raw network data -> standardized JSON"
    )

    parser.add_argument(
        "input",
        help="Path to PCAP, PCAPNG, CAP or packet CSV"
    )

    parser.add_argument(
        "--max-flows",
        type=int,
        default=None,
        help="Maximum number of flows to process"
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    # Check input
    if not input_path.exists():
        raise SystemExit(
            f"\nERROR: Input file does not exist:\n{input_path}"
        )

    extension = input_path.suffix.lower()

    print("\n========================================")
    print(" MODEL 1 - NETWORK DATA ENGINE")
    print("========================================")
    print(f"Input : {input_path}")
    print(f"Type  : {extension}")
    print("----------------------------------------")

    # Parse input
    if extension in {".pcap", ".pcapng", ".cap"}:

        print("Reading packet capture...")
        flows = parse_pcap(
            str(input_path),
            args.max_flows
        )

    elif extension == ".csv":

        print("Reading CSV...")
        flows = parse_packet_csv(
            str(input_path),
            args.max_flows
        )

    else:
        raise SystemExit(
            "\nERROR: Unsupported file format.\n"
            "Supported formats:\n"
            "  .pcap\n"
            "  .pcapng\n"
            "  .cap\n"
            "  .csv"
        )

    # ----------------------------------------
    # Create output directory automatically
    # ----------------------------------------

    project_root = Path(__file__).resolve().parents[1]

    output_dir = project_root / "output"

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------------------
    # Create JSON
    # ----------------------------------------

    output_file = (
        output_dir /
        f"{input_path.stem}_network.json"
    )

    result = {
        "schema_version": "1.0",
        "engine": "Model 1 - Network JSON Engine",
        "source_file": input_path.name,
        "flow_count": len(flows),
        "flows": flows
    }

    output_file.write_text(
        json.dumps(
            result,
            indent=2
        ),
        encoding="utf-8"
    )

    print("----------------------------------------")
    print(f"Flows : {len(flows)}")
    print(f"JSON  : {output_file}")
    print("----------------------------------------")
    print("MODEL 1 COMPLETED SUCCESSFULLY")
    print("========================================\n")


if __name__ == "__main__":
    main()