# -*- coding: utf-8 -*-

import re

def pytest_itemcollected(item):
    node = item.obj
    doc = str(node.__doc__.strip()) if node.__doc__ else str('')
    doc = re.sub('[ÀÂÄ]', 'A', doc)
    doc = re.sub('[Çç]', 'c', doc)
    doc = re.sub('[ÈÉÊË]', 'E', doc)
    doc = re.sub('[ÎÏ]', 'I', doc)
    doc = re.sub('[ÔÖ]', 'O', doc)
    doc = re.sub('[ÙÛÜ]', 'U', doc)
    doc = re.sub('[àâä]', 'a', doc)
    doc = re.sub('[ç]', 'c', doc)
    doc = re.sub('[èéêë]', 'e', doc)
    doc = re.sub('[îï]', 'i', doc)
    doc = re.sub('[ôö]', 'o', doc)
    doc = re.sub('[ùû]', 'u', doc)
    item._nodeid = ' : '.join([item._nodeid,doc])
