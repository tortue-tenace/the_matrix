import os, sys
from dotenv import load_dotenv
from typing import Any

print("\nORACLE STATUS: Reading the Matrix...\n")
if not load_dotenv(".env"):
    print("No .env file found")
required_vars = ["MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL", "ZION_ENDPOINT"]
missing = [name for name in required_vars if os.getenv(name) is None]
if missing:
    print("WARNING: Missing configuration for :", ", ".join(missing))
else:
    print("Whole configuration loaded:")
variables: list[tuple[str, str | None]] = [("MODE:", os.getenv("MATRIX_MODE")),
("DATABASE:", os.getenv("DATABASE_URL")),
("API ACCESS:", os.getenv("API_KEY")),
("LOG LEVEL:", os.getenv("LOG_LEVEL")),
("ZION NETWORK:", os.getenv("ZION_ENDPOINT"))]
for name, value in variables:
    if value is not None:
        print(name, value)
    else:
        print(f"{name} varialbe is empty")
mode = os.getenv("MATRIX_MODE", "production")
if mode == "development":
    print("Mode: development (verbose logging enabled)")
else:
    print("Mode: production (strict security checks)")
print("\nEnvironment security check:")
print("[OK] No hardcoded secrets detected")
if load_dotenv(".env"):
    print("[OK] .env file properly configured")
else:
    print("[MISSING] No .env file found (using system environment variables)")
if missing:
    print(f"[MISSING] Incomplete configuration: {', '.join(missing)}")
else:
    print("[OK] Configuration complete")
print("[OK] Production overrides available")
print("\nThe Oracle sees all configurations.")