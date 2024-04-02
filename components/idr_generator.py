# -*- coding: latin-1 -*-
from .commons import logging_setup, to_dataframe, create_dir, add_en_dash, get_prov_from_code, get_ed_name_from_code
from .builders import BuildIDRReport
import pandas as pd
import sys

class IDRGenerator:

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

            out_df.rename(columns={"NAME_2": "C_NAME"}, inplace=True)
            out_df = drop_multipart(out_df, "C_NAME","COMMUNITY_TYPE_F", "PD_NO_CONCAT")
            return out_df[["C_NAME","COMMUNITY_TYPE_F", "PD_NO_CONCAT"]]

        else: # RoC

            out_df.rename(columns={"NAME_1": "C_NAME"}, inplace=True)
            out_df = drop_multipart(out_df, "C_NAME","COMMUNITY_TYPE_E", "PD_NO_CONCAT")
            return out_df[["C_NAME", "COMMUNITY_TYPE_E", "PD_NO_CONCAT"]]

    def __init__(self, idr_data, out_path, ed_num):

        # Setup logging
        self.logger = logging_setup()

        self.out_path = out_path
        self.ed_num = ed_num
        self.logger.info("Loading data for Indigenous Lands Report")
        self.df = to_dataframe(idr_data, encoding='latin-1', sheet_name="PDs and Indigenous Communities")

        self.logger.info("Generating IDR Report Table")
        self.report_df = self.gen_report_table()

        if len(self.report_df) == 0:
            self.logger.info(f"No Communities with Indigenous Peoples found in {self.ed_num}. No report generated.")

        else:
            # Set a bunch of things for the report from the first line of the data and create a dict to hold them
            self.row1 = self.df[self.df['FED_NUM'] == self.ed_num].head(1)

            self.report_dict = {
                'ed_name': get_ed_name_from_code(int(self.ed_num)), # No need to join made dict get match via function
                'ed_code': self.ed_num,
                'prov': get_prov_from_code(int(self.ed_num)) # No prov in indigenous data. Get from ED_NUM
            }
            create_dir(self.out_path)
            self.logger.info("Creating Report PDF")

            BuildIDRReport(self.report_dict, self.report_df, out_dir=self.out_path)

            self.logger.info("Report Generated")
