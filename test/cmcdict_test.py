# -*- coding: utf-8 -*-
import pytest
import cmcdict

pytestmark = [pytest.mark.unit_tests]

def test_1():
    """nomvar wrong type """
    result = cmcdict.get_metvar_metadata(2,['description_short_en'])
    assert(result is None)


def test_2():
    """nomvar None"""
    result = cmcdict.get_metvar_metadata(nomvar = None, columns = cmcdict.__METVAR_METADATA_COLUMNS)
    assert(result is None)


def test_3():
    """nomvar valid"""
    result = cmcdict.get_metvar_metadata(nomvar = 'TT', columns = cmcdict.__METVAR_METADATA_COLUMNS)
    assert(result == {'nomvar': 'TT', 'usage': 'current', 'origin': '', 'date': '', 'type': 'real', 'description_short_en': 'Air temperature', 'description_short_fr': "Température de l'air", 'description_long_en': '', 'description_long_fr': '', 'units': '°C', 'min': '', 'max': '', 'codes': None, 'precision': '', 'magnitude': ''})

def test_4():
    """nomvar valid does not exist"""
    result = cmcdict.get_metvar_metadata(nomvar = '?*', columns = cmcdict.__METVAR_METADATA_COLUMNS)
    assert(result is None)

def test_5():
    """columns wrong type"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar = 'TT', columns = 1)


def test_6():
    """columns None"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar = 'TT', columns = None)
    
def test_7():
    """columns valid list"""
    result = cmcdict.get_metvar_metadata(nomvar = 'TT', columns = cmcdict.__METVAR_METADATA_COLUMNS)
    assert(result == {'nomvar': 'TT', 'usage': 'current', 'origin': '', 'date': '', 'type': 'real', 'description_short_en': 'Air temperature', 'description_short_fr': "Température de l'air", 'description_long_en': '', 'description_long_fr': '', 'units': '°C', 'min': '', 'max': '', 'codes': None, 'precision': '', 'magnitude': ''})

def test_8():
    """columns empty list"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar = 'TT', columns = [])


def test_9():
    """columns list wrong type"""
    with pytest.raises(TypeError):
        _ = cmcdict.get_metvar_metadata(nomvar = 'TT', columns = [1])

def test_10():
    """columns list invalid column"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar = 'TT', columns = ['1'])

def test_11():
    """columns list with nomvar """
    with pytest.raises(ValueError):
        _ = cmcdict.get_metvar_metadata(nomvar = 'TT', columns = ['nomvar', 'units'])
    

# # ______________________________________________________________________

# # def get_typvar_metadata(nomtype: str, columns: list = __TYPVAR_METADATA_COLUMNS)
def test_11():
    """nomtype wrong type """
    result = cmcdict.get_typvar_metadata(nomtype = 2, columns = cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert(result is None)


def test_12():
    """nomtype None"""
    result = cmcdict.get_typvar_metadata(nomtype = None, columns = cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert(result is None)


def test_13():
    """nomtype valid"""
    result = cmcdict.get_typvar_metadata(nomtype = 'R', columns = cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert(result == {'typvar': 'R', 'date': '', 'description_short_en': 'Analysis increment', 'description_short_fr': "Incrément d'analyse"})

def test_14():
    """nomtype valid does not exist"""
    result = cmcdict.get_typvar_metadata(nomtype = '?*', columns = cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert(result is None)

def test_15():
    """columns wrong type"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype = 'R', columns = 1)


def test_16():
    """columns None"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype = 'R', columns = None)

    
def test_17():
    """columns valid list"""
    result = cmcdict.get_typvar_metadata(nomtype = 'R', columns = cmcdict.__TYPVAR_METADATA_COLUMNS)
    assert(result == {'typvar': 'R', 'date': '', 'description_short_en': 'Analysis increment', 'description_short_fr': "Incrément d'analyse"})

def test_18():
    """columns empty list"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype = 'R', columns = [])


def test_19():
    """columns list wrong type"""
    with pytest.raises(TypeError):
        _ = cmcdict.get_typvar_metadata(nomtype = 'R', columns = [1])


def test_20():
    """columns list invalid column"""
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype = 'R', columns = ['1'])


def test_21():
    """columns list with nomtype """
    with pytest.raises(ValueError):
        _ = cmcdict.get_typvar_metadata(nomtype = 'R', columns = ['nomvar', 'units'])


def test_22():
    """test current vars"""
    with open('current_vars.txt', 'r') as f:
        vars = f.readlines()

    vars = [s.replace('\n','') for s in vars]

    for v in vars:
        data = cmcdict.get_metvar_metadata(nomvar = v, columns = ['units', 'description_short_en'])
        if data is None:
            assert(False)

def test_23():
    """test nomvar with a deprecated usage, success with allow all usages"""
    result = cmcdict.get_metvar_metadata(nomvar = 'UD', columns = cmcdict.__METVAR_METADATA_COLUMNS, usages= cmcdict.__METVAR_USAGES)
    assert(result == {'nomvar': 'UD', 'usage': 'deprecated', 'origin': '', 'date': '2021-06-30', 'type': 'real', 'description_short_en': 'U-component of the wind at anemometer level', 'description_short_fr': "Composante U du vent au niveau de l'anémomètre", 'description_long_en': 'Note, the variable UDST (IP1=1195) should be used instead of UD.', 'description_long_fr': 'Noter que la variable UDST (IP1=1195) devrait être utilisée au lieu de UD.', 'units': 'm/s', 'min': '', 'max': '', 'codes': None, 'precision': '', 'magnitude': ''})

def test_24():
    """test nomvar 'UD' with only 'current' usage allowd, failure UD has 'deprecated' usage. result is a dictionnary with 'None' for all keys."""
    result = cmcdict.get_metvar_metadata(nomvar = 'UD', columns = cmcdict.__METVAR_METADATA_COLUMNS, usages = ['current'])
    assert(result == {'nomvar': 'UD', 'usage': None, 'origin': None, 'date': None, 'type': None, 'description_short_en': None, 'description_short_fr': None, 'description_long_en': None, 'description_long_fr': None, 'units': None, 'min': None, 'max': None, 'codes': None, 'precision': None, 'magnitude': None})

def test_25():
    """test nomvar with only 'current' usage allowed, success UU has current usage"""
    result = cmcdict.get_metvar_metadata(nomvar = 'UU', columns = cmcdict.__METVAR_METADATA_COLUMNS, usages = ['current'])
    assert(result == {'nomvar': 'UU', 'usage': 'current', 'origin': '', 'date': '', 'type': 'real', 'description_short_en': 'U-component of the wind (along the X-axis of the grid)', 'description_short_fr': "Composante U du vent (selon l'axe des X sur la grille)", 'description_long_en': '', 'description_long_fr': '', 'units': 'kts', 'min': '', 'max': '', 'codes': None, 'precision': '', 'magnitude': ''})
