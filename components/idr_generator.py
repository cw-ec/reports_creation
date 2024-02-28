# -*- coding: utf-8 -*-
from .commons import logging_setup, to_dataframe, create_dir, add_en_dash
from .builders import BuildIDRReport
import pandas as pd
import sys

class IDRGenerator:

    def gen_report_table(self) -> pd.DataFrame:
        """Generates the table that will be put into the report. Return the table with only the required fields"""

        # Create data copy because we may need the orig later
        out_df = self.df.copy()
        out_df = out_df[(out_df["ED_CODE"] == self.ed_num) & (out_df["PD_NBR"] >= 500)]  # Get only mobile poll records for the ed of interest

        # Create Poll Number field be concatenating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)
        out_df['ELECTORS_LISTED'] = 123  # 123 placeholder for now until we get the electors counts added to the SQL
        out_df["VOID_IND"] = 'N'  # This field is missing in most recent version of the data placeholder until fixed


        # Add the institution count to the report table
        inst_count = out_df.groupby('PD_NO_CONCAT')['MOBILE_POLL_STN_ID'].nunique().rename('TOTAL_INST')
        out_df = out_df.join(inst_count, on=['PD_NO_CONCAT'])

        # Add total count of electors for the mobile poll
        sum_elec = out_df.groupby('PD_NO_CONCAT')['ELECTORS_LISTED'].sum().rename('TOTAL_ELECTORS')
        out_df = out_df.join(sum_elec, on=['PD_NO_CONCAT'])

        # Create list of all PD numbers (concatenated) in each APD
        apd_grouped = out_df[['PD_NO_CONCAT', 'ADV_PD_NBR']].groupby('PD_NO_CONCAT').agg(list)
        apd_grouped.rename(columns={'ADV_PD_NBR':'APD_LIST'}, inplace=True)
        out_df = out_df.join(apd_grouped, on=['PD_NO_CONCAT'])
        out_df['APD_LIST'] = out_df['APD_LIST'].apply(lambda x: str([int(y) for y in x])[1:-1] if isinstance(x, list) else '')

        # Drop Duplicates before sending to builder
        out_df = out_df.drop_duplicates(subset='PD_NO_CONCAT', keep='first')

        return out_df[['PD_NO_CONCAT', 'TOTAL_INST', 'ELECTORS_LISTED', 'APD_LIST']]

    def __init__(self, data, out_path, ed_num):

        # Setup logging
        self.logger = logging_setup()

        self.out_path = out_path
        self.ed_num = ed_num
        self.logger.info("Loading data for Indigenous Lands Report")
        self.df = to_dataframe(data, encoding='latin-1')

        self.logger.info("Generating IDR Report Table")
        self.report_df = self.gen_report_table()

        # Set a bunch of things for the report from the first line of the data and create a dict to hold them
        self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)

        self.report_dict = {
            'ed_name': add_en_dash(self.row1["ED_NAME_BIL"].to_list()[0]),
            'ed_code': self.row1['ED_CODE'].to_list()[0],
            'prov': self.row1['PRVNC_NAME_BIL'].to_list()[0]
        }
        create_dir(self.out_path)
        self.logger.info("Creating Report PDF")
        self.template = BuildIDRReport(self.report_dict, self.report_df, out_dir=self.out_path)

        self.logger.info("Report Generated")
