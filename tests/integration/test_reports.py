import json
from careguide.config import ROOT
from careguide.reporting.scenarios import write_report


def test_real_report_generation(tmp_path):
    # Evaluates existing synthetic input data and writes generated results, not mocked aggregate values.
    report = write_report(ROOT)
    assert report["summary"]["scenario_count"] > 20
    assert report["summary"]["pass"] + report["summary"]["fail"] == report["summary"]["scenario_count"]
    assert report["clinical_validation"] == "not clinically validated"
    assert (ROOT / "reports/safety_report.json").is_file()
    assert (ROOT / "reports/scenario_results.csv").is_file()
    assert json.loads((ROOT / "reports/safety_report.json").read_text())["summary"] == report["summary"]
