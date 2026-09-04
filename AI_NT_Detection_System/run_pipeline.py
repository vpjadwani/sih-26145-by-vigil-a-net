from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def run():

    if len(sys.argv) < 2:

        print(
            "Usage:\n"
            "python run_pipeline.py <pcap_file>"
        )

        sys.exit(1)


    input_file = Path(sys.argv[1])


    if not input_file.exists():

        print(
            f"[ERROR] PCAP file not found:\n"
            f"{input_file}"
        )

        sys.exit(1)


    # =====================================================
    # MODEL 1
    # =====================================================

    model1_script = (
        ROOT /
        "model1" /
        "src" /
        "main.py"
    )


    print()
    print("########################################")
    print(" SIH 2026 NETWORK THREAT PIPELINE")
    print("########################################")
    print()


    subprocess.run(

        [
            sys.executable,
            str(model1_script),
            str(input_file)
        ],

        check=True
    )


    # =====================================================
    # MODEL 1 OUTPUT
    # =====================================================

    model1_output = (

        ROOT /
        "model1" /
        "output" /
        f"{input_file.stem}_network.json"
    )


    if not model1_output.exists():

        print(
            "[ERROR] Model 1 did not generate "
            "the expected JSON:"
        )

        print(model1_output)

        sys.exit(1)


    # =====================================================
    # MODEL 2
    # =====================================================

    model2_script = (

        ROOT /
        "model2" /
        "src" /
        "threat_analyzer.py"
    )


    subprocess.run(

        [
            sys.executable,
            str(model2_script),
            str(model1_output)
        ],

        check=True
    )


    print()
    print("########################################")
    print(" PIPELINE COMPLETED")
    print("########################################")
    print()
    print(
        "Model 1 JSON:"
    )
    print(
        model1_output
    )

    print()


if __name__ == "__main__":

    run()