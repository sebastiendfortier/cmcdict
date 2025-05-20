# cmcdict

Python library to work with the CMC operational dictionary.

## Installation

There are several ways to install and use cmcdict:

### Via Pixi (Recommended)

This project now supports [Pixi](https://pixi.sh) for dependency management and development environment setup. Pixi is a modern Python package manager that combines the best of conda and pip.

1. First, install pixi if you don't have it already:

```bash
. ssmuse-sh -p /fs/ssm/eccc/cmd/cmds/apps/pixi/202503/00/pixi_0.41.4_all
```

2. Create a development environment and install all dependencies:

```bash
# Clone the repository
git clone https://gitlab.science.gc.ca/CMDS/cmcdict.git
cd cmcdict

# Install all dependencies (including development dependencies)
pixi install --environment dev

```

### Via pip in a virtualenv

```bash
python -m venv cmcdict-venv
cd cmcdict-venv
. bin/activate
pip3 install https://gitlab.science.gc.ca/CMDS/cmcdict/repository/master/archive.zip
```

### Via SSM Bundle

To use the latest bundle version:
```bash
. r.load.dot /fs/ssm/eccc/cmd/cmds/cmcdict/bundle/2025.03.00
```

### Via SSM Domain

To use a specific domain version:
```bash
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/cmcdict/202503/00
```

## Usage

```python
import cmcdict

# Basic usage
result = cmcdict.get_metvar_metadata('TT')
print(result)

# Get specific columns
result = cmcdict.get_metvar_metadata('TT', columns=['units', 'description_short_en'])
print(result)

# Get metadata for multiple variables
results = cmcdict.get_metvar_metadata(['TT', 'UU', 'VV'])
print(results)

# Get metadata with IP1/IP3 values
result = cmcdict.get_metvar_metadata('UDST', ip1='1196')
print(result)

# Get metadata for a type variable
result = cmcdict.get_typvar_metadata('K')
print(result)
```

For more detailed usage examples and documentation, please refer to the [documentation](docs/intro.rst).

## Development

### Version Management

The package version is managed in a single source of truth: `cmcdict/__init__.py`. To update the version:

1. Edit the version in `cmcdict/__init__.py`:
```python
__version__ = "YYYY.MM.VV"  # e.g., "2025.01.00"
```

The version format follows `YYYY.MM.VV` where:
- `YYYY`: Release year
- `MM`: Release month
- `VV`: Version number within the month (starting at 00)

#### Build Numbers

In addition to the version, conda packages also use a build number in `conda.recipe/meta.yaml`. The build number should be:

- Incremented when rebuilding the package without changing its version, for example when:
  - Updating dependencies without changing package functionality
  - Fixing packaging issues (missing files, etc.)
  - Making build process changes
- Reset to 0 when updating the version number

Example build number usage:
```yaml
# In conda.recipe/meta.yaml
build:
  number: 0  # Reset to 0 for new versions
  # or
  number: 1  # Increment for rebuilds of same version
```

#### Version Usage

The version from `__init__.py` is automatically used by:
- The Python package build system (via hatchling)
- Documentation and runtime version checks
- Conda package builds (via BUILD_VERSION environment variable)
- All other package metadata

To verify the version is being picked up correctly:
```bash
# Check Python package version
pixi run get-version

# Build conda package (will use version from __init__.py)
pixi run conda-build

# Verify conda package version
conda list cmcdict
```

No other files need to be modified when updating the version.

### Development Tasks with Pixi

Pixi provides several predefined tasks for common development workflows:

```bash
# Run tests
pixi run --environment dev test

# Run linter
pixi run --environment dev lint

# Install the package in development mode
pixi run --environment dev build

# Build documentation
pixi run --environment dev docs
```

The clean task removes:
- Python build artifacts (build/, dist/, __pycache__, etc.)
- Documentation build files
- Conda build artifacts
- Temporary test environments
- Package caches

### Building and Publishing Conda Packages

This project includes tasks to build and publish conda packages to your personal anaconda.org channel:

```bash
# Build the conda package
pixi run -e dev conda-build

# Upload to your personal channel (fortiers)
pixi run -e dev conda-upload

# Test the uploaded package in a fresh environment
pixi run -e dev test-upload
```

The test-upload task will:
1. Create a new environment with the current package version
2. Install the package from the conda channel
3. Run a basic usage test
4. Clean up the test environment

Make sure you are logged in to Anaconda before uploading:

```bash
# Login to anaconda.org
anaconda login
```

### Managing Dependencies with Pixi

To add or update dependencies:

```bash
# Add a runtime dependency
pixi add package-name

# Add a development dependency
pixi add --feature dev package-name

# Update specific package
pixi update package-name
```

### Using Make and Pixi Together

The project provides a Makefile that integrates with Pixi for convenient development workflows. The Makefile will automatically detect if Pixi is available and install it if needed.

#### Common Make Commands

```bash
# Run tests
make test

# Run linting
make lint

# Fix linting issues automatically
make lint-fix

# Format code
make format

# Build the package
make build

# Build documentation
make doc

# Build conda package
make conda-build

# Upload conda package
make conda-upload

# Test package with Python 3.8
make test-py38

# Test package with Python 3.13
make test-py313

# Test with both Python versions
make test-both

# Clean all build artifacts
make clean
```

#### Understanding Pixi Environments

Pixi manages separate environments for different purposes:

1. **Default Environment**: Used for basic package usage
   ```bash
   pixi run python
   ```

2. **Development Environment**: Contains all development tools
   ```bash
   pixi run --environment dev python
   ```

3. **Testing Environments**: Specific Python versions for compatibility testing
   ```bash
   # Python 3.8 environment
   cd package_tests/environments
   pixi run --environment py38 python

   # Python 3.13 environment
   cd package_tests/environments
   pixi run --environment py313 python
   ```

#### Environment Management

```bash
# List all available environments
pixi environment list

# Activate an environment
pixi shell --environment dev

# Install dependencies for an environment
pixi install --environment dev

# Update dependencies
pixi update --environment dev
```

The Makefile automatically handles environment selection for each command, so you typically don't need to manage environments manually.

## Contributing

1. Clone the repository:
```bash
git clone https://gitlab.science.gc.ca/CMDS/cmcdict.git
```

2. Create a new branch:
```bash
git checkout -b my_change
```

3. Make your changes and commit them

4. Push your changes and create a merge request

## Testing

The project uses pytest for testing. Tests are marked with the `unit_tests` marker:

```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit_tests

# Using pixi
pixi run test

# Using pixi with development environment
pixi run --environment dev test
```

## License

This project is licensed under the GNU General Public License v3 - see the LICENSE file for details.

## Contact

- Sébastien Fortier (sebastien.fortier@ec.gc.ca)
