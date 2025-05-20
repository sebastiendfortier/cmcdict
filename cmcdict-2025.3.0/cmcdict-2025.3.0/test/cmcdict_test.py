# -*- coding: utf-8 -*-
import pytest
import cmcdict
import os

pytestmark = [pytest.mark.unit_tests]

# Get the test directory path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def test_01():
    """nomvar wrong type"""
    with pytest.raises(TypeError):
        _ = cmcdict.get_metvar_metadata(2, ["description_short_en"])


def test_02():
    """nomvar None"""
    with pytest.raises(TypeError):
        _ = cmcdict.get_metvar_metadata(nomvar=None, columns=cmcdict.__METVAR_METADATA_COLUMNS)


def test_03():
    """nomvar valid"""
    result = cmcdict.get_metvar_metadata(nomvar="TT", columns=cmcdict.__METVAR_METADATA_COLUMNS)
    assert result == {
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


def test_04():
    """nomvar valid does not exist"""
    result = cmcdict.get_metvar_metadata(nomvar="?*", columns=cmcdict.__METVAR_METADATA_COLUMNS)
    assert result is None


def test_05():
    """columns wrong type"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar="TT", columns=1)


def test_06():
    """columns None"""
    result = cmcdict.get_metvar_metadata(nomvar="TT", columns=None)
    assert result == {
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


def test_07():
    """columns valid list"""
    result = cmcdict.get_metvar_metadata(nomvar="TT", columns=cmcdict.__METVAR_METADATA_COLUMNS)
    assert result == {
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


def test_08():
    """columns empty list"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar="TT", columns=[])


def test_09():
    """columns list wrong type"""
    with pytest.raises(TypeError):
        _ = cmcdict.get_metvar_metadata(nomvar="TT", columns=[1])


def test_10():
    """columns list invalid column"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar="TT", columns=["1"])


def test_11():
    """columns list with nomvar"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar="TT", columns=["nomvar", "units"])


def test_12():
    """nomtype wrong type"""
    result = cmcdict.get_typvar_metadata(nomtype=2, columns=cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert result is None


def test_13():
    """nomtype None"""
    result = cmcdict.get_typvar_metadata(nomtype=None, columns=cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert result is None


def test_14():
    """nomtype valid"""
    result = cmcdict.get_typvar_metadata(nomtype="R", columns=cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert result == {
        "typvar": "R",
        "date": "",
        "description_short_en": "Analysis increment",
        "description_short_fr": "Incrément d'analyse",
    }


def test_15():
    """nomtype valid does not exist"""
    result = cmcdict.get_typvar_metadata(nomtype="?*", columns=cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert result is None


def test_16():
    """columns wrong type"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype="R", columns=1)


def test_17():
    """columns None"""
    result = cmcdict.get_typvar_metadata(nomtype="R", columns=None)
    assert result == {
        "typvar": "R",
        "date": "",
        "description_short_en": "Analysis increment",
        "description_short_fr": "Incrément d'analyse",
    }


def test_18():
    """columns valid list"""
    result = cmcdict.get_typvar_metadata(nomtype="R", columns=cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert result == {
        "typvar": "R",
        "date": "",
        "description_short_en": "Analysis increment",
        "description_short_fr": "Incrément d'analyse",
    }


def test_19():
    """columns empty list"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype="R", columns=[])


def test_20():
    """columns list wrong type"""
    with pytest.raises(TypeError):
        _ = cmcdict.get_typvar_metadata(nomtype="R", columns=[1])


def test_21():
    """columns list invalid column"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype="R", columns=["1"])


def test_22():
    """columns list with nomtype"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype="R", columns=["nomvar", "units"])


def test_23():
    """test current vars"""
    current_vars_path = os.path.join(TEST_DIR, "current_vars.txt")
    with open(current_vars_path, "r") as f:
        vars = f.readlines()

    vars = [s.replace("\n", "") for s in vars]

    # Use batch processing to get metadata for all variables at once
    results = cmcdict.get_metvar_metadata(vars, columns=["units", "description_short_en"])

    # Check that all variables have metadata
    for v in vars:
        assert results[v] is not None, f"No metadata found for variable {v}"


def test_24():
    """test nomvar with a current usage, success with allow all usages"""
    result = cmcdict.get_metvar_metadata(
        nomvar="UD", columns=cmcdict.__METVAR_METADATA_COLUMNS, usages=cmcdict.__METVAR_USAGES
    )
    assert result == {
        "nomvar": "UD",
        "usage": "current",
        "origin": "",
        "date": "2024-09-17",
        "measure_type": "real",
        "description_short_en": "U-component of the wind at anemometer level",
        "description_short_fr": "Composante U du vent au niveau de l'anémomètre",
        "description_long_en": "",
        "description_long_fr": "",
        "units": "m/s",
        "min": "",
        "max": "",
        "codes": None,
        "precision": "",
        "magnitude": "",
    }


def test_25():
    """test nomvar 'UD' with only 'current' usage allowed, success UD has current usage"""
    result = cmcdict.get_metvar_metadata(nomvar="UD", columns=cmcdict.__METVAR_METADATA_COLUMNS, usages=["current"])
    assert result == {
        "nomvar": "UD",
        "usage": "current",
        "origin": "",
        "date": "2024-09-17",
        "measure_type": "real",
        "description_short_en": "U-component of the wind at anemometer level",
        "description_short_fr": "Composante U du vent au niveau de l'anémomètre",
        "description_long_en": "",
        "description_long_fr": "",
        "units": "m/s",
        "min": "",
        "max": "",
        "codes": None,
        "precision": "",
        "magnitude": "",
    }


def test_26():
    """test nomvar with only 'current' usage allowed, success UU has current usage"""
    result = cmcdict.get_metvar_metadata(nomvar="UU", columns=cmcdict.__METVAR_METADATA_COLUMNS, usages=["current"])
    assert result == {
        "nomvar": "UU",
        "usage": "current",
        "origin": "",
        "date": "",
        "measure_type": "real",
        "description_short_en": "U-component of the wind (along the X-axis of the grid)",
        "description_short_fr": "Composante U du vent (selon l'axe des X sur la grille)",
        "description_long_en": "",
        "description_long_fr": "",
        "units": "kts",
        "min": "",
        "max": "",
        "codes": None,
        "precision": "",
        "magnitude": "",
    }


def test_27():
    """test nomvar with ip1 specified, success"""
    result = cmcdict.get_metvar_metadata(
        nomvar="UDST", ip1="1196", columns=["description_short_en", "description_short_fr"]
    )
    assert result == {
        "nomvar": "UDST",
        "description_short_en": "U-component of the wind at anemometer level (Sea Ice)",
        "description_short_fr": "Composante U du vent au niveau de l'anémomètre (Glace Marine)",
    }


def test_28():
    """test nomvar with ip1 specified but not found"""
    result = cmcdict.get_metvar_metadata(nomvar="UDST", ip1="9999", columns=["description_short_en"])
    assert result is None


def test_29():
    """test nomvar with multiple definitions but no ip1 attributes - should return first one with most recent date"""
    result = cmcdict.get_metvar_metadata(nomvar="TT", columns=["description_short_en", "date"])
    assert result["nomvar"] == "TT"
    assert result["description_short_en"] == "Air temperature"


def test_30():
    """test nomvar with multiple definitions with same date but no ip1 - should return first one"""
    result = cmcdict.get_metvar_metadata(nomvar="AP", columns=["description_short_en", "date"])
    assert result["nomvar"] == "AP"
    assert result["description_short_en"] == "Planetary albedo"


def test_31():
    """test nomvar with no dates - should return first current metadata"""
    result = cmcdict.get_metvar_metadata(nomvar="UU", columns=["description_short_en", "date"])
    assert result["nomvar"] == "UU"
    assert result["date"] == ""  # Verify date is empty
    assert result["description_short_en"] == "U-component of the wind (along the X-axis of the grid)"


def test_32():
    """test ip1 parameter type validation - should accept both string and int"""
    # Test with string
    result1 = cmcdict.get_metvar_metadata(nomvar="UDST", ip1="1196", columns=["description_short_en"])
    assert result1 is not None
    assert result1["description_short_en"] == "U-component of the wind at anemometer level (Sea Ice)"

    # Test with integer
    result2 = cmcdict.get_metvar_metadata(nomvar="UDST", ip1=1196, columns=["description_short_en"])
    assert result2 is not None
    assert result2["description_short_en"] == "U-component of the wind at anemometer level (Sea Ice)"

    # Test with float - should work since it's converted to int
    result3 = cmcdict.get_metvar_metadata(nomvar="UDST", ip1=1196.0, columns=["description_short_en"])
    assert result3 is not None
    assert result3["description_short_en"] == "U-component of the wind at anemometer level (Sea Ice)"


def test_33():
    """test nomvar with multiple definitions, some with ip1, some without - should return dictionary of ip1 definitions"""
    # First get a definition with specific ip1
    result1 = cmcdict.get_metvar_metadata(nomvar="UDST", ip1="1196", columns=["description_short_en"])
    assert result1 is not None
    assert result1["description_short_en"] == "U-component of the wind at anemometer level (Sea Ice)"

    # Then get all definitions - should return a dictionary keyed by ip1
    result2 = cmcdict.get_metvar_metadata(nomvar="UDST", columns=["description_short_en"])
    assert isinstance(result2, dict)
    assert "1196" in result2
    assert "1195" in result2
    assert result2["1196"]["description_short_en"] == "U-component of the wind at anemometer level (Sea Ice)"
    assert result2["1195"]["description_short_en"] == "U-component of the wind at anemometer level (Aggregated)"


def test_34():
    """test with invalid usages parameter"""
    with pytest.raises(ValueError) as exc_info:
        _ = cmcdict.get_metvar_metadata(nomvar="TT", usages=["invalid_usage"])
    assert "invalid usage" in str(exc_info.value).lower()


def test_35():
    """test with empty usages list"""
    with pytest.raises(ValueError) as exc_info:
        _ = cmcdict.get_metvar_metadata(nomvar="TT", usages=[])
    assert "usages cannot be empty" in str(exc_info.value)


def test_36():
    """test with code type variable"""
    result = cmcdict.get_metvar_metadata(nomvar="GS", columns=["codes", "measure_type"])
    print(result)
    print(result["codes"])
    assert result["measure_type"] == "code"
    assert "sol" in result["codes"]
    assert "eau" in result["codes"]
    assert "neige" in result["codes"]
    assert "glace" in result["codes"]


def test_37():
    """test with logical type variable"""
    result = cmcdict.get_metvar_metadata(nomvar="OBSE", columns=["codes", "measure_type"])
    assert result["measure_type"] == "logical"
    assert "0:Not observed" in result["codes"]
    assert "1:Observed" in result["codes"]


def test_38():
    """test nomvar with multiple definitions but no ip1 - should return most recent one"""
    result = cmcdict.get_metvar_metadata(nomvar="TT", columns=["description_short_en", "date"])
    assert isinstance(result, dict)
    assert "nomvar" in result  # Single definition
    assert result["description_short_en"] == "Air temperature"


def test_39():
    """test nomvar with multiple definitions with same date but no ip1 - should return first one"""
    result = cmcdict.get_metvar_metadata(nomvar="AP", columns=["description_short_en", "date"])
    assert isinstance(result, dict)
    assert "nomvar" in result  # Single definition
    assert result["description_short_en"] == "Planetary albedo"


def test_40():
    """test nomvar with ip3 specified, success"""
    result = cmcdict.get_metvar_metadata(nomvar="QO1", ip3=0, columns=["description_short_en", "description_short_fr"])
    assert result == {
        "nomvar": "QO1",
        "description_short_en": "Outflow at the end of time-step (final value)",
        "description_short_fr": "Débit sortant à la fin du pas de temps (valeur finale)",
    }


def test_41():
    """test nomvar with ip3 specified but not found"""
    result = cmcdict.get_metvar_metadata(nomvar="QO1", ip3="999", columns=["description_short_en"])
    assert result is None


def test_42():
    """test nomvar with multiple ip3 definitions - should return dictionary of ip3 definitions"""
    result = cmcdict.get_metvar_metadata(nomvar="QO1", columns=["description_short_en"])
    assert isinstance(result, dict)
    assert "0" in result
    assert "10" in result
    assert "20" in result
    assert "30" in result
    assert result["0"]["description_short_en"] == "Outflow at the end of time-step (final value)"
    assert result["10"]["description_short_en"] == "Outflow at the end of time-step (raw value)"
    assert result["20"]["description_short_en"] == "Outflow at the end of time-step (removed by a diversion)"
    assert result["30"]["description_short_en"] == "Outflow at the end of time-step (removed for irrigation)"


def test_43():
    """test ip3 parameter type validation - should accept both string and int"""
    # Test with string
    result1 = cmcdict.get_metvar_metadata(nomvar="QO1", ip3="0", columns=["description_short_en"])
    assert result1 is not None
    assert result1["description_short_en"] == "Outflow at the end of time-step (final value)"

    # Test with integer
    result2 = cmcdict.get_metvar_metadata(nomvar="QO1", ip3=0, columns=["description_short_en"])
    assert result2 is not None
    assert result2["description_short_en"] == "Outflow at the end of time-step (final value)"

    # Test with float - should work since it's converted to int
    result3 = cmcdict.get_metvar_metadata(nomvar="QO1", ip3=0.0, columns=["description_short_en"])
    assert result3 is not None
    assert result3["description_short_en"] == "Outflow at the end of time-step (final value)"


def test_44():
    """test that ip1 and ip3 are ignored when not relevant for the variable"""
    # Test with TT which doesn't use ip1 or ip3
    result1 = cmcdict.get_metvar_metadata(
        nomvar="TT",
        ip1="1234",
        ip3="5678",
        columns=["description_short_en"],  # Should be ignored  # Should be ignored
    )
    assert result1 is not None
    assert result1["description_short_en"] == "Air temperature"

    # Test with UDST which uses ip1 but not ip3
    result2 = cmcdict.get_metvar_metadata(
        nomvar="UDST",
        ip1="1196",
        ip3="5678",
        columns=["description_short_en"],  # Should be used  # Should be ignored
    )
    assert result2 is not None
    assert result2["description_short_en"] == "U-component of the wind at anemometer level (Sea Ice)"

    # Test with QO1 which uses ip3 but not ip1
    result3 = cmcdict.get_metvar_metadata(
        nomvar="QO1",
        ip1="1234",
        ip3="0",
        columns=["description_short_en"],  # Should be ignored  # Should be used
    )
    assert result3 is not None
    assert result3["description_short_en"] == "Outflow at the end of time-step (final value)"


def test_45():
    """test batch processing with simple variables"""
    result = cmcdict.get_metvar_metadata(["TT", "UU", "VV"], columns=["description_short_en"])
    assert len(result) == 3
    assert result["TT"]["description_short_en"] == "Air temperature"
    assert result["UU"]["description_short_en"] == "U-component of the wind (along the X-axis of the grid)"
    assert result["VV"]["description_short_en"] == "V-component of the wind (along the Y-axis of the grid)"


def test_46():
    """test batch processing with IP1 variables"""
    result = cmcdict.get_metvar_metadata(["UDST", "QO1"], columns=["description_short_en"])
    assert len(result) == 2
    assert isinstance(result["UDST"], dict)
    assert "1196" in result["UDST"]
    assert "1195" in result["UDST"]
    assert result["UDST"]["1196"]["description_short_en"] == "U-component of the wind at anemometer level (Sea Ice)"


def test_47():
    """test batch processing with IP3 variables"""
    result = cmcdict.get_metvar_metadata(["QO1", "QO2"], columns=["description_short_en"])
    assert len(result) == 2
    assert isinstance(result["QO1"], dict)
    assert "0" in result["QO1"]
    assert "10" in result["QO1"]
    assert result["QO1"]["0"]["description_short_en"] == "Outflow at the end of time-step (final value)"


def test_48():
    """test batch processing with mixed variable types"""
    result = cmcdict.get_metvar_metadata(["TT", "UDST", "QO1", "INVALID"], columns=["description_short_en"])
    assert len(result) == 4
    # Regular variable
    assert isinstance(result["TT"], dict)
    assert "description_short_en" in result["TT"]
    # IP1 variable
    assert isinstance(result["UDST"], dict)
    assert "1196" in result["UDST"]
    # IP3 variable
    assert isinstance(result["QO1"], dict)
    assert "0" in result["QO1"]
    # Invalid variable
    assert result["INVALID"] is None


def test_49():
    """test batch processing with invalid inputs"""
    # Test with None in nomvars list
    result1 = cmcdict.get_metvar_metadata(["TT", None, "UU"], columns=["description_short_en"])
    assert result1["TT"] is not None
    assert result1[None] is None
    assert result1["UU"] is not None

    # Test with invalid type in nomvars list
    result2 = cmcdict.get_metvar_metadata(["TT", 123, "UU"], columns=["description_short_en"])
    assert result2["TT"] is not None
    assert result2[123] is None
    assert result2["UU"] is not None


def test_50():
    """test batch processing performance with large number of variables"""
    # Create a list of 100 variables (mix of valid and invalid)
    large_var_list = ["TT", "UU", "VV"] * 33 + ["INVALID"]
    result = cmcdict.get_metvar_metadata(large_var_list, columns=["description_short_en", "units"])

    # Check that all unique variables are present
    assert "TT" in result
    assert "UU" in result
    assert "VV" in result
    assert "INVALID" in result

    # Check that the total number of unique variables is correct
    assert len(result) == 4  # TT, UU, VV, and INVALID

    # Check that the metadata for each valid variable is correct
    assert result["TT"]["description_short_en"] == "Air temperature"
    assert result["TT"]["units"] == "°C"
    assert result["UU"]["description_short_en"] == "U-component of the wind (along the X-axis of the grid)"
    assert result["UU"]["units"] == "kts"
    assert result["VV"]["description_short_en"] == "V-component of the wind (along the Y-axis of the grid)"
    assert result["VV"]["units"] == "kts"
    assert result["INVALID"] is None

    # Test that we can handle a large number of unique variables
    unique_vars = [f"VAR{i}" for i in range(100)]
    large_unique_result = cmcdict.get_metvar_metadata(unique_vars, columns=["description_short_en"])
    assert len(large_unique_result) == 100  # Each variable should be present in result
    assert all(var in large_unique_result for var in unique_vars)  # All variables should be in result
