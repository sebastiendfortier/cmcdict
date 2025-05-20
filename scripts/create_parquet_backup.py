import cmcdict
import polars as pl
import os
from pathlib import Path


def create_parquet_backup(output_dir: str = "data"):
    """
    Create parquet backups of the metvar and typvar dataframes from the CMC dictionary.

    Args:
        output_dir (str): Directory where parquet files will be saved
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the CMC Dictionary
    cmc_dict = cmcdict.CMCDictionary()

    # Get the dataframes
    metvar_df = cmc_dict._metvar_df
    typvar_df = cmc_dict._typvar_df

    if metvar_df is not None:
        output_path = Path(output_dir) / "metvar_dictionary.parquet"
        print(f"Saving metvar dataframe to {output_path}")
        metvar_df.write_parquet(output_path)
    else:
        print("Warning: Could not create metvar parquet file - no data available")

    if typvar_df is not None:
        output_path = Path(output_dir) / "typvar_dictionary.parquet"
        print(f"Saving typvar dataframe to {output_path}")
        typvar_df.write_parquet(output_path)
    else:
        print("Warning: Could not create typvar parquet file - no data available")


if __name__ == "__main__":
    create_parquet_backup()
