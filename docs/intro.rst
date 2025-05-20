cmcdict
=======

Welcome to cmcdict's documentation!
-----------------------------------

cmcdict is a set of functions that help querying the operational
variable dictionary. It provides structured access to metadata about meteorological
variables and their types, supporting both English and French descriptions.
It provides structured access to metadata about meteorological
variables and their types, supporting both English and French descriptions.

Philosophy
~~~~~~~~~~

Provide structured methods to query the operational variable
dictionary, with support for:
- Multiple variable definitions with IP1 values
- Current and historical variable definitions
- Bilingual descriptions
- Various data types (real, code, logical, integer)


Requirements
~~~~~~~~~~~~

-  Python 3.8 or greater
-  `virtualenv <https://virtualenv.pypa.io>`__

Dependencies
~~~~~~~~~~~~

None

Installing cmcdict
~~~~~~~~~~~~~~~~~~

There are several ways to install and use cmcdict:

Via pip in a virtualenv
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   python -m venv cmcdict-venv
   cd cmcdict-venv
   . bin/activate
   pip3 install https://gitlab.science.gc.ca/CMDS/cmcdict/repository/master/archive.zip

Via SSM Bundle
^^^^^^^^^^^^^^

To use the latest bundle version:

.. code:: bash

   . r.load.dot /fs/ssm/eccc/cmd/cmds/cmcdict/bundle/2025.03.00

Via SSM Domain
^^^^^^^^^^^^^^

To use a specific domain version:

.. code:: bash

   . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/cmcdict/202503/00

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code:: python

   import cmcdict

   # Get metadata for a simple variable
   result = cmcdict.get_metvar_metadata('TT')
   print(result)  # Shows temperature metadata

   # Get metadata for a type variable
   result = cmcdict.get_typvar_metadata('K')
   print(result)  # Shows type metadata

Advanced Usage
~~~~~~~~~~~~~~

.. code:: python

   # Get specific columns only
   result = cmcdict.get_metvar_metadata('TT', columns=['units', 'description_short_en'])
   
   # Get variable with specific IP1
   result = cmcdict.get_metvar_metadata('UDST', ip1='1196')
   
   # Get metadata for a code-type variable
   result = cmcdict.get_metvar_metadata('GS', columns=['codes'])
   
   # Get metadata for a logical-type variable
   result = cmcdict.get_metvar_metadata('OBSE', columns=['codes'])

Special Cases
~~~~~~~~~~~~~

1. Variables with IP1:
   - Some variables have multiple definitions with different IP1 values
   - You can either:
   a) Specify an IP1 value to get a specific definition
   b) Get all IP1 definitions in a dictionary keyed by IP1 values

   - Example:

   .. code:: python

      # Get specific definition
      result = cmcdict.get_metvar_metadata('UDST', ip1='1196')
      print(result)  # Single definition for Sea Ice

      # Get all IP1 definitions
      results = cmcdict.get_metvar_metadata('UDST')
      print(results)  # Dictionary with '1195' and '1196' as keys

2. Date Handling:
   - When multiple definitions exist without IP1:
   - Returns the most recent definition by date
   - For definitions without dates, returns the first current one
   - For multiple definitions with same date, returns first one

3. Usage States:
   - By default, only returns 'current' variables
   - Can be configured to include other states (obsolete, deprecated, etc.)

API Reference
-------------

get_metvar_metadata
~~~~~~~~~~~~~~~~~~~

.. code:: python

   def get_metvar_metadata(
       nomvar: Union[str, Sequence[str]],
       columns: Optional[List[str]] = None,
       usages: List[str] = ['current'],
       ip1: Optional[Union[str, int, float, Sequence[Union[str, int, float]]]] = None,
       ip3: Optional[Union[str, int, float, Sequence[Union[str, int, float]]]] = None
   ) -> Union[Optional[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
       """Get metadata for one or more metvars with optional IP values."""

Parameters:
   - nomvar: Single nomvar string or sequence of nomvars
   - columns: List of metadata columns to return. If None, returns all available columns
   - usages: List of usage states to consider (default: ["current"])
   - ip1: Optional single value or sequence of IP1 values
   - ip3: Optional single value or sequence of IP3 values

Returns:
   - For single nomvar without IP: Dictionary mapping column names to values
   - For single nomvar with IP: Dictionary mapping IP values to metadata dictionaries
   - For sequence input: Dictionary mapping nomvars to metadata dictionaries
   - Returns None if not found

Note:
   - If sequences are provided for nomvar/ip1/ip3, they must all be the same length
   - IP values are converted using convert_ip before comparison
   - For sequence inputs, results maintain the order of input nomvars
   - Missing values in sequence results are filled with None
   - Variables without a usage attribute will be returned regardless of the usages parameter

get_typvar_metadata
~~~~~~~~~~~~~~~~~~~

.. code:: python

   def get_typvar_metadata(
       nomtype: str,
       columns: Optional[List[str]] = None
   ) -> Optional[Dict[str, str]]:
       """Get metadata for a type variable."""

Parameters:
   - nomtype: Type name to look up
   - columns: List of metadata columns to return. If None, returns all available columns

Returns:
   Dictionary with requested metadata or None if not found

Raises:
   - ValueError: If columns is invalid
   - TypeError: If nomtype is not a string

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


Then create a merge request on science's gitlab
https://gitlab.science.gc.ca/CMDS/cmcdict/merge_requests

Code Conventions
~~~~~~~~~~~~~~~~

-  `PEP8 <https://www.python.org/dev/peps/pep-0008>`__

Testing
~~~~~~~

The project uses pytest for testing. Tests are marked with the ``unit_tests`` marker:

.. code:: bash

   # Run all tests
   pytest

   # Run only unit tests
   pytest -m unit_tests

Bugs and Issues
~~~~~~~~~~~~~~~

All bugs, enhancements and issues are managed on
`GitLab <https://gitlab.science.gc.ca/CMDS/cmcdict/issues>`__.

Contact
-------

-  Sébastien Fortier
