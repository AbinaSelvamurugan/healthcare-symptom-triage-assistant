"""Optional online check of *account-specific* access to the configured model."""
import sys
from careguide.llm.anthropic_client import AnthropicProvider, ProviderUnavailable

try:
    provider = AnthropicProvider()
    if not provider.verify_model():
        print("Model check failed: configured model is not active or accessible")
        sys.exit(1)
    print("PASS: configured model accessible to the authenticated Anthropic account")
except ProviderUnavailable as exc:
    print(f"Model check failed: {exc}")
    sys.exit(2)
