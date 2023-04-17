cmcdict
=======

Welcome to cmcdict’s documentation!
-----------------------------------

cmcdict is a set of functions that help querying the operational
variable dictionnary.

Philosophy
~~~~~~~~~~

Provide structured methods to query the operational variable
dictionnary.

Installation
------------

Requirements
~~~~~~~~~~~~

-  Python 3.6 or greater
-  `virtualenv <https://virtualenv.pypa.io>`__

Dependencies
~~~~~~~~~~~~

None

Installing cmcdict
~~~~~~~~~~~~~~~~~~

Install in a virtualenv using pip3:

.. code:: bash

   python -m venv cmcdict-venv
   cd cmcdict-venv
   . bin/activate
   pip3 install https://gitlab.science.gc.ca/CMDS/cmcdict/repository/master/archive.zip

   # via SSM
   . r.load.dot /fs/ssm/eccc/cmd/cmds/cmcdict/latest

Running
-------

.. code:: bash

   # inside your script
   >>> import cmcdict

   >>> cmcdict.get_metvar_metadata('TT')

      {
       'nomvar': 'TT',
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
       'magnitude': ''
      }

   >>> cmcdict.get_typvar_metadata('K')

      {
       'typvar': 'K',
       'date': '',
       'description_short_en': 'Various constants',
       'description_short_fr': 'Constantes variées'
      }


Contributing
------------

Getting the source code
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   git clone https://gitlab.science.gc.ca/CMDS/cmcdict.git
   # OPTIONAL: adjust environment variables if necessary
   cp cmcdict.emv local.env
   vi local.env
   . local.env
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

Then create a merge request on science’s gitlab
https://gitlab.science.gc.ca/CMDS/cmcdict/merge_requests

Code Conventions
~~~~~~~~~~~~~~~~

-  `PEP8 <https://www.python.org/dev/peps/pep-0008>`__

Bugs and Issues
~~~~~~~~~~~~~~~

All bugs, enhancements and issues are managed on
`GitLab <https://gitlab.science.gc.ca/CMDS/cmcdict/issues>`__.

Contact
-------

-  Sébastien Fortier
