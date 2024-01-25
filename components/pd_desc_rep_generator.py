import pandas as pd
import os, sys
from .commons import logging_setup, to_dataframe


class PDDescriptionGeneration:

    def is_valid(self, in_data):
        """Validates inputs"""
        if not isinstance(in_data, str):
            raise Exception("Parameter 'in_data' must be of type 'string'")

    def create_report(self):
        """Create the PD Description Report: consists of a table for each pd num-suffix
        """
        print(self.in_df[['PD_NBR', 'PD_NBR_SFX']].head())
        sys.exit()
        self.in_df['PD_NUMSUF'] = f"{self.in_df['PD_NBR']}-{self.in_df['PD_NBR_SFX']}"

    def __init__(self, in_data):
        self.logger = logging_setup()

        # Validate input data
        self.logger.info("Validating Inputs")
        self.is_valid(in_data)

        # Set inputs
        self.in_data = in_data

        # Load Data
        self.in_df = to_dataframe(self.in_data)

        # Run Process
        self.logger.info("Processing Report")
        self.create_report()

        self.logger.info("Processing Complete")
