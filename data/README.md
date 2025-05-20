# CMC Dictionary Parquet Backup

This directory contains parquet file backups of the CMC operational dictionary dataframes. These files serve as a fallback when the XML dictionary file is not accessible.

## Files

- `metvar_dictionary.parquet`: Contains metadata about meteorological variables
- `typvar_dictionary.parquet`: Contains metadata about type variables

## Creating Backup Files

To create or update the parquet backup files, run:

```bash
python scripts/create_parquet_backup.py
```

This will:
1. Try to load the XML dictionary
2. Convert the data to Polars DataFrames
3. Save the DataFrames as parquet files in this directory

## Usage

The parquet files are automatically used as a fallback when:
1. The XML dictionary file cannot be found in the expected locations
2. There is an error parsing the XML dictionary

No additional configuration is needed - the library will automatically attempt to load from these files if the XML dictionary is not available. 
