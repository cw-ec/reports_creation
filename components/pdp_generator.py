# -*- coding: utf-8 -*-
from .commons import logging_setup, to_dataframe, create_dir, add_en_dash, get_ed_name_from_code
from .builders import BuildPDPReport
import pandas as pd
import sys

class PDPGenerator:

    def gen_report_table(self) -> pd.DataFrame:
        """Generates the table that will be put into the report. Return the table with only the required fields"""

        # Create data copy because we may need the orig later
        out_df = self.df.copy()
        out_df = out_df[out_df["ED_CODE"] == self.ed_num]

        if len(out_df) == 0:  #If no data return the empty dataframe
            return out_df

        else:
            # Create Poll Number field be concatenating the poll num and suffix
            out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)

            # Fix en dashes if needed
            out_df['POLL_NAME_FIXED'] = out_df['POLL_NAME_FIXED'].apply(lambda x: x.replace('--', '—'))

            out_df['ELECTORS_LISTED'] = 123  # 123 placeholder for now until we get the electors counts added to the SQL
            out_df["VOID_IND"] = 'N' # This field is missing in most recent version of the data placeholder until fixed

            out_df["VOID_IND"] = out_df["VOID_IND"].replace('N', '') # No need to show N's replace with nothing
            return out_df[['PD_NO_CONCAT', 'POLL_NAME_FIXED', 'ELECTORS_LISTED', 'VOID_IND']]


    def __init__(self, data, out_path, ed_num):

        # Setup logging
        self.logger = logging_setup()

        self.out_path = out_path
        self.ed_num = ed_num
        self.logger.info("Loading data for Polling District Profile")
        self.df = to_dataframe(data, encoding='latin-1')

        self.logger.info("Generating PDP Report Table")
        self.report_df = self.gen_report_table()

        if len(self.report_df) == 0:
            self.logger.warning(f"No data available for PDD on {self.ed_num}. Check input data or workflow")

        else:
            # Set a bunch of things for the report from the first line of the data and create a dict to hold them
            self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)

            self.report_dict = {
                'ed_name': self.row1["ED_NAME_BIL"].to_list()[0].replace('--', '—'),
                'ed_code': self.row1['ED_CODE'].to_list()[0],
                'prov': self.row1['PRVNC_NAME_BIL'].to_list()[0],'rep_order': f"Representation order of {self.row1['RDSTRBTN_YEAR'].to_list()[0]} / Décret de représentation de {self.row1['RDSTRBTN_YEAR'].to_list()[0]}"
            }

            create_dir(self.out_path)
            self.logger.info("Creating Report PDF")
            BuildPDPReport(self.report_dict, self.report_df, out_dir=self.out_path)

            self.logger.info("Report Generated")
