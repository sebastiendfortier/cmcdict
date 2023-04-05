# Introduction

## What is it?

cmcdict is a set of functions that help querying the operational variable dictionnary.

## cmcdict philosophy

Provide structured methods to query the operational variable dictionnary.


# Installation

Use the git repository package:

    python3 -m pip install git+http://gitlab.science.gc.ca/CMDS/cmcdict.git

### Use cmcdict

``` python
# inside your script
import cmcdict

cmcdict.get_metvar_metadata('TT')

{'nomvar': 'TT',
 'origin': '',
 'date': '',
 'type': 'real',
 'description_short_en': 'Air temperature',
 'description_short_fr': "Température de l'air",
 'description_long_en': '',
 'description_long_fr': '',
 'units': '°C',
 'min': '',
 'max': '',
 'codes': None,
 'precision': '',
 'magnitude': ''}

cmcdict.get_typvar_metadata('K')

{'typvar': 'K',
 'date': '',
 'description_short_en': 'Various constants',
 'description_short_fr': 'Constantes variées'}
```

For more examples and information check out the [documentation](https://web.science.gc.ca/~spst900/cmcdict/master/index.html)

# Contributing

## Getting the source code

``` bash
git clone git@gitlab.science.gc.ca:cmds/cmcdict.git
# create a new branch
git checkout -b my_change
# modify the code
# commit your changes
# fetch changes
git fetch
# merge recent master
git merge origin/master
# push your changes
git push my_change
```

Then create a merge request on science\'s gitlab
<https://gitlab.science.gc.ca/CMDS/cmcdict/merge_requests>

