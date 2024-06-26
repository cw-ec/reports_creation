# -*- coding: utf-8 -*-
from .commons import logging_setup, to_dataframe, create_dir, get_prov_from_code, get_ed_name_from_code
from .builders import BuildIDRReport
import pandas as pd
import sys, os

"""
Process the input data for the IDR report and calls the IDR builder function to finish the report. 
"""

class IDRGenerator:

    def is_valid(self, data, out_path, ed_num, sheet_name) -> None:
        """Checks to see if inputs are valid. Returns an exception if any inputs fail"""
        if not isinstance(data, str) or not os.path.exists(data):
            self.logger.exception(f"Parameter data is not of type string or does not exist")
            raise Exception(f"Parameter data is not of type string or does not exist")
        if not isinstance(out_path, str):
            self.logger.exception(f"Parameter out_path must be of type string. Currently type: {type(out_path)}")
            raise Exception(f"Parameter out_path must be of type string. Currently type: {type(out_path)}")
        if not isinstance(ed_num, int):
            self.logger.exception(f"Parameter ed_num must be an integer. Currently type: {type(ed_num)}")
            raise Exception(f"Parameter ed_num must be an integer. Currently type: {type(ed_num)}")
        if not isinstance(sheet_name, str):
            self.logger.exception(f"Parameter sheet_name: Must be of type string. Currently type: {type(sheet_name)}")

    def gen_report_table(self) -> pd.DataFrame:
        """Generates the table that will be put into the report. Return the table with only the required fields"""

        def drop_multipart(df: pd.DataFrame, community_fld: str, desc_fld:str, pd_num_fld:str) -> pd.DataFrame:
            """Finds multipart communities and drops duplicate records when they have the same pd number"""

            multi = df[df.duplicated(subset=[community_fld,desc_fld, pd_num_fld], keep='first')]

            if len(multi) == 0:  # if there are no multipart features return the original data
                return df
            else:  # Where multipart features are present check for and remove those with matching pd_nums
                out = df[~df.index.isin(multi.index.values.tolist())]
                return out

        # Create data copy because we may need the orig later
        out_df = self.df.copy()
        out_df = out_df[out_df["FED_NUM"] == self.ed_num]

        # If there are no Indigenous lands in the ED return the empty dataframe
        if len(out_df) == 0:
            return out_df

        # Create Poll Number field be concatenating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NUM', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)

        # Fields are different when in English or French provinces this logic returns the correct fields for that
        if (self.ed_num >= 24000) and (self.ed_num < 25000): # Quebec

            out_df['C_TYPE'] = out_df[['COMMUNITY_TYPE_F', 'COMMUNITY_TYPE_E']].apply(lambda x: f"{x.iloc[0]} / {x.iloc[1]}",axis=1)  # Concat the community type fields
            out_df.rename(columns={"NAME_2": "C_NAME"}, inplace=True)
            out_df = drop_multipart(out_df, "C_NAME","COMMUNITY_TYPE_F", "PD_NO_CONCAT")
            return out_df[["C_NAME","C_TYPE", "PD_NO_CONCAT"]]

        else: # RoC

            out_df['C_TYPE'] = out_df[['COMMUNITY_TYPE_E', 'COMMUNITY_TYPE_F']].apply(lambda x: f"{x.iloc[0]} / {x.iloc[1]}", axis=1)  # Concat the community type fields
            out_df.rename(columns={"NAME_1": "C_NAME"}, inplace=True)
            out_df = drop_multipart(out_df, "C_NAME","COMMUNITY_TYPE_E", "PD_NO_CONCAT")
            return out_df[["C_NAME", "C_TYPE", "PD_NO_CONCAT"]]

    def __init__(self, idr_data, out_path, ed_num, sheet_name="PDs and Indigenous Communities"):

        # Setup logging
        self.logger = logging_setup()

        self.is_valid(idr_data, out_path, ed_num, sheet_name)  # run the validator

        self.out_path = out_path
        self.ed_num = ed_num
        self.df = to_dataframe(idr_data, encoding='latin-1', sheet_name=sheet_name)

        self.report_df = self.gen_report_table()

        if len(self.report_df) == 0:
            self.logger.warn(f"No data for Communities with Indigenous Peoples found in {self.ed_num}. No report generated.")

        else:
            # Set a bunch of things for the report from the first line of the data and create a dict to hold them
            self.row1 = self.df[self.df['FED_NUM'] == self.ed_num].head(1)

            self.report_dict = {
                'ed_name': get_ed_name_from_code(int(self.ed_num)).replace('--', '—'), # No need to join made dict get match via function
                'ed_code': self.ed_num,
                'prov': get_prov_from_code(int(self.ed_num)) # No prov in indigenous data. Get from ED_NUM
            }
            create_dir(self.out_path)

            # Run the report builder
            BuildIDRReport(self.report_dict, self.report_df, out_dir=self.out_path)

            self.logger.info("Report Generated")
