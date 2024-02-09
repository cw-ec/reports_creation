from .commons import logging_setup, to_dataframe
from components.builders.build_pdd_report import BuildPDDReport
import pandas as pd
import sys


class PDDGenerator:

    def gen_report_tables(self) -> list:
        """Generates the table that will be put into the report. Return the table with only the required fields"""

        # Create data copy because we may need the orig later
        out_df = self.df.copy()
        out_df = out_df[out_df["ED_CODE"] == self.ed_num]

        # Create Poll Number field be concatenating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)

        out_df = out_df[['PD_NO_CONCAT', 'FROM_CROSS_FEAT', 'TO_CROSS_FEAT', 'FROM_CIV_NUM', 'TO_CIV_NUM', 'ST_SIDE_DESC_BIL']]
        df_list = []
        # Create a df for each pd and append it to the df list
        for pd in out_df['PD_NO_CONCAT'].values.tolist():
            pd_df = out_df[out_df['PD_NO_CONCAT'] == pd ]
            df_list.append(pd_df)

        return df_list


    def __init__(self, data, out_path, ed_num):
        # Setup logging
        self.logger = logging_setup()

        self.out_path = out_path
        self.ed_num = ed_num
        self.logger.info("Loading data for Polling District Description")
        self.df = to_dataframe(data, encoding='latin-1')

        self.logger.info("Generating PDP Report Table")
        self.report_dfs = self.gen_report_tables()

        # Set a bunch of things for the report from the first line of the data and create a dict to hold them
        self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)
        self.report_dict = {
            'ed_name': self.row1["ED_NAME_BIL"].to_list()[0],
            'ed_code': self.row1['ED_CODE'].to_list()[0],
            'prov': self.row1['PRVNC_NAME_BIL'].to_list()[0]
        }

        self.logger.info("Creating Report PDF")
        BuildPDDReport(self.report_dict, self.report_dfs, out_dir=self.out_path)

        self.logger.info("Report Generated")
