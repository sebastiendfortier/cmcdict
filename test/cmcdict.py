# -*- coding: utf-8 -*-
import pytest
import numpy as np
import cmcdict
pytestmark = [pytest.mark.unit_tests]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/ReaderCsv/testsFiles/'


def test_1(plugin_test_dir):
    """Test with pds1_level2.new.csv. It should return a DataFrame"""
    src = plugin_test_dir + 'pds1_level2.new.csv'
    df = fstpy.CsvFileReader(path=src, encode_ip1=False).to_pandas()

    NI = 3
    NJ = 2
    NK = 1

    d = {'nomvar': (1, "CSV"), 'etiket': (1, 'CSVREADER'), 'nbits': (1, 24), 'datyp': (1, 1), 'grtyp': (1, 'X'), 'typvar': (1, 'X'),
         'ip2': (1, 0), 'ip3': (1, 0), 'ig1': (1, 0), 'ig2': (1, 0), 'ig3': (1, 0), 'ig4': (1, 0), 'npas': (1, 0), 'grid': (1, '00'), 'ni': (1, NI),
         'nj': (1, NJ), 'nk': (1, NK)}

    for k, v in d.items():
        assert(df[k].unique().size == v[0])
        assert(df[k].unique()[0] == v[1])

    assert(df.ip1.unique().size == 2)
    assert(df.ip1.unique()[0] == 1)
    assert(df.ip1.unique()[1] == 0)

    d1 = np.array([[11.1, 22.2], [33.3, 44.4], [55.5, 66.6]], dtype=np.float32)
    d2 = df.d[0]
    d3 = np.array([[77.7, 88.8], [99.9, 100.1], [110.11, 120.12]], dtype=np.float32)
    d4 = df.d[1]

    assert(np.array_equal(d1, d2))
    assert(np.array_equal(d3, d4))
    assert(df.d.size == 2)


# test 
