from math import isnan
from .commons import logging_setup, to_dataframe, create_dir, to_excel, get_excel_header
from .builders import BuildDPKReport
import pandas as pd
import sys, os

pd.options.mode.chained_assignment = None  # default='warn'


class DPKGenerator:

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

    def gen_report_tables(self) -> list:
        """Generates the table that will be put into the report. Return the table with only the required fields"""

        # Create data copy because we may need the orig later
        out_df = self.df[self.df["ED_CODE"] == self.ed_num].copy()

        if len(out_df) == 0:
            return []

        # Sort the input data (fields ordered as requested)
        out_df = out_df.sort_values(
            by=['ED_CODE', 'ST_PARSED_NAME', 'ST_TYP_CDE', 'ST_DRCTN_CDE', 'FULL_PLACE_NAME', 'FROM_CIV_NUM', 'FROM_CROSS_FEAT', 'PD_NBR', 'PD_NBR_SFX', 'ST_SIDE_DESC_BIL'],
            na_position='first')  # Sort ascending with NAN first

        for f in ['ED_NAMEE', 'ED_NAMEF', 'POLL_NAME_FIXED']:  # en-dashes for report excel file
            out_df[f] = out_df[f].apply(lambda x: x.replace('--', '—'))

        to_excel(df=out_df[["ED_CODE", "ED_NAMEE", "ED_NAMEF", "ST_NME", "ST_TYP_CDE", "ST_DRCTN_CDE", "PLACE_NAME", "CSD_TYP_DESC_BIL", "FROM_CROSS_FEAT", "TO_CROSS_FEAT","FROM_CIV_NUM", "TO_CIV_NUM", "ST_SIDE_DESC_BIL", "FULL_PD_NBR", "PD_NBR", "PD_NBR_SFX", "POLL_NAME_FIXED",  "ADV_PD_NBR"]],
                 out_dir=self.out_path,
                 out_nme=f"INDCIR_{self.ed_num}",
                 header=get_excel_header(self.ed_num, "DPK")
                 )
        # Create Poll Number field be concatenating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)

        out_df["ADV_PD_NBR"] = out_df["ADV_PD_NBR"].apply(lambda x: str(int(x)) if not isnan(x) else '')  # Make sure these are integers if nan make it an empty string

        out_df = out_df[['STREET_NME_FULL', 'FROM_CROSS_FEAT', 'TO_CROSS_FEAT', 'FROM_CIV_NUM', 'TO_CIV_NUM', 'ST_SIDE_DESC_BIL', 'PD_NO_CONCAT', 'ADV_PD_NBR', 'FULL_PLACE_NAME']]

        df_list = []

        # Create a df for each pd and append it to the df list
        for str_nme in out_df['STREET_NME_FULL'].unique().tolist(): # Iterate over list of unique street names
            str_df = out_df[out_df['STREET_NME_FULL'] == str_nme].copy()

            for pl_nme in str_df['FULL_PLACE_NAME'].unique().tolist():  # iterate over each place name as the same street name can be in multiple places
                pl_df = str_df[str_df['FULL_PLACE_NAME'] == pl_nme]

                if len(pl_df) >= 1:  # Make sure there are records in the table before adding it to the table list
                    df_list.append(pl_df)

        return df_list


    def __init__(self, data, out_path, ed_num):
        # Setup logging
        self.logger = logging_setup()

        self.is_valid(data, out_path, ed_num)

        self.out_path = out_path
        self.ed_num = ed_num
        self.df = to_dataframe(data, encoding='latin-1')

        self.report_dfs = self.gen_report_tables()

        if len(self.report_dfs) == 0:
            self.logger.warn(f"Data for {self.ed_num} contains no data. Report not generated")

        else:
            # Set a bunch of things for the report from the first line of the data and create a dict to hold them
            self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)

            self.report_dict = {
                'ed_name': self.row1["ED_NAME_BIL"].to_list()[0].replace('--', '—'),
                'ed_code': self.row1['ED_CODE'].to_list()[0],
                'prov': self.row1['PRVNC_NAME_BIL'].to_list()[0],
                'rep_yr': self.row1['RDSTRBTN_YEAR'].to_list()[0]
            }
            create_dir(self.out_path)
            BuildDPKReport(self.report_dict, self.report_dfs, out_dir=self.out_path)

            self.logger.info("Report Generated")
