#######################################################################
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

from pathlib import Path
import re
from setuptools import find_packages, setup


def get_package_version():
    init_py = Path(__file__).resolve().parent / "cmcdict" / "__init__.py"
    version_regex = r"__version__\s*=\s*['\"]([^'\"]*)['\"]"
    try:
        with open(init_py, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(version_regex, content)
            if match:
                return match.group(1)
            else:
                print("Warning: __version__ not found in __init__.py")
                return "unknown"
    except Exception as e:
        print(f"Error reading version from __init__.py: {e}")
        return "unknown"
    
LONG_DESCRIPTION = read('README.md')

DESCRIPTION = 'Python library to work with the CMC operational dictionary'

MANIFEST = Path('MANIFEST')

if MANIFEST.exists():
    MANIFEST.unlink()

setup(
    name='cmcdict',
    version=get_package_version(),
    description=DESCRIPTION.strip(),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='GPLv3',
    platforms='all',
    keywords=' '.join([
        'cmc',
        'o.dict'
    ]),
    author='Sebastien Fortier',
    author_email='sebastien.fortier@ec.gc.ca',
    maintainer='Sebastien Fortier',
    maintainer_email='sebastien.fortier@ec.gc.ca',
    url='https://gitlab.science.gc.ca/CMDS/cmcdict',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
