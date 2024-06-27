# -*- coding: utf-8 -*-
from .commons import logging_setup, to_dataframe, to_excel, get_excel_header
from .builders import BuildAPDReport
import pandas as pd
import sys, os

"""
This script contains the class responsible for prepping input data so that it is ready for the APD report.
"""

class APDGenerator:
    """ Responsible for generating the Advance Polling Districts Report"""

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
        """Takes the input dataframe and filters / transforms it so that its report ready"""
        # Create data copy because we may need the orig later
        out_df = self.df.copy()

        out_df = out_df[out_df["ED_CODE"] == self.ed_num]

        if len(out_df) == 0:
            return out_df

        else:

            # Create Poll Number field be concatenating the poll num and suffix
            out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)

            # Create list of all PD numbers (concatenated) in each APD
            grouped = out_df[['PD_NO_CONCAT', 'ADV_PD_NBR']].groupby('ADV_PD_NBR').agg(list)
            grouped.rename(columns={'PD_NO_CONCAT': 'PD_LIST'}, inplace=True)

            # Join the tables together so that ADV_PD_NBR and ADV POLL name are with the list of pds
            out_df = out_df.drop_duplicates(subset='ADV_PD_NBR', keep='first').join(grouped, on="ADV_PD_NBR")

            # Drop NAN rows if any
            out_df = out_df[~out_df['ADV_PD_NBR'].isnull()]
            out_df['ADV_PD_NBR'] = out_df['ADV_PD_NBR'].astype(int)
            out_df = out_df.sort_values(by='ADV_PD_NBR', ascending=True)

            out_df['TOTAL'] = out_df['PD_LIST'].apply(lambda x: len(x) if isinstance(x, list) else 0 ) # Create a field that gives us how many pds are in the apd
            out_df['PD_LIST'] = out_df['PD_LIST'].apply(lambda  x: ', '.join(x) if isinstance(x,list) else '')  # Convert from list to string (list breaks reportlab)

            for f in ['ED_NAMEE', 'ED_NAMEF', "ADV_POLL_NAME_FIXED"]:  # en-dashes for report excel file
                out_df[f] = out_df[f].apply(lambda x: x.replace('--', '—'))
            to_excel(df=out_df[
                ["ED_CODE", "ED_NAMEE", "ED_NAMEF", "FULL_ADV_PD_NBR", "ADV_PD_NBR", "ADV_PD_NBR_SFX", "ADV_POLL_NAME_FIXED", "PD_LIST", "TOTAL"]],
                     out_dir=self.out_path,
                     out_nme=f"ADVANC_{self.ed_num}",
                     header=get_excel_header(self.ed_num, 'APD'))

            # Fix en dashes in the adv poll name
            out_df["ADV_POLL_NAME_FIXED"] = out_df["ADV_POLL_NAME_FIXED"].apply(lambda x: x.replace('--', '—'))

            return out_df[['ADV_PD_NBR', 'ADV_POLL_NAME_FIXED', 'PD_LIST', 'TOTAL']]


    def __init__(self, data, out_path, ed_num) -> None:

        # Setup logging
        self.logger = logging_setup()

        self.is_valid(data, out_path, ed_num)  # Validates Inputs

        self.out_path = out_path
        self.ed_num = ed_num
        self.df = to_dataframe(data, encoding='latin-1')

        self.logger.info("Generating ADP Report Table")
        self.report_df = self.gen_report_table()

        # Check if there is still data available after processing.
        if len(self.report_df) == 0:  # If not then don't continue processing and warm the user
            self.logger.warn(f"No APD report generated for {self.ed_num} as no data was available. Check data or workflow and try again.")

        else:  # If there is still data then continue processing
            # Set a bunch of things for the report from the first line of the data and create a dict to hold them
            self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)

            self.report_dict = {
                'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
                'report_type': "Advance Polling Districts / Districts de vote par anticipation",
                'rep_yr': self.row1['RDSTRBTN_YEAR'].to_list()[0],
                'ed_name': self.row1["ED_NAME_BIL"].to_list()[0].replace('--', '—'),
                'ed_code': self.row1['ED_CODE'].to_list()[0],
                'prov': self.row1['PRVNC_NAME_BIL'].to_list()[0]
            }

            # Run the builder class to construct the report
            BuildAPDReport(self.report_dict, self.report_df, out_dir=self.out_path)

            self.logger.info("Report Generated")
