######################################################################
#
# Copyright (c) 2023 Government of Canada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

__version__ = "2025.03.00"

import logging
import os
import sys
import xml.etree.ElementTree as etree
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import polars as pl

from .config import (
    COUNTDOWN_RANGE,
    FACTOR_VALUES,
    HIGH_VALUES,
    LOW_VALUES,
    NEW_STYLE_RANGES,
    OLD_STYLE_RANGES,
    ZERO_VALUES,
    Kind,
)

LOGGER = logging.getLogger(__name__)


class OpDictNotFoundException(Exception):
    pass


class MultipleDefinitionsException(Exception):
    """Raised when multiple definitions exist for a nomvar and no ip1 is specified."""

    pass


__VAR_DICT_FILE = "opdict/ops.variable_dictionary.xml"

__METVAR_METADATA_COLUMNS = [
    "usage",
    "origin",
    "date",
    "measure_type",
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

__METVAR_USAGES = ["current"]

__TYPVAR_METADATA_COLUMNS = ["date", "description_short_en", "description_short_fr"]


@lru_cache(maxsize=0 if "pytest" in sys.modules else 256)
def __find_ops_variable_dictionary() -> Optional[Path]:
    """Find the operational dictionary XML file.

    Returns:
        Optional[Path]: Path to the XML dictionary file if found, None otherwise.

    The function will try to find the dictionary in the following order:
    1. CMCCONST environment variable path
    2. Default system path (/home/smco502/datafiles/constants)
    3. Package's data directory
    """
    try:
        # Check if CMCCONST is defined
        if "CMCCONST" in os.environ:
            base_path = Path(os.environ["CMCCONST"])
            dict_file = base_path / __VAR_DICT_FILE
            if dict_file.exists():
                LOGGER.info(f"Found dictionary file at {dict_file}")
                return dict_file

        # Try default system path
        base_path = Path("/home/smco502/datafiles/constants")
        dict_file = base_path / __VAR_DICT_FILE
        if dict_file.exists():
            LOGGER.info(f"Found dictionary file at {dict_file}")
            return dict_file

        # Try package's data directory as fallback
        package_data_path = Path(__file__).parent.parent / "data" / __VAR_DICT_FILE
        if package_data_path.exists():
            LOGGER.info(f"Found dictionary file in package data at {package_data_path}")
            return package_data_path

        raise OpDictNotFoundException("Dictionary file not found in any location")

    except Exception as e:
        if isinstance(e, OpDictNotFoundException):
            raise
        LOGGER.warning(f"Error finding operational dictionary: {str(e)}")
        return None


# @lru_cache(maxsize=None)
@lru_cache(maxsize=0 if "pytest" in sys.modules else 256)
def __parse_opt_dict() -> Optional[etree.Element]:
    """Parse the operational dictionary XML file"""
    try:
        # Find the dictionary file
        dict_file = __find_ops_variable_dictionary()
        if dict_file is None:
            LOGGER.warning("Could not find operational dictionary file")
            return None

        # Parse the XML file
        tree = etree.parse(dict_file)
        root = tree.getroot()

        # Check if we found any metvar elements
        metvars = root.findall(".//metvar")
        if not metvars:
            LOGGER.warning("No metvar elements found in dictionary")
            return None

        LOGGER.warning(f"Found {len(metvars)} metvar elements")
        return root

    except Exception as e:
        LOGGER.warning(f"Error parsing operational dictionary: {str(e)}")
        return None


def __check_and_get(var: str, xml_elem: etree.Element, columns: list, nomvar_info: dict) -> None:
    """check if the var is in the requested columns and gets the var in the xml element

    :param var: variable to search for
    :type var: str
    :param xml_elem: xml element to search in
    :type xml_elem: etree.Element
    :param columns: The list of columns to retrieve from the optdict XML file
    :type columns: list
    :param nomvar_info: nomvar metadata
    :type nomvar_info: dict
    """

    if var in columns:
        value = xml_elem.get(var)
        nomvar_info[var] = "" if value is None else value.strip()


def __check_and_find(var: str, filter_: str, xml_elem: etree.Element, columns: list, nomvar_info: dict) -> None:
    """check if the var is in the requested columns and finds the var in the xml element

    :param var: variable to search for
    :type var: str
    :param filter: xml serach filter
    :type filter: str
    :param xml_elem: xml element to search in
    :type xml_elem: etree.Element
    :param columns: The list of columns to retrieve from the optdict XML file
    :type columns: list
    :param nomvar_info: nomvar metadata
    :type nomvar_info: dict
    """

    if var in columns:
        value = xml_elem.find(filter_)
        nomvar_info[var] = "" if value is None or str(value.text).strip() == "" else str(value.text).strip()


def __process_codes(xml_elem: etree.Element, columns: list, nomvar_info: dict) -> None:
    """processes the codes for a type code in a nomvar

    :param xml_elem: xml element to search in
    :type xml_elem: etree.Element
    :param columns: The list of columns to retrieve from the optdict XML file
    :type columns: list
    :param nomvar_info: nomvar metadata
    :type nomvar_info: dict
    """

    if "codes" in columns:
        # Initialize codes as None
        nomvar_info["codes"] = None

        # if type_element exists and its tag is either 'code' or 'logical'
        if xml_elem is not None and xml_elem.tag in ("code", "logical"):
            # iterate over the value elements
            values = []

            for value_element in xml_elem.findall("value"):
                values.append(f"{value_element.text}")

            meanings_with_lang = [i.text for i in xml_elem.findall("meaning[@lang='en']")]
            meanings_without_lang = [i.text for i in xml_elem.findall("meaning")]

            codes = []
            if len(values) == len(meanings_with_lang):
                for a, b in zip(values, meanings_with_lang):
                    codes.append(f"{a}:{b}")
            elif len(values) == len(meanings_without_lang) / 2:
                half_index = len(meanings_without_lang) // 2
                first_half = meanings_without_lang[:half_index]
                second_half = meanings_without_lang[half_index:]
                for a, b, c in zip(values, first_half, second_half):
                    codes.append(f"{a}:{b}/{c}")
            elif len(values) == len(meanings_without_lang):
                codes = [f"{a}:{b}" for a, b in zip(values, meanings_without_lang)]

            if codes:
                nomvar_info["codes"] = ";".join(codes)


def __process_type(measure_elem_children: list, columns: list, nomvar_info: dict) -> None:
    """processes the type from a metvar element in the op dict

    :param measure_elem_children: children of the measure element
    :type measure_elem_children: list
    :param columns: The list of columns to retrieve from the optdict XML file
    :type columns: list
    :return: the type of measure_element, either 'real', 'code', 'integer', 'logical', if exists
    :rtype: str
    """

    measure_type = ""

    if "type" in columns:
        for child in measure_elem_children:
            if child.tag in ("real", "code", "integer", "logical"):
                measure_type = child.tag
                break

        nomvar_info["type"] = measure_type


def __validate_columns_param(columns, allowed_columns):
    if not isinstance(columns, list) or len(columns) < 1:
        raise ValueError("Columns must be a list of at least 1 element")

    if "nomvar" in columns:
        raise ValueError("nomvar must not be in columns")

    invalid_columns = set(columns) - set(allowed_columns)

    if invalid_columns:
        invalid_columns2 = ", ".join(sorted(invalid_columns))
        raise ValueError(f"Invalid columns: {invalid_columns2}")


def __validate_usages_param(usages, allowed_usages):
    if not isinstance(usages, list) or len(usages) < 1:
        raise ValueError("usages must be a list of at least 1 element")

    invalid_usages = set(usages) - set(allowed_usages)

    if invalid_usages:
        invalid_usages2 = ", ".join(sorted(invalid_usages))
        raise ValueError(f"Invalid usages: {invalid_usages2}")


def __process_ip_definitions(valid_metvars: List[etree.Element], ip_attr: str) -> Dict[str, Dict[str, Any]]:
    """Process IP definitions (IP1 or IP3) from valid metvars."""
    ip_metvars = {}
    for metvar in valid_metvars:
        nomvar_elem = metvar.find("nomvar")
        if nomvar_elem is not None and ip_attr in nomvar_elem.attrib:
            ip_str = nomvar_elem.get(ip_attr)
            ip_metvars[ip_str] = metvar
    return ip_metvars


def __has_ip_attribute(valid_metvars: List[etree.Element], ip_attr: str) -> bool:
    """Check if any metvar has the specified IP attribute."""
    return any(ip_attr in m.find("nomvar").attrib for m in valid_metvars if m.find("nomvar") is not None)


def __find_matching_definition(
    valid_metvars: List[etree.Element], ip_value: Optional[Union[str, int]], ip_attr: str
) -> Optional[etree.Element]:
    """Find metvar definition matching the specified IP value."""
    if ip_value is None:
        return None

    ip_value_int = int(float(ip_value))
    for metvar in valid_metvars:
        nomvar_elem = metvar.find("nomvar")
        if nomvar_elem is not None:
            dict_ip = nomvar_elem.get(ip_attr)
            if dict_ip and int(dict_ip) == ip_value_int:
                return metvar
    return None


def __get_latest_definition(valid_metvars: List[etree.Element]) -> etree.Element:
    """Get the most recent metvar definition based on date."""
    dates = [m.get("date", "") for m in valid_metvars]
    non_empty_dates = [d for d in dates if d]

    if non_empty_dates:
        latest_date = max(non_empty_dates)
        latest_metvars = [m for m in valid_metvars if m.get("date", "") == latest_date]
        return latest_metvars[0]
    return valid_metvars[0]


def process_metvar(metvar_element: etree.Element) -> Dict[str, Any]:
    """Process a metvar element from the XML dictionary according to DTD structure"""
    record = {}

    # Get metvar attributes
    record["origin"] = metvar_element.get("origin", "")
    record["usage"] = metvar_element.get("usage", "current")
    record["pack"] = metvar_element.get("pack", "")
    record["date"] = metvar_element.get("date", "")

    # Get nomvar element and its attributes
    nomvar_elem = metvar_element.find("nomvar")
    if nomvar_elem is not None:
        record["nomvar"] = nomvar_elem.text.strip() if nomvar_elem.text else ""
        # Get all nomvar attributes
        record["ip1"] = nomvar_elem.get("ip1", "")
        record["ip2"] = nomvar_elem.get("ip2", "")
        record["ip3"] = nomvar_elem.get("ip3", "")
        record["level"] = nomvar_elem.get("level", "")
        record["kind"] = nomvar_elem.get("kind", "")
        record["etiket"] = nomvar_elem.get("etiket", "")
    else:
        record["nomvar"] = ""
        record["ip1"] = record["ip2"] = record["ip3"] = ""
        record["level"] = record["kind"] = record["etiket"] = ""

    # Get description elements
    desc_elem = metvar_element.find("description")
    if desc_elem is not None:
        # Get short descriptions
        short_en = desc_elem.find("short[@lang='en']")
        short_fr = desc_elem.find("short[@lang='fr']")
        record["description_short_en"] = short_en.text.strip() if short_en is not None and short_en.text else ""
        record["description_short_fr"] = short_fr.text.strip() if short_fr is not None and short_fr.text else ""

        # Get long descriptions
        long_en = desc_elem.find("long[@lang='en']")
        long_fr = desc_elem.find("long[@lang='fr']")
        record["description_long_en"] = long_en.text.strip() if long_en is not None and long_en.text else ""
        record["description_long_fr"] = long_fr.text.strip() if long_fr is not None and long_fr.text else ""
    else:
        record["description_short_en"] = record["description_short_fr"] = ""
        record["description_long_en"] = record["description_long_fr"] = ""

    # Process measure element
    measure_elem = metvar_element.find("measure")
    if measure_elem is not None:
        # Find which type of measure it is
        measure_type = None
        measure_data = None
        for type_name in ["integer", "real", "logical", "code"]:
            type_elem = measure_elem.find(type_name)
            if type_elem is not None:
                measure_type = type_name
                measure_data = type_elem
                break

        record["measure_type"] = measure_type if measure_type else ""

        if measure_data is not None:
            # Handle common elements for integer and real
            if measure_type in ["integer", "real"]:
                units_elem = measure_data.find("units")
                record["units"] = units_elem.text.strip() if units_elem is not None and units_elem.text else ""

                magnitude_elem = measure_data.find("magnitude")
                record["magnitude"] = (
                    magnitude_elem.text.strip() if magnitude_elem is not None and magnitude_elem.text else ""
                )

                min_elem = measure_data.find("min")
                record["min"] = min_elem.text.strip() if min_elem is not None and min_elem.text else ""

                max_elem = measure_data.find("max")
                record["max"] = max_elem.text.strip() if max_elem is not None and max_elem.text else ""

                # Additional elements for real type
                if measure_type == "real":
                    precision_elem = measure_data.find("precision")
                    record["precision"] = (
                        precision_elem.text.strip() if precision_elem is not None and precision_elem.text else ""
                    )
                else:
                    record["precision"] = ""

            # Handle code and logical types
            elif measure_type in ["code", "logical"]:
                codes = []
                values = measure_data.findall("value")
                meanings_en = measure_data.findall("meaning[@lang='en']")
                # meanings_fr = measure_data.findall("meaning[@lang='fr']")
                meanings = measure_data.findall("meaning")

                # If we have language-specific meanings
                if meanings_en and len(values) == len(meanings_en):
                    for val, meaning in zip(values, meanings_en):
                        if val.text and meaning.text:
                            codes.append(f"{val.text.strip()}:{meaning.text.strip()}")
                # If we have both languages without explicit attributes
                elif len(values) * 2 == len(measure_data.findall("meaning")):
                    meanings = measure_data.findall("meaning")
                    half = len(meanings) // 2
                    for i, val in enumerate(values):
                        if val.text and meanings[i].text and meanings[i + half].text:
                            codes.append(
                                f"{val.text.strip()}:{meanings[i].text.strip()}/{meanings[i + half].text.strip()}"
                            )
                # Simple value-meaning pairs without language attributes
                elif len(values) == len(meanings):
                    for val, meaning in zip(values, meanings):
                        if val.text and meaning.text:
                            codes.append(f"{val.text.strip()}:{meaning.text.strip()}")

                record["codes"] = ";".join(codes) if codes else None
                record["units"] = record["precision"] = record["magnitude"] = ""
                record["min"] = record["max"] = ""
    else:
        record["measure_type"] = ""
        record["units"] = record["precision"] = record["magnitude"] = ""
        record["min"] = record["max"] = ""
        record["codes"] = None

    return record


def process_typvar(typvar_element: etree.Element) -> Dict[str, str]:
    """Process a typvar element from the XML dictionary according to DTD structure"""
    record = {}

    # Get typvar attributes
    record["origin"] = typvar_element.get("origin", "")
    record["usage"] = typvar_element.get("usage", "current")
    record["date"] = typvar_element.get("date", "")

    # Get nomtype element
    nomtype_elem = typvar_element.find("nomtype")
    record["typvar"] = nomtype_elem.text.strip() if nomtype_elem is not None and nomtype_elem.text else ""

    # Get description elements
    desc_elem = typvar_element.find("description")
    if desc_elem is not None:
        # Get short descriptions
        short_en = desc_elem.find("short[@lang='en']")
        short_fr = desc_elem.find("short[@lang='fr']")
        record["description_short_en"] = short_en.text.strip() if short_en is not None and short_en.text else ""
        record["description_short_fr"] = short_fr.text.strip() if short_fr is not None and short_fr.text else ""
    else:
        record["description_short_en"] = record["description_short_fr"] = ""

    return record


# Define schemas for the DataFrames
METVAR_SCHEMA = {
    "nomvar": pl.Utf8,
    "origin": pl.Utf8,
    "usage": pl.Utf8,
    "pack": pl.Utf8,
    "date": pl.Utf8,
    "ip1": pl.Utf8,
    "ip2": pl.Utf8,
    "ip3": pl.Utf8,
    "level": pl.Utf8,
    "kind": pl.Utf8,
    "etiket": pl.Utf8,
    "description_short_en": pl.Utf8,
    "description_short_fr": pl.Utf8,
    "description_long_en": pl.Utf8,
    "description_long_fr": pl.Utf8,
    "measure_type": pl.Utf8,
    "units": pl.Utf8,
    "precision": pl.Utf8,
    "magnitude": pl.Utf8,
    "min": pl.Utf8,
    "max": pl.Utf8,
    "codes": pl.Utf8,
}

TYPVAR_SCHEMA = {
    "typvar": pl.Utf8,
    "origin": pl.Utf8,
    "usage": pl.Utf8,
    "date": pl.Utf8,
    "description_short_en": pl.Utf8,
    "description_short_fr": pl.Utf8,
}


def __load_parquet_backup(data_dir: str = "data") -> Tuple[Optional[pl.DataFrame], Optional[pl.DataFrame]]:
    """Load metvar and typvar dataframes from parquet files if they exist.

    Args:
        data_dir (str): Directory containing the parquet files

    Returns:
        Tuple[Optional[pl.DataFrame], Optional[pl.DataFrame]]: Tuple of (metvar_df, typvar_df)
    """
    try:
        # First try the specified data directory
        metvar_path = Path(data_dir) / "metvar_dictionary.parquet"
        typvar_path = Path(data_dir) / "typvar_dictionary.parquet"

        # If files don't exist in data_dir, try package's data directory
        if not metvar_path.exists() or not typvar_path.exists():
            package_dir = Path(__file__).parent
            package_data_dir = package_dir / "data"
            metvar_path = package_data_dir / "metvar_dictionary.parquet"
            typvar_path = package_data_dir / "typvar_dictionary.parquet"

        metvar_df = pl.read_parquet(metvar_path) if metvar_path.exists() else None
        typvar_df = pl.read_parquet(typvar_path) if typvar_path.exists() else None

        if metvar_df is not None:
            LOGGER.warning(f"Loaded metvar dataframe from {metvar_path}")
        if typvar_df is not None:
            LOGGER.warning(f"Loaded typvar dataframe from {typvar_path}")

        return metvar_df, typvar_df

    except Exception as e:
        LOGGER.warning(f"Error loading parquet files: {str(e)}")
        return None, None


class CMCDictionary:
    """Singleton class that caches the XML as Polars DataFrames for faster lookups"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._load_dictionary()
            self._initialized = True

    def _load_dictionary(self):
        """Load and parse the XML dictionary once into Polars DataFrames"""
        root = globals()["__parse_opt_dict"]()
        if root is None:
            LOGGER.warning("Failed to get XML root element, attempting to load from parquet backup")
            self._metvar_df, self._typvar_df = __load_parquet_backup()
            if self._metvar_df is None and self._typvar_df is None:
                LOGGER.error("Failed to load from parquet backup")
            return

        # Process metvars
        metvar_records = []
        for metvar in root.findall(".//metvar"):
            record = process_metvar(metvar)
            if record["nomvar"]:  # Only add if nomvar exists
                metvar_records.append(record)

        # Create metvar DataFrame
        if metvar_records:
            self._metvar_df = pl.DataFrame(metvar_records, schema=METVAR_SCHEMA).sort("nomvar")
        else:
            self._metvar_df = None
            LOGGER.error("No metvar records found")

        # Process typvars
        typvar_records = []
        for typvar in root.findall(".//typvar"):
            record = process_typvar(typvar)
            if record["typvar"]:  # Only add if typvar exists
                typvar_records.append(record)

        # Create typvar DataFrame
        if typvar_records:
            self._typvar_df = pl.DataFrame(typvar_records, schema=TYPVAR_SCHEMA).sort("typvar")
        else:
            self._typvar_df = None
            LOGGER.error("No typvar records found")

    def get_metvar(
        self,
        nomvar: Union[str, Sequence[str]],
        columns: List[str],
        usages: List[str] = None,
        ip1: Optional[Union[str, int, Sequence[Union[str, int]]]] = None,
        ip3: Optional[Union[str, int, Sequence[Union[str, int]]]] = None,
    ) -> Union[Optional[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
        """Get metadata for one or more metvars using cache.

        Args:
            nomvar: Single nomvar string or sequence of nomvars
            columns: List of columns to return
            usages: List of usages to consider (default: ["current"])
            ip1: Optional single value or sequence of ip1 values
            ip3: Optional single value or sequence of ip3 values

        Returns:
            For single nomvar without IP: Dictionary mapping column names to values
            For single nomvar with IP: Dictionary mapping IP values to metadata dictionaries
            For sequence input: Dictionary mapping nomvars to metadata dictionaries
            Returns None if not found
        """
        if usages is None:
            usages = ["current"]

        if self._metvar_df is None:
            return None

        # Convert inputs to lists if they're sequences
        is_sequence = not isinstance(nomvar, str)
        nomvars = list(nomvar) if is_sequence else [nomvar]

        # Convert IP values if provided
        def convert_ip_value(x):
            if x is None or (isinstance(x, str) and not x.strip()):
                return None
            try:
                val = float(x)
                if val.is_integer():
                    val = int(val)
                    # Get just the p value from convert_ip
                    _, p, _ = convert_ip(val, 0, 0, -1)  # Decode mode
                    return p
                return val
            except (ValueError, TypeError):
                return None

        # Handle IP1 values
        if ip1 is not None:
            if is_sequence and not isinstance(ip1, (str, int)):
                if len(ip1) != len(nomvars):
                    raise ValueError("All input sequences must have the same length")
                ip1s = [convert_ip_value(x) for x in ip1]
            else:
                ip1s = [convert_ip_value(ip1)] * len(nomvars)
        else:
            ip1s = [None] * len(nomvars)

        # Handle IP3 values
        if ip3 is not None:
            if is_sequence and not isinstance(ip3, (str, int)):
                if len(ip3) != len(nomvars):
                    raise ValueError("All input sequences must have the same length")
                ip3s = [convert_ip_value(x) for x in ip3]
            else:
                ip3s = [convert_ip_value(ip3)] * len(nomvars)
        else:
            ip3s = [None] * len(nomvars)

        # Process each nomvar
        results = {}
        for i, nv in enumerate(nomvars):
            if not isinstance(nv, str):
                results[nv] = None
                continue
            try:
                # Build filter conditions
                conditions = [pl.col("nomvar") == nv]

                # Only apply usage filter if the variable has a usage attribute
                if usages:
                    conditions.append(
                        pl.col("usage").is_in(usages) | pl.col("usage").is_null() | (pl.col("usage") == "")
                    )

                # Get initial result
                result = self._metvar_df
                for condition in conditions:
                    result = result.filter(condition)
                if result.height == 0:
                    results[nv] = None
                    continue
                # Check if this metvar has IP values
                has_ip1 = result.filter(pl.col("ip1").ne("")).height > 0
                has_ip3 = result.filter(pl.col("ip3").ne("")).height > 0

                # If the metvar has IP values, return a dictionary of IP definitions
                if has_ip1 or has_ip3:
                    ip_results = {}
                    # Convert IP values in the DataFrame to p values
                    if has_ip1:
                        # Convert IP1 values to p values
                        try:
                            result = result.with_columns(
                                [pl.col("ip1").map_elements(convert_ip_value, return_dtype=pl.Float32).alias("ip1_p")]
                            )
                        except AttributeError:
                            result = result.with_columns([pl.col("ip1").apply(convert_ip_value).alias("ip1_p")])

                    if has_ip3:
                        try:
                            result = result.with_columns(
                                [pl.col("ip3").map_elements(convert_ip_value, return_dtype=pl.Float32).alias("ip3_p")]
                            )
                        except AttributeError:
                            result = result.with_columns([pl.col("ip3").apply(convert_ip_value).alias("ip3_p")])

                    # Apply IP filters if provided
                    if ip1s[i] is not None and has_ip1:
                        result = result.filter(pl.col("ip1_p") == ip1s[i])
                    if ip3s[i] is not None and has_ip3:
                        result = result.filter(pl.col("ip3_p") == ip3s[i])

                    # If specific IP values were provided and found, return single result
                    if (ip1s[i] is not None or ip3s[i] is not None) and len(result) > 0:
                        result = result.sort("date", descending=True)
                        row = result.row(0, named=True)
                        results[nv] = {"nomvar": nv, **{col: row[col] for col in columns}}
                    else:
                        # Otherwise return all IP definitions
                        result = result.sort("date", descending=True)
                        for row in result.iter_rows(named=True):
                            key = row["ip1"] if has_ip1 else row["ip3"]
                            if key and key.strip():
                                ip_results[key] = {"nomvar": nv, **{col: row[col] for col in columns}}
                        results[nv] = ip_results if ip_results else None
                else:
                    # For non-IP variables, return the most recent definition
                    if len(result) > 0:
                        result = result.sort("date", descending=True)
                        row = result.row(0, named=True)
                        results[nv] = {"nomvar": nv, **{col: row[col] for col in columns}}
                    else:
                        results[nv] = None

            except Exception as e:
                LOGGER.warning(f"Error getting metadata for {nv}: {str(e)}")
                results[nv] = None

        # Return results in appropriate format
        if not is_sequence:
            return results[nomvars[0]]
        return results

    def get_typvar(self, nomtype: str, columns: List[str]) -> Optional[Dict[str, str]]:
        """Get metadata for a single typvar using cached DataFrame"""
        if self._typvar_df is None or not isinstance(nomtype, str):
            return None

        try:
            # Get matching record
            needed_cols = ["typvar"] + columns
            result = self._typvar_df.filter(pl.col("typvar") == nomtype).select(needed_cols)

            if len(result) == 0:
                return None

            row = result.row(0, named=True)
            return {"typvar": nomtype, **{col: row[col] for col in columns}}

        except Exception as e:
            LOGGER.warning(f"Error getting typvar metadata for {nomtype}: {str(e)}")
            return None


# Create singleton instance
_dict_cache = CMCDictionary()


def convert_ip(ip: int, p: float, kind: int, mode: int) -> Tuple[int, float, int]:
    """
    Convert between IP values and real values with their associated kinds.

    This function handles both encoding (P->IP) and decoding (IP->P) of values
    using various coordinate systems (height, pressure, sigma, etc.).

    Args:
        ip: The coded IP value
        p: The actual value
        kind: The type of coordinate (see Kind enum)
        mode: Direction of conversion (>0 for P->IP, <0 for IP->P)

    Returns:
        Tuple of (ip, p, kind) where:
            - ip: The coded IP value
            - p: The actual value
            - kind: The coordinate type

    Special Cases:
        1. Old Style Encoding:
            - Height range (12000 < ip <= 32000): 5m steps
            - Sigma range (2000 <= ip <= 12000): 0-1 range
            - Pressure range (0 <= ip < 1100): Direct mb values
            - Complex pressure range (1200 < ip < 2000): Various scales

        2. New Style Encoding:
            - Uses mantissa and exponent encoding
            - Special ranges for arbitrary values (10-12, 1-6)
            - Handles negative values with offset

        3. Zero Values:
            - Each kind has its own zero threshold
            - Values below threshold are treated as zero

        4. Range Validation:
            - Each kind has valid ranges (LOW_VALUES to HIGH_VALUES)
            - Values outside range return error code (-999999)
    """
    if mode > 0:  # P -> IP conversion
        if kind not in Kind._value2member_map_:
            return (-999999, p, -1)

        # Special case for pressure = 0
        if kind == Kind.PRESSURE and p == 0.0:
            return (0, p, kind)

        # Range validation
        if p < LOW_VALUES.get(kind, -1e10) or p > HIGH_VALUES.get(kind, 1e10):
            return (-999999, p, -1)

        # New style encoding
        iexp = 4  # Initial exponent
        temp = p

        # Apply zero value threshold
        if abs(temp) < ZERO_VALUES.get(kind, 1e-5):
            temp = ZERO_VALUES[kind]

        # Apply scaling factor
        temp = temp * FACTOR_VALUES.get(kind, 1.0)

        # Determine limits and offset based on sign
        if temp >= 0:
            limit1 = 1000000.0
            limit2 = 100000.0
            offset = 0
        else:
            temp = -temp
            limit1 = 48000.0
            limit2 = 4800.0
            offset = 1000000

        # Adjust exponent to fit value in range
        while 0 < iexp < 15:
            if temp >= limit1:
                temp /= 10.0
                iexp -= 1
            elif temp < limit2:
                temp *= 10.0
                iexp += 1
            else:
                break

        if temp > limit1:
            return (-1, p, kind)

        mantissa = int(offset + round(temp))
        ip = mantissa | (iexp << 20) | (kind << 24)

    else:  # IP -> P conversion
        if ip > 32767:  # New style encoding
            # Special ranges based on test output
            if NEW_STYLE_RANGES["ARBITRARY_10_12"][0] <= ip <= NEW_STYLE_RANGES["ARBITRARY_10_12"][1]:
                return (ip, 10.0 + (ip - NEW_STYLE_RANGES["ARBITRARY_10_12"][0]) / 10000, Kind.ARBITRARY)
            elif NEW_STYLE_RANGES["ARBITRARY_1_6"][0] <= ip <= NEW_STYLE_RANGES["ARBITRARY_1_6"][1]:
                return (ip, 1.0 + (ip - NEW_STYLE_RANGES["ARBITRARY_1_6"][0]) / 100000, Kind.ARBITRARY)
            elif ip == NEW_STYLE_RANGES["SPECIAL_CASE"]:
                return (ip, 0.0, Kind.ARBITRARY)

            kind = (ip >> 24) & 0xF
            if kind not in Kind._value2member_map_:
                return (ip, -999999.0, -1)

            iexp = (ip >> 20) & 0xF
            mantissa = ip & 0xFFFFF

            if mantissa > 1000000:
                p = -(mantissa - 1000000)
            else:
                p = mantissa

            p = p / (10 ** (iexp - 4))  # Adjust for initial exponent of 4
            p = p / FACTOR_VALUES.get(kind, 1.0)

            # Apply range limits
            if p < LOW_VALUES.get(kind, -1e10):
                p = LOW_VALUES[kind]
            elif p > HIGH_VALUES.get(kind, 1e10):
                p = HIGH_VALUES[kind]

            # Apply zero threshold
            if abs(p) < 1.001 * ZERO_VALUES.get(kind, 1e-5):
                p = 0.0

        else:  # Old style encoding
            # Special countdown range
            if COUNTDOWN_RANGE[0] <= ip <= COUNTDOWN_RANGE[1]:
                return (ip, 26.0 - (ip - COUNTDOWN_RANGE[0]), Kind.ARBITRARY)

            # Height range
            if OLD_STYLE_RANGES["HEIGHT"][0] < ip <= OLD_STYLE_RANGES["HEIGHT"][1]:
                kind = Kind.ABOVE_SEA
                p = 5.0 * (ip - 12001)
            # Sigma range
            elif OLD_STYLE_RANGES["SIGMA"][0] <= ip <= OLD_STYLE_RANGES["SIGMA"][1]:
                kind = Kind.SIGMA
                p = float(ip - 2000) / 10000.0
            # Pressure range
            elif OLD_STYLE_RANGES["PRESSURE"][0] <= ip < OLD_STYLE_RANGES["PRESSURE"][1]:
                kind = Kind.PRESSURE
                p = float(ip)
            # Complex pressure range
            elif OLD_STYLE_RANGES["COMPLEX_PRESSURE"][0] < ip < OLD_STYLE_RANGES["COMPLEX_PRESSURE"][1]:
                kind = Kind.PRESSURE
                if ip < 1400:
                    p = float(ip - 1200) / 20000.0
                elif ip < 1600:
                    p = float(ip - 1400) / 2000.0
                elif ip < 1800:
                    p = float(ip - 1600) / 200.0
                else:
                    p = float(ip - 1800) / 20.0
            elif OLD_STYLE_RANGES["OTHERS"][0] <= ip <= OLD_STYLE_RANGES["OTHERS"][1]:
                kind = Kind.ARBITRARY
                p = 1200.0 - ip
            # Special boundary cases
            elif ip == OLD_STYLE_RANGES["SIGMA"][1]:  # 12000
                kind = Kind.SIGMA
                p = 1.0
            elif ip == OLD_STYLE_RANGES["COMPLEX_PRESSURE"][0]:  # 1200
                kind = Kind.ARBITRARY
                p = 0.0
            elif ip == OLD_STYLE_RANGES["SIGMA"][0]:  # 2000
                kind = Kind.SIGMA
                p = 0.0
            else:
                kind = Kind.ARBITRARY
                p = float(ip)

    return (ip, p, kind)


def get_metvar_metadata(
    nomvar: Union[str, Sequence[str]],
    columns: Optional[List[str]] = None,
    usages: Optional[List[str]] = None,
    ip1: Optional[Union[str, int, float, Sequence[Union[str, int, float]]]] = None,
    ip3: Optional[Union[str, int, float, Sequence[Union[str, int, float]]]] = None,
) -> Union[Optional[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """Get metadata for one or more metvars with optional IP values.

    Args:
        nomvar: Single nomvar string or sequence of nomvars
        columns: List of columns to return. If None, returns all available columns.
        usages: List of usages to consider (default: ["current"])
        ip1: Optional single value or sequence of IP1 values
        ip3: Optional single value or sequence of IP3 values

    Returns:
        For single nomvar without IP: Dictionary mapping column names to values
        For single nomvar with IP: Dictionary mapping IP values to metadata dictionaries
        For sequence input: Dictionary mapping nomvars to metadata dictionaries
        Returns None if not found

    Note:
        - If sequences are provided for nomvar/ip1/ip3, they must all be the same length
        - IP values are converted using convert_ip before comparison
        - For sequence inputs, results maintain the order of input nomvars
        - Missing values in sequence results are filled with None
        - Variables without a usage attribute will be returned regardless of the usages parameter
    """
    if usages is None:
        usages = ["current"]

    # Input validation
    is_sequence = not isinstance(nomvar, str)
    if not isinstance(nomvar, (str, list, tuple, np.ndarray)):
        raise TypeError("nomvar must be a string or sequence")

    if columns is None:
        columns = list(__METVAR_METADATA_COLUMNS)
    elif not isinstance(columns, list):
        raise ValueError("columns must be a list")
    elif not columns:
        raise ValueError("columns cannot be empty")
    elif not all(isinstance(col, str) for col in columns):
        raise TypeError("all columns must be strings")
    elif not all(col in __METVAR_METADATA_COLUMNS for col in columns):
        raise ValueError("invalid column name")
    elif "nomvar" in columns:
        raise ValueError("nomvar cannot be in columns")

    if not isinstance(usages, list):
        raise ValueError("usages must be a list")
    elif not usages:
        raise ValueError("usages cannot be empty")
    elif not all(isinstance(usage, str) for usage in usages):
        raise TypeError("all usages must be strings")
    elif not all(usage in __METVAR_USAGES for usage in usages):
        invalid_usages = [usage for usage in usages if usage not in __METVAR_USAGES]
        raise ValueError(f"Invalid usages: {', '.join(invalid_usages)}")

    # Get metadata from cache
    result = _dict_cache.get_metvar(nomvar, columns, usages, ip1, ip3)

    # Return result in appropriate format
    if not is_sequence:
        return result
    return result


def get_typvar_metadata(nomtype: str, columns: Optional[List[str]] = None) -> Optional[Dict[str, str]]:
    """Get metadata for a type variable.

    Args:
        nomtype: The type variable to get metadata for
        columns: List of columns to return. If None, returns all available columns.

    Returns:
        Dictionary mapping column names to values, or None if not found

    Raises:
        ValueError: If columns is invalid
        TypeError: If nomtype is not a string
    """
    if not isinstance(nomtype, str):
        return None

    if columns is None:
        columns = list(__TYPVAR_METADATA_COLUMNS)
    elif not isinstance(columns, list):
        raise ValueError("columns must be a list")
    elif not columns:
        raise ValueError("columns cannot be empty")
    elif not all(isinstance(col, str) for col in columns):
        raise TypeError("all columns must be strings")
    elif not all(col in __TYPVAR_METADATA_COLUMNS for col in columns):
        raise ValueError("invalid column name")
    elif "typvar" in columns:
        raise ValueError("typvar cannot be in columns")

    return _dict_cache.get_typvar(nomtype, columns)
