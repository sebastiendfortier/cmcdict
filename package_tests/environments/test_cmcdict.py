import sys
import cmcdict

EXPECTED_OUTPUT = {
    "nomvar": "TT",
    "usage": "current",
    "origin": "",
    "date": "",
    "measure_type": "real",
    "description_short_en": "Air temperature",
    "description_short_fr": "Température de l'air",
    "description_long_en": "",
    "description_long_fr": "",
    "units": "°C",
    "min": "",
    "max": "",
    "codes": None,
    "precision": "",
    "magnitude": "",
}


def run_test():
    sys.stdout.write(f"\nPython version: {sys.version}\n")
    sys.stdout.flush()
    sys.stdout.write(f"Testing cmcdict version: {cmcdict.__version__}\n")
    sys.stdout.flush()

    sys.stdout.write("\nRunning get_metvar_metadata('TT') test...\n")
    sys.stdout.flush()
    result = cmcdict.get_metvar_metadata("TT")

    sys.stdout.write("\nExpected output:\n")
    sys.stdout.write(str(EXPECTED_OUTPUT) + "\n")
    sys.stdout.flush()

    sys.stdout.write("\nActual output:\n")
    sys.stdout.write(str(result) + "\n")
    sys.stdout.flush()

    if result == EXPECTED_OUTPUT:
        sys.stdout.write("\n✅ Test passed: Output matches expected result\n")
        sys.stdout.flush()
        return True
    else:
        sys.stdout.write("\n❌ Test failed: Output does not match expected result\n")
        sys.stdout.write("\nDifferences:\n")
        for key in EXPECTED_OUTPUT:
            if key not in result:
                sys.stdout.write(f"Missing key in result: {key}\n")
            elif result[key] != EXPECTED_OUTPUT[key]:
                sys.stdout.write(f"Mismatch for {key}:\n")
                sys.stdout.write(f"  Expected: {EXPECTED_OUTPUT[key]}\n")
                sys.stdout.write(f"  Got:      {result[key]}\n")
        sys.stdout.flush()
        return False


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
