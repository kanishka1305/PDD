import json
from pathlib import Path

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


def generate_report(scan_id, analysis_result):

    report_path = REPORT_DIR / f"report_{scan_id}.json"

    with open(report_path, "w") as file:
        json.dump(
            analysis_result,
            file,
            indent=4
        )

    return str(report_path)