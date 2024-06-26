# -*- coding: utf-8 -*-
from .commons import logging_setup, to_dataframe, create_dir, to_excel, get_excel_header
from .builders import BuildMPSReport
import pandas as pd
from math import isnan
import sys, os

"""
Process the input data for the MPS report and calls the MPS builder function to finish the report. 
"""

class MPSGenerator:

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
        out_df = out_df[(out_df["ED_CODE"] == self.ed_num) & (out_df["PD_NBR"] >= 500)]  # Get only mobile poll records for the ed of interest

        if len(out_df) == 0:
            return out_df

        # Create Poll Number field be concatenating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)
        # out_df['ELECTORS_LISTED'] = 123  # 123 placeholder for now until we get the electors counts added to the SQL

        out_df = out_df.merge(self.ec_df[["PD_ID", "ELECTOR_COUNT"]], on="PD_ID", how='left')
        out_df.drop(columns=['ELECTORS_LISTED'], inplace=True)
        out_df.rename(columns={"ELECTOR_COUNT": "ELECTORS_LISTED"}, inplace=True)
        out_df['ELECTORS_LISTED'] = out_df['ELECTORS_LISTED'].fillna(0)

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
        out_df['APD_LIST'] = out_df['APD_LIST'].apply(lambda x: [y for y in x if not isnan(y)])  # Remove all nulls from the list
        out_df['APD_LIST'] = out_df['APD_LIST'].apply(lambda x: str([int(y) for y in x])[1:-1] if (isinstance(x, list)) and (len(x)!=0) else '')

        # Drop Duplicates before sending to builder
        out_df = out_df.drop_duplicates(subset='PD_NO_CONCAT', keep='first')
        out_df = out_df[out_df["VOID_IND"]=='N']

        if len(out_df) > 0:

            for f in ['ED_NAMEE', 'ED_NAMEF']:  # en-dashes for report excel file
                out_df[f] = out_df[f].apply(lambda x: x.replace('--', '—'))

            to_excel(df=out_df[["ED_CODE", "ED_NAMEE", "ED_NAMEF", "FULL_PD_NBR", "PD_NBR", "PD_NBR_SFX", "TOTAL_INST", "ELECTORS_LISTED", "ADV_PD_NBR"]],
                     out_dir=self.out_path,
                     out_nme=f"SUMINS_{self.ed_num}",
                     header=get_excel_header(self.ed_num, "MPS"))

        return out_df[['PD_NO_CONCAT', 'TOTAL_INST', 'ELECTORS_LISTED', 'APD_LIST']]

    def __init__(self, data, out_path, ed_num) -> None:

        # Setup logging
        self.logger = logging_setup()

        self.is_valid(data, out_path, ed_num)  # Validate inputs

        self.out_path = out_path
        self.ed_num = ed_num
        self.df = to_dataframe(data, encoding='latin-1')
        self.ec_df = to_dataframe(".\\data\ELECTOR_COUNTS.xlsx", encoding='latin-1')  # Placeholder until database table gets updated

        self.report_df = self.gen_report_table()

        if len(self.report_df) == 0:
            self.logger.warn(f"No MPS report generated for {self.ed_num} as no data was available. Check data or workflow and try again.")

        else:
            # Set a bunch of things for the report from the first line of the data and create a dict to hold them
            self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)

            self.report_dict = {
                'ed_name': self.row1["ED_NAME_BIL"].to_list()[0].replace('--', '—'),
                'ed_code': self.row1['ED_CODE'].to_list()[0],
                'prov': self.row1['PRVNC_NAME_BIL'].to_list()[0],
                'rep_yr': self.row1['RDSTRBTN_YEAR'].to_list()[0]
            }
            # Ensure that the output directory exists
            create_dir(self.out_path)
            BuildMPSReport(self.report_dict, self.report_df, out_dir=self.out_path)

            self.logger.info("Report Generated")
