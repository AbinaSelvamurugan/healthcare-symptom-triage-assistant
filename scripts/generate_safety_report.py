from careguide.config import ROOT
from careguide.reporting.scenarios import write_report

if __name__ == "__main__":
    report = write_report(ROOT)
    print(f"Generated 4 report artifacts from {len(report['scenario_results'])} measured synthetic scenarios")
