#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# Get the test directory path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the root directory path (parent of test dir)
ROOT_DIR = os.path.dirname(TEST_DIR)

# Add the root directory to Python path to ensure cmcdict can be imported
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Print diagnostic information
print("\nPath Information:")
print(f"Test Directory: {TEST_DIR}")
print(f"Root Directory: {ROOT_DIR}")
print(f"Python Path: {sys.path}\n")

import cmcdict
from pprint import pprint

# Define metadata columns (same as in cmcdict module)
METVAR_METADATA_COLUMNS = [
    "usage",
    "origin",
    "date",
    "type",
    "description_short_en",
    "description_short_fr",
    "description_long_en",
    "description_long_fr",
    "units",
    "min",
    "max",
    "codes",
    "precision",
    "magnitude",
]

TYPVAR_METADATA_COLUMNS = ["date", "description_short_en", "description_short_fr"]

METVAR_USAGES = ["current"]


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f" {title} ")
    print("=" * 80 + "\n")


def print_result(description, result):
    """Print a test result with description"""
    print("-" * 40)
    print(f"Test: {description}")
    print(f"Result:")
    pprint(result)
    print()


def main():
    print_section("Basic API Usage - Single Variables")

    # Test simple variable lookup
    print_result(
        "Get metadata for temperature (TT)", cmcdict.get_metvar_metadata(nomvar="TT", columns=METVAR_METADATA_COLUMNS)
    )

    # Test non-existent variable
    print_result(
        "Get metadata for non-existent variable",
        cmcdict.get_metvar_metadata(nomvar="?*", columns=METVAR_METADATA_COLUMNS),
    )

    print_section("Error Cases")

    # Test wrong type for nomvar
    print_result(
        "Try to get metadata with wrong type (number instead of string)",
        cmcdict.get_metvar_metadata(2, ["description_short_en"]),
    )

    # Test None nomvar
    print_result(
        "Try to get metadata with None nomvar",
        cmcdict.get_metvar_metadata(nomvar=None, columns=METVAR_METADATA_COLUMNS),
    )

    try:
        cmcdict.get_metvar_metadata(nomvar="TT", columns=1)
    except ValueError as e:
        print_result("Try to get metadata with wrong columns type (number)", str(e))

    try:
        cmcdict.get_metvar_metadata(nomvar="TT", columns=[])
    except ValueError as e:
        print_result("Try to get metadata with empty columns list", str(e))

    print_section("IP1/IP3 Examples")

    # Test variable with IP1
    print_result(
        "Get metadata for UDST with IP1=1196",
        cmcdict.get_metvar_metadata(
            nomvar="UDST", ip1="1196", columns=["description_short_en", "description_short_fr"]
        ),
    )

    # Test variable with IP3
    print_result(
        "Get metadata for QO1 with IP3=0",
        cmcdict.get_metvar_metadata(nomvar="QO1", ip3=0, columns=["description_short_en"]),
    )

    # Test IP values being ignored when not relevant
    print_result(
        "Get metadata for TT with IP values (should be ignored)",
        cmcdict.get_metvar_metadata(nomvar="TT", ip1="1234", ip3="5678", columns=["description_short_en"]),
    )

    print_section("Batch Processing Examples")

    # Test batch processing with simple variables
    print_result(
        "Get metadata for multiple simple variables",
        cmcdict.get_metvar_metadata(["TT", "UU", "VV"], columns=["description_short_en"]),
    )

    # Test batch processing with IP1 variables
    print_result(
        "Get metadata for multiple variables with IP1",
        cmcdict.get_metvar_metadata(["UDST", "QO1"], columns=["description_short_en"]),
    )

    # Test batch processing with mixed types
    print_result(
        "Get metadata for mixed variable types including invalid",
        cmcdict.get_metvar_metadata(["TT", "UDST", "QO1", "INVALID"], columns=["description_short_en"]),
    )

    print_section("Type Variables (TYPVAR) Examples")

    # Test type variable metadata
    print_result(
        "Get metadata for type variable 'R'",
        cmcdict.get_typvar_metadata(nomtype="R", columns=["description_short_en", "description_short_fr"]),
    )

    print_section("Usage Parameter Examples")

    # Note: We want to:
    # 1. Return data for variables even if they don't have a usage attribute
    # 2. Default to "current" when usage is not specified
    # 3. Allow filtering by usage when it is present

    # Test with default usage (current)
    print_result(
        "Get metadata with default usage (current) - should return variables with usage='current' OR no usage",
        cmcdict.get_metvar_metadata(nomvar="UD", columns=["usage", "description_short_en"]),
    )

    # Test with explicit current usage
    print_result(
        "Get metadata with explicit current usage - should return variables with usage='current' OR no usage",
        cmcdict.get_metvar_metadata(nomvar="UD", columns=["usage", "description_short_en"], usages=["current"]),
    )

    # Test with all possible usage values
    all_usages = ["current", "future", "obsolete", "incomplete", "deprecated"]
    print_result(
        "Get metadata allowing all valid usages - should return ALL variables regardless of usage",
        cmcdict.get_metvar_metadata(nomvar="TT", columns=["usage", "description_short_en"], usages=all_usages),
    )

    # Test variables with different usages in batch
    print_result(
        "Get metadata for multiple variables with all usage values",
        cmcdict.get_metvar_metadata(
            nomvar=["TT", "UU", "VV", "ABCD"],  # Mix of variables
            columns=["usage", "description_short_en"],
            usages=all_usages,
        ),
    )

    # Test variables that might not have usage attribute
    print_result(
        "Get metadata for variables that might not have usage attribute",
        cmcdict.get_metvar_metadata(
            nomvar=["TT", "UU", "VV", "ABCD"],  # Mix of variables, some might not have usage
            columns=["usage", "description_short_en"],
            usages=["current"],  # Should still return variables without usage attribute
        ),
    )

    # Test with invalid usage
    try:
        result = cmcdict.get_metvar_metadata(
            nomvar="UD", columns=["usage", "description_short_en"], usages=["invalid_usage"]
        )
    except ValueError as e:
        print_result("Try to get metadata with invalid usage", str(e))

    # Test with empty usage list
    try:
        result = cmcdict.get_metvar_metadata(nomvar="UD", columns=["usage", "description_short_en"], usages=[])
    except ValueError as e:
        print_result("Try to get metadata with empty usage list", str(e))

    # Test with None usage
    try:
        result = cmcdict.get_metvar_metadata(
            nomvar="TT",
            columns=["usage", "description_short_en"],
            usages=None,  # Try with None usage
        )
    except ValueError as e:
        print_result("Try to get metadata with None usage", str(e))

    print_section("Large Scale Tests")

    # Test with current_vars.txt
    current_vars_path = os.path.join(TEST_DIR, "current_vars.txt")

    print("File Path Information:")
    print(f"Attempting to read from: {current_vars_path}")
    print(f"File exists: {os.path.exists(current_vars_path)}")
    print(f"Current working directory: {os.getcwd()}\n")

    try:
        with open(current_vars_path, "r") as f:
            vars = [s.strip() for s in f.readlines()]

        print(f"Successfully read {len(vars)} variables from current_vars.txt")
        print("First 5 variables:", vars[:5])
        print("\nGetting metadata for all variables...")

        results = cmcdict.get_metvar_metadata(vars, columns=["units", "description_short_en"])

        print(f"\nResults for first 5 variables:")
        for var in vars[:5]:
            print(f"\n{var}:")
            pprint(results[var])

    except FileNotFoundError:
        print(f"ERROR: Could not find {current_vars_path}")
        print("Make sure you're running the script from either:")
        print(f"  1. The root directory: {ROOT_DIR}")
        print(f"  2. The test directory: {TEST_DIR}")
    except Exception as e:
        print(f"ERROR reading file: {str(e)}")

    # Test with large number of variables
    large_var_list = ["TT", "UU", "VV"] * 33 + ["INVALID"]
    print(f"\nTesting with {len(large_var_list)} variables (repeated TT, UU, VV + INVALID)")

    result = cmcdict.get_metvar_metadata(large_var_list, columns=["description_short_en"])

    print("\nUnique results:")
    pprint(result)

    # Test with many unique variables
    unique_vars = [f"VAR{i}" for i in range(100)]
    print(f"\nTesting with {len(unique_vars)} unique variables (VAR0 through VAR99)")

    large_unique_result = cmcdict.get_metvar_metadata(unique_vars, columns=["description_short_en"])

    print(f"Got results for {len(large_unique_result)} variables")
    print("First 5 results:")
    for var in unique_vars[:5]:
        print(f"{var}: {large_unique_result[var]}")


if __name__ == "__main__":
    main()
