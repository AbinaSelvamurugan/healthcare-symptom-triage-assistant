import sys
from careguide.config import ROOT
from careguide.reporting.scenarios import write_report

if __name__ == "__main__":
    report = write_report(ROOT)
    print(f"Synthetic scenarios: {report['summary']['pass']} PASS / {report['summary']['fail']} FAIL")
    print("Reports: reports/safety_report.json, reports/scenario_results.csv, reports/safety_metrics.csv, reports/safety_report.md")
    print("Clinical acceptance: not clinically validated")
    sys.exit(1 if report["summary"]["fail"] else 0)
