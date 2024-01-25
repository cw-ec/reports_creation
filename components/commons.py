import logging
import sys
import os
import pandas as pd
from datetime import datetime


def logging_setup(log_dir=".\\") -> logging.getLogger():
    """Sets up logging takes one parameter to set a directory for the output log file"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, f"{datetime.today().strftime('%d-%m-%Y')}_log.log")),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger()


def create_dir(path: str) -> None:
    """Check if directory exists and if it doesn't create it."""
    if not os.path.exists(path):
        os.makedirs(path)


def to_dataframe(to_import: str, sheet=0, encoding='UTF-8') -> pd.DataFrame:
    """Import the given path into a pandas dataframe. Returns that pandas dataframe

    to_import = the path to the data to import into the dataframe. Required

    sheet = Name of the sheet to import into a dataframe. Can be integer or text of name (str)

    """

    path_list = os.path.split(to_import)
    f_type = path_list[-1].split('.')[-1]

    if f_type == 'csv':
        return pd.read_csv(to_import, encoding=encoding)
    elif f_type in ["xlsx", "xls"]:
        return pd.read_excel(to_import, sheet_name=sheet)
    else:
        raise Exception(f"File Extension: {f_type} not yet handled by this function")
