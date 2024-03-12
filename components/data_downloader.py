import oracledb
import json
import csv
import os, sys
import sqlalchemy
import pandas as pd
from collections import OrderedDict
from .commons import logging_setup, create_dir


class DataDownloader:
    """Downloads the data from associated databases using SQL requirements (username, password) are passed into the  script using a json file. Data will be downloaded into the data folder
    at the root of this repository"""

    def extract_params(self) -> OrderedDict:
        """Extracts the requested reports from the input workflow"""

        oc = OrderedDict()

        with open(self.settings, mode='r') as j:
            content = json.load(j)

            for k in content.keys():
                oc[k] = content[k]

            return oc

    def download_data(self) -> None:
        """Downloads the data into the data folder"""

        for dataset in self.params['data']:

            out_csv_nme = os.path.split(dataset['sql_path'])[-1].split('.')[0]

            self.logger.info(f"Running query to extract {out_csv_nme}.csv")

            # Read the required SQL file(s) into a variable
            with open(dataset['sql_path'], mode='r') as f:
                sql_file = f.read()

            # connect_string = f"oracle://{dataset['username']}:{dataset['password']}@{dataset['database']}"

            # Add FED Array to SQL file
            sql_file = sql_file.replace('ED_LIST_HERE', str(tuple(dataset['ed_list'])))

            # Create db connection
            connection = oracledb.connect(user=dataset['username'],
                                          password=dataset['password'],
                                          dsn=f"{dataset['database']}")

            self.logger.info(f"Getting data for {out_csv_nme}")
            df = pd.read_sql(sql_file, connection)
            df.to_csv(os.path.join(self.out_path, f"{out_csv_nme}.csv"), encoding='mbcs', index=False)  # mbcs == ANSI driver name (ANSI was the encoding available when using golden)

    def __init__(self, settings) -> None:
        # setup logging
        self.logger = logging_setup()

        # Get the parameters from the setting json
        self.settings = settings

        # Set output directory and create the directory
        self.out_path = ".\\data"
        create_dir(self.out_path)

        self.logger.info("Extracting connection parameters")
        self.params = self.extract_params()

        self.download_data()

        self.logger.info("DONE!")


if __name__ == '__main__':
    DataDownloader(r"C:\reports_creation-Build-PDF-Report\workflows\data_download.json")