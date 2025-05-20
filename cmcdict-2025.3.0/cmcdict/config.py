"""Configuration module for the CMC dictionary.

This module contains enumerations and constant dictionaries used throughout the
cmcdict package for defining coordinate types, value ranges, and encoding parameters.
"""

from enum import IntEnum
from typing import Dict


class Kind(IntEnum):
    """Enumeration of coordinate types used in the CMC dictionary.

    This enumeration defines the different kinds of vertical coordinates and other
    specialized types that can be associated with a meteorological variable.

    Attributes:
        ABOVE_SEA (int): Coordinate relative to sea level.
        SIGMA (int): Sigma coordinate.
        PRESSURE (int): Pressure coordinate.
        ARBITRARY (int): Arbitrary coordinate or value.
        ABOVE_GND (int): Coordinate relative to ground level.
        HYBRID (int): Hybrid coordinate.
        THETA (int): Theta (potential temperature) coordinate.
        HOURS (int): Time in hours.
    """

    ABOVE_SEA = 0
    SIGMA = 1
    PRESSURE = 2
    ARBITRARY = 3
    ABOVE_GND = 4
    HYBRID = 5
    THETA = 6
    HOURS = 10


# Range limits for each kind
LOW_VALUES: Dict[Kind, float] = {
    Kind.ABOVE_SEA: -100.0,
    Kind.SIGMA: 0.0,
    Kind.PRESSURE: 0.0,
    Kind.ARBITRARY: -1e10,
    Kind.ABOVE_GND: -100.0,
    Kind.HYBRID: 0.0,
    Kind.THETA: 0.0,
    Kind.HOURS: -24.0,
}

HIGH_VALUES: Dict[Kind, float] = {
    Kind.ABOVE_SEA: 100000.0,
    Kind.SIGMA: 1.0,
    Kind.PRESSURE: 1100.0,
    Kind.ARBITRARY: 1e10,
    Kind.ABOVE_GND: 100000.0,
    Kind.HYBRID: 1.0,
    Kind.THETA: 400.0,
    Kind.HOURS: 240.0,
}

# Zero thresholds for each kind
ZERO_VALUES: Dict[Kind, float] = {
    Kind.ABOVE_SEA: 0.0001,
    Kind.SIGMA: 0.0001,
    Kind.PRESSURE: 0.0001,
    Kind.ARBITRARY: 0.0001,
    Kind.ABOVE_GND: 0.0001,
    Kind.HYBRID: 0.0001,
    Kind.THETA: 0.0001,
    Kind.HOURS: 0.0001,
}

# Scaling factors for each kind
FACTOR_VALUES: Dict[Kind, float] = {
    Kind.ABOVE_SEA: 1.0,
    Kind.SIGMA: 1.0,
    Kind.PRESSURE: 1.0,
    Kind.ARBITRARY: 1.0,
    Kind.ABOVE_GND: 1.0,
    Kind.HYBRID: 1.0,
    Kind.THETA: 1.0,
    Kind.HOURS: 1.0,
}

# Old style encoding ranges
OLD_STYLE_RANGES = {
    "HEIGHT": (12000, 32000),
    "SIGMA": (2000, 12000),
    "PRESSURE": (0, 1100),
    "COMPLEX_PRESSURE": (1200, 2000),
    "OTHERS": (1100, 1200),
}

# Special countdown range
COUNTDOWN_RANGE = (1051, 1076)

# New style encoding ranges
NEW_STYLE_RANGES = {
    "ARBITRARY_10_12": (1077, 1099),
    "ARBITRARY_1_6": (1100, 1199),
    "SPECIAL_CASE": 1200,
}
