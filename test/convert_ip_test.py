import pytest
from cmcdict import convert_ip, Kind

pytestmark = [pytest.mark.unit_tests]


def test_01():
    """Test special case of zero pressure"""
    ip, p, kind = convert_ip(0, 0.0, Kind.PRESSURE, 1)
    assert ip == 0
    assert p == 0.0
    assert kind == Kind.PRESSURE


def test_02():
    """Test pressure values at and beyond limits"""
    # Just under max pressure
    ip, p, kind = convert_ip(0, 1099.99, Kind.PRESSURE, 1)
    assert kind == Kind.PRESSURE
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p - 1099.99) < 0.01

    # At max pressure - should encode successfully
    ip, p, kind = convert_ip(0, 1100.0, Kind.PRESSURE, 1)
    assert kind == Kind.PRESSURE
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p - 1100.0) < 0.01

    # Beyond max pressure - should fail
    ip, p, kind = convert_ip(0, 1100.1, Kind.PRESSURE, 1)
    assert ip == -999999
    assert kind == -1
    assert p == 1100.1  # Original value should be unchanged


def test_03():
    """Test sigma level values within valid range"""
    # Minimum sigma
    ip, p, kind = convert_ip(0, 0.0, Kind.SIGMA, 1)
    assert kind == Kind.SIGMA
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p) < 1e-5

    # Maximum sigma
    ip, p, kind = convert_ip(0, 1.0, Kind.SIGMA, 1)
    assert kind == Kind.SIGMA
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p - 1.0) < 1e-5


def test_04():
    """Test height values at and beyond limits"""
    # Minimum height - should fail
    ip, p, kind = convert_ip(0, -20000.0, Kind.ABOVE_SEA, 1)
    assert ip == -999999
    assert kind == -1
    assert p == -20000.0  # Original value should be unchanged

    # Maximum height
    ip, p, kind = convert_ip(0, 100000.0, Kind.ABOVE_SEA, 1)
    assert kind == Kind.ABOVE_SEA
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p - 100000.0) < 0.1

    # Below min height - should fail
    ip, p, kind = convert_ip(0, -20001.0, Kind.ABOVE_SEA, 1)
    assert ip == -999999
    assert kind == -1
    assert p == -20001.0  # Original value should be unchanged

    # Above max height - should fail
    ip, p, kind = convert_ip(0, 100001.0, Kind.ABOVE_SEA, 1)
    assert ip == -999999
    assert kind == -1
    assert p == 100001.0  # Original value should be unchanged


def test_05():
    """Test pressure values near encoding boundaries"""
    test_values = [999.999, 99.9999, 9.99999, 0.99999]
    for val in test_values:
        ip, p, kind = convert_ip(0, val, Kind.PRESSURE, 1)
        assert kind == Kind.PRESSURE
        rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
        assert abs(rev_p - val) < 0.001


def test_06():
    """Test very small non-zero values"""
    ip, p, kind = convert_ip(0, 0.000001, Kind.PRESSURE, 1)
    assert kind == Kind.PRESSURE
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    # Very small values may be converted to zero
    assert rev_p == 0.0 or abs(rev_p - 0.000001) < 1e-6


def test_07():
    """Test negative values for supported kinds"""
    # Negative height
    ip, p, kind = convert_ip(0, -10.0, Kind.ABOVE_SEA, 1)
    assert kind == Kind.ABOVE_SEA
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p - (-10.0)) < 0.01

    # Negative hours
    ip, p, kind = convert_ip(0, -12.0, Kind.HOURS, 1)
    assert kind == Kind.HOURS
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p - (-12.0)) < 0.01


def test_08():
    """Test common meteorological pressure levels"""
    levels = [1013.25, 1000.0, 850.0, 700.0, 500.0, 250.0, 100.0]
    for level in levels:
        ip, p, kind = convert_ip(0, level, Kind.PRESSURE, 1)
        assert kind == Kind.PRESSURE
        rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
        assert abs(rev_p - level) < 0.01


def test_09():
    """Test common sigma levels"""
    levels = [0.995, 0.850, 0.500, 0.250]
    for level in levels:
        ip, p, kind = convert_ip(0, level, Kind.SIGMA, 1)
        assert kind == Kind.SIGMA
        rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
        assert abs(rev_p - level) < 0.001


def test_10():
    """Test common height levels"""
    heights = [0.0, 1500.0, 5000.0, 10000.0]
    for height in heights:
        ip, p, kind = convert_ip(0, height, Kind.ABOVE_SEA, 1)
        assert kind == Kind.ABOVE_SEA
        rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
        assert abs(rev_p - height) < 0.1


def test_11():
    """Test common forecast hour offsets"""
    hours = [0.0, 3.0, 6.0, 12.0, 24.0, -3.0]
    for hour in hours:
        ip, p, kind = convert_ip(0, hour, Kind.HOURS, 1)
        assert kind == Kind.HOURS
        rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
        assert abs(rev_p - hour) < 0.01


def test_12():
    """Test conversion with invalid kind value"""
    ip, p, kind = convert_ip(0, 100.0, 99, 1)  # Invalid kind
    assert ip == -999999
    assert kind == -1


def test_13():
    """Test sigma values near the edges of valid range"""
    # Very small sigma
    ip, p, kind = convert_ip(0, 0.0001, Kind.SIGMA, 1)
    assert kind == Kind.SIGMA
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert rev_p == 0.0

    # Near maximum sigma
    ip, p, kind = convert_ip(0, 0.9999, Kind.SIGMA, 1)
    assert kind == Kind.SIGMA
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p - 0.9999) < 1e-5


def test_14():
    """Test values near powers of ten boundaries"""
    # Large value near power of 10
    ip, p, kind = convert_ip(0, 9999.99, Kind.ABOVE_SEA, 1)
    assert kind == Kind.ABOVE_SEA
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert abs(rev_p - 9999.99) < 0.01

    # Small value near power of 10
    ip, p, kind = convert_ip(0, 0.0001, Kind.PRESSURE, 1)
    assert kind == Kind.PRESSURE
    rev_ip, rev_p, rev_kind = convert_ip(ip, 0, 0, -1)
    assert rev_p == 0.0


def test_15():
    """Test old style encoding ranges"""
    # Height range (12000 < ip <= 32000)
    ip, p, kind = convert_ip(12002, 0, 0, -1)
    assert kind == Kind.ABOVE_SEA
    assert abs(p - 5.0) < 0.01  # 12002 -> 5.0 meters

    # Sigma range (2000 <= ip <= 12000)
    ip, p, kind = convert_ip(2100, 0, 0, -1)
    assert kind == Kind.SIGMA
    assert abs(p - 0.01) < 0.001  # 2100 -> 0.01 sigma

    # Pressure range (0 <= ip < 1100)
    ip, p, kind = convert_ip(850, 0, 0, -1)
    assert kind == Kind.PRESSURE
    assert abs(p - 850.0) < 0.01

    # Complex pressure range (1200 < ip < 2000)
    ip, p, kind = convert_ip(1300, 0, 0, -1)
    assert kind == Kind.PRESSURE
    assert p < 1.0  # Value in complex pressure range
