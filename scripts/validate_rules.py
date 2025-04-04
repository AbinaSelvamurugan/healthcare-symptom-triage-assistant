"""Validate configuration schemas and report clinical approval."""
import sys
from careguide.config import load_config
from careguide.clinical_rules.engine import RuleEngine


def main() -> int:
    try:
        config, policy, protocol = load_config()
        RuleEngine(protocol)
    except Exception as exc:
        print(f"CONFIGURATION FAIL: {type(exc).__name__}: {exc}")
        return 1
    print(f"PASS: configuration schema, policy {policy.policy_version}, {len(protocol.rules)} demonstration rules")
    print(f"Mode: {config.mode}; jurisdiction: {config.jurisdiction}")
    print("Clinical approval: none. These are demonstration fixtures only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
