import os
import warnings
import xml.etree.ElementTree as ET
from functools import lru_cache
from glob import glob
from pathlib import Path
from typing import Union


class OpDictNotFoundException(Exception):
    pass

__KNOWN_CMC_CONSTANTS_DIR = Path('/home/smco502/datafiles/constants')
__VAR_DICT_FILE = Path('opdict/ops.variable_dictionary.xml')
__BASE_DIR = Path('/fs/ssm/eccc/cmo/cmoi/base')

@lru_cache(maxsize=None)
def __find_latest_date_folder() -> Union[Path, None]:
    """Finds the latest date folder within the given base directory.

    :param base_dir: the base directory to search
    :return: the latest date folder, or None if not found
    """
    # date_folders = [folder for folder in base_dir.iterdir() if folder.is_dir() and folder.name.isdigit()]
    date_folders = glob(f'{__BASE_DIR}/[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
    date_folders = [Path(f) for f in date_folders]
    return max(date_folders, default=None)

def __get_dict_file_from_ssm(latest_date_folder: str) -> Path:
    """get the op dictionary file path from the latest ssm package

    :param latest_date_folder: most recent ssm package path
    :type latest_date_folder: str
    :return: op dictionary file path
    :rtype: Path
    """
    op_dict_file = __KNOWN_CMC_CONSTANTS_DIR / __VAR_DICT_FILE
    env_file_path = __BASE_DIR / latest_date_folder / f"base_{latest_date_folder.stem}_rhel-8-amd64-64/src/environment.sh"
    if env_file_path.exists(): #os.path.exists(env_file_path):
        with open(env_file_path, 'r') as f:
            for line in f:
                if line.startswith("export CMCCONST="):
                    op_dict_file =  Path(line.strip().split("=")[1]) / __VAR_DICT_FILE
    return op_dict_file       
                
@lru_cache(maxsize=None)
def __find_ops_variable_dictionary() -> Path:
    """Finds the path to the operational dictionary XML file.

    :return: the path to the operational dictionary XML file
    """
    # /home/smco502/datafiles/constants
    constants_dir = os.getenv('CMCCONST', '')

    op_dict_file = __KNOWN_CMC_CONSTANTS_DIR / __VAR_DICT_FILE

    if constants_dir == '':
        warnings.warn("cmoi base ssm package not loaded, attemting to find definition else where", UserWarning)
        latest_date_folder = __find_latest_date_folder()
        if not latest_date_folder:
            return op_dict_file
        op_dict_file = __get_dict_file_from_ssm(latest_date_folder)
    else:
        op_dict_file = Path(constants_dir) / __VAR_DICT_FILE
    return op_dict_file

@lru_cache(maxsize=None)
def __parse_opt_dict() -> ET.ElementTree:
    """Parses the operational dictionary XML file and returns the root element.

    :return: the root element of the operational dictionary XML file
    """
    try:
        tree = ET.parse(__find_ops_variable_dictionary())
    except FileNotFoundError as e:
        warnings.warn(f"Operational dictionary XML file not found at {e.filename}.", UserWarning)
        return None
    return tree.getroot()



def __check_and_get(var: str, xml_elem: ET.Element, columns: list, nomvar_info: dict) -> None:
    """check if the var is in the requested columns and gets the var in the xml element

    :param var: variable to search for
    :type var: str
    :param xml_elem: xml element to search in
    :type xml_elem: ET.Element
    :param columns: The list of columns to retrieve from the optdict XML file
    :type columns: list
    :param nomvar_info: nomvar metadata
    :type nomvar_info: dict
    """
    if var in columns:
        value =  xml_elem.get(var)
        nomvar_info[var] =  '' if value is None else value.strip()
    

def __check_and_find(var: str, filter: str , xml_elem: ET.Element, columns: list, nomvar_info: dict) -> None:
    """check if the var is in the requested columns and finds the var in the xml element

    :param var: variable to search for
    :type var: str
    :param filter: xml serach filter
    :type filter: str
    :param xml_elem: xml element to search in
    :type xml_elem: ET.Element
    :param columns: The list of columns to retrieve from the optdict XML file
    :type columns: list
    :param nomvar_info: nomvar metadata
    :type nomvar_info: dict
    """
    if var in columns:
        value = xml_elem.find(filter)
        nomvar_info[var] = '' if value is None else str(value.text).strip()



def __process_codes(xml_elem: ET.Element, columns: list, nomvar_info: dict) -> None:
    """processes the codes for a type code in a nomvar

    :param xml_elem: xml element to search in
    :type xml_elem: ET.Element
    :param columns: The list of columns to retrieve from the optdict XML file
    :type columns: list
    :param nomvar_info: nomvar metadata
    :type nomvar_info: dict
    """
    if 'codes' in columns:
            # if type_element exists and its tag is either 'code' or 'logical'
        if xml_elem is not None and xml_elem.tag in ['code', 'logical']:
                # iterate over the value elements
            values = []
                
            for value_element in xml_elem.findall('value'):
                value = value_element.text

                values.append(f"{value}")

            meanings_with_lang =  [i.text for i in xml_elem.findall("meaning[@lang='en']")]
            meanings_without_lang =  [i.text for i in xml_elem.findall("meaning")]
                
            codes = []
            if (len(values) == len(meanings_with_lang)):
                for a,b in zip(values,meanings_with_lang):
                    codes.append(f'{a}:{b}')
            elif len(values) == len(meanings_without_lang)/2:
                half_index = len(meanings_without_lang) // 2
                first_half = meanings_without_lang[:half_index]
                second_half = meanings_without_lang[half_index:]
                for a,b,c in zip(values,first_half,second_half):
                    codes.append(f'{a}:{b}/{c}')
            elif len(values) == len(meanings_without_lang):
                codes = [f'{a}:{b}' for a,b in zip(values,meanings_without_lang)]

            nomvar_info['codes'] = ';'.join(codes)



def __process_type(measure_elem_children: list, columns: list, nomvar_info: dict) -> None:
    """processes the type from a metvar element in the op dict

    :param measure_elem_children: children of the measure element
    :type measure_elem_children: list
    :param columns: The list of columns to retrieve from the optdict XML file
    :type columns: list
    :return: the type of measure_element, either 'real', 'code', 'integer', 'logical', if exists
    :rtype: str
    """
    measure_type = ''
    if 'type' in columns:
        for child in measure_elem_children:
            if child.tag in ('real', 'code', 'integer', 'logical'):
                measure_type = child.tag
                break
        nomvar_info['type'] = measure_type


@lru_cache(maxsize=None)
def get_metvar_metadata(nomvar: str, columns: list =['origin', 'date', 'type', 'description_short_en','description_short_fr', 'description_long_en', 'description_long_fr','units', 'min', 'max', 'codes', 'precision', 'magnitude']) -> Union[dict, None]:
    """
    Retrieves metvar metadata information from a CMC optdict XML file for a given nomvar and columns.

    :param nomvar: The nomvar to search for in the optdict XML file.
    :type nomvar: str

    :param columns: The list of columns to retrieve from the optdict XML file. Default is ['origin', 'date', 'type', 'description_short_en','description_short_fr', 'description_long_en', 'description_long_fr','units', 'min', 'max', 'codes', 'precision', 'magnitude'].
    :type columns: list

    :return: A dictionary containing the metadata information for the given nomvar and columns.
    :rtype: dict

    :raises ValueError: If columns is not a list or has less than one element, or if nomvar is in columns, or if columns contains invalid column names.
    """
    allowed_columns = ['origin', 'date', 'type', 'description_short_en', 'description_short_fr', 'description_long_en', 'description_long_fr', 'units', 'min', 'max', 'codes', 'precision', 'magnitude']
    
    if not isinstance(columns, list) or len(columns) < 1:
        raise ValueError("Columns must be a list of at least 1 element")
        
    if 'nomvar' in columns:
        raise ValueError("nomvar must not be in columns")
        
    invalid_columns = set(columns) - set(allowed_columns)
    if invalid_columns:
        raise ValueError("Invalid columns: {}".format(", ".join(sorted(invalid_columns))))


    nomvar_info = { 'nomvar': nomvar }
    for col in columns: 
        nomvar_info[col] = None

    # Find the metvar element with the given nomvar
    cmc_dict_xml_root = __parse_opt_dict()
    if cmc_dict_xml_root is None:
        raise OpDictNotFoundException()

    nomvar_metvar = cmc_dict_xml_root.find(f".//metvar[nomvar='{nomvar}']")

    if nomvar_metvar is not None and nomvar_metvar.get('usage') == 'current':

        __check_and_get('origin', nomvar_metvar, columns, nomvar_info)

        __check_and_get('date', nomvar_metvar, columns, nomvar_info)

        measure_elem = nomvar_metvar.findall(".//measure/*")

        __check_and_find('precision', ".//precision", measure_elem[0], columns, nomvar_info)

        __check_and_find('magnitude', ".//magnitude", measure_elem[0], columns, nomvar_info)

        __process_type(measure_elem, columns, nomvar_info)

        __process_codes(measure_elem[0], columns, nomvar_info)

        __check_and_find('description_short_en', ".//short[@lang='en']", nomvar_metvar, columns, nomvar_info)

        __check_and_find('description_short_fr', ".//short[@lang='fr']", nomvar_metvar, columns, nomvar_info)

        __check_and_find('description_long_en', ".//long[@lang='en']", nomvar_metvar, columns, nomvar_info)

        __check_and_find('description_long_fr', ".//long[@lang='fr']", nomvar_metvar, columns, nomvar_info)
        
        __check_and_find('units', ".//units", nomvar_metvar, columns, nomvar_info)

        __check_and_find('min', ".//min", nomvar_metvar, columns, nomvar_info)

        __check_and_find('max', ".//max", nomvar_metvar, columns, nomvar_info)

    else:
        return None        
    return nomvar_info



@lru_cache(maxsize=None)
def get_typvar_metadata(nomtype: str, columns: list =['date', 'description_short_en','description_short_fr']) -> Union[dict, None]:
    """
    Retrieves typvar metadata information from a CMC optdict XML file for a given nomvar and columns.

    :param nomvar: The nomvar to search for in the optdict XML file.
    :type nomvar: str

    :param columns: The list of columns to retrieve from the optdict XML file. Default is ['date', 'description_short_en','description_short_fr'].
    :type columns: list

    :return: A dictionary containing the metadata information for the given nomvar and columns.
    :rtype: dict

    :raises ValueError: If columns is not a list or has less than one element, or if nomvar is in columns, or if columns contains invalid column names.
    """
    allowed_columns = ['date', 'description_short_en', 'description_short_fr']
    
    if not isinstance(columns, list) or len(columns) < 1:
        raise ValueError("Columns must be a list of at least 1 element")
        
    if 'nomtype' in columns:
        raise ValueError("nomtype must not be in columns")
        
    invalid_columns = set(columns) - set(allowed_columns)
    if invalid_columns:
        raise ValueError("Invalid columns: {}".format(", ".join(sorted(invalid_columns))))


    typvar_info = { 'typvar': nomtype }
    for col in columns: 
        typvar_info[col] = None

    # Find the metvar element with the given nomvar
    cmc_dict_xml_root = __parse_opt_dict()
    if cmc_dict_xml_root is None:
        raise OpDictNotFoundException()

    typvar_nomtype = cmc_dict_xml_root.find(f".//typvar[nomtype='{nomtype}']")

    if typvar_nomtype is not None and typvar_nomtype.get('usage') == 'current':

        __check_and_get('date', typvar_nomtype, columns, typvar_info)

        __check_and_find('description_short_en', ".//short[@lang='en']", typvar_nomtype, columns, typvar_info)

        __check_and_find('description_short_fr', ".//short[@lang='fr']", typvar_nomtype, columns, typvar_info)

    else:
        return None        
    return typvar_info
# tt_meta = get_metadata_from_optdict(nomvar = 'TT')
# es_meta = get_metadata_from_optdict(nomvar = 'ES')
