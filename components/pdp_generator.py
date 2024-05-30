# -*- coding: utf-8 -*-
from .commons import logging_setup, to_dataframe, create_dir, get_ed_name_from_code, to_excel, get_excel_header
from .builders import BuildPDPReport
from .builders.report_parameters import PDPSettings
import pandas as pd
import sys, os

class PDPGenerator:

    def is_valid(self, data, out_path, ed_num) -> None:
        """Checks to see if inputs are valid"""

        if not isinstance(data, str) or not os.path.exists(data):
            self.logger.exception(f"Parameter data is not of type string or does not exist")
            raise Exception(f"Parameter data is not of type string or does not exist")
        if not isinstance(out_path, str):
            self.logger.exception(f"Parameter out_path must be of type string. Currently type: {type(out_path)}")
            raise Exception(f"Parameter out_path must be of type string. Currently type: {type(out_path)}")
        if not isinstance(ed_num, int):
            self.logger.exception(f"Parameter ed_num must be an integer. Currently type: {type(ed_num)}")
            raise Exception(f"Parameter ed_num must be an integer. Currently type: {type(ed_num)}")

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

            # out_df['ELECTORS_LISTED'] = 123  # 123 placeholder for now until we get the electors counts added to the SQL
            out_df = out_df.merge(self.ec_df[["PD_ID", "ELECTOR_COUNT"]], on="PD_ID", how='left')
            out_df.drop(columns=['ELECTORS_LISTED'], inplace=True)
            out_df.rename(columns={"ELECTOR_COUNT":"ELECTORS_LISTED"}, inplace=True)

            out_df['ELECTORS_LISTED'] = out_df['ELECTORS_LISTED'].fillna(0)

            for f in ['ED_NAMEE', 'ED_NAMEF', 'POLL_NAME_FIXED']:  # en-dashes for report excel file
                out_df[f] = out_df[f].apply(lambda x: x.replace('--', '—'))

            # Send the table to be exported to the out directory
            to_excel(out_df[["ED_CODE", "ED_NAMEE", "ED_NAMEF", "FULL_PD_NBR", "PD_NBR", "PD_NBR_SFX", "POLL_NAME_FIXED", "ELECTORS_LISTED", "VOID_IND"]],
                     out_dir= self.out_path,
                     out_nme=f"PD_PROF_{self.ed_num}",
                     header= get_excel_header(self.ed_num, 'PDP'),
                     )

            out_df["VOID_IND"] = out_df["VOID_IND"].replace('N', '') # No need to show N's replace with nothing
            return out_df[['PD_NO_CONCAT', 'POLL_NAME_FIXED', 'ELECTORS_LISTED', 'VOID_IND']]

    def __init__(self, data, out_path, ed_num):

        # Setup logging
        self.logger = logging_setup()

        self.is_valid(data, out_path, ed_num)

        self.out_path = out_path
        self.ed_num = ed_num
        self.df = to_dataframe(data, encoding='latin-1')
        self.ec_df = to_dataframe(".\\data\ELECTOR_COUNTS.xlsx", encoding='latin-1')  # Placeholder until database table gets updates

        self.report_df = self.gen_report_table()

        if len(self.report_df) == 0:
            self.logger.warn(f"No data available for PDP on {self.ed_num}. Check input data or workflow")
            self.logger.info(f"No PDP report generated for {self.ed_num}")

        else:
            # Set a bunch of things for the report from the first line of the data and create a dict to hold them
            self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)

            self.report_dict = {
                'ed_name': self.row1["ED_NAME_BIL"].to_list()[0].replace('--', '—'),
                'ed_code': self.row1['ED_CODE'].to_list()[0],
                'prov': self.row1['PRVNC_NAME_BIL'].to_list()[0],
                'rep_yr':self.row1['RDSTRBTN_YEAR'].to_list()[0]
            }

            create_dir(self.out_path)
            BuildPDPReport(self.report_dict, self.report_df, out_dir=self.out_path)

            self.logger.info("Report Generated")
