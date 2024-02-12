# -*- coding: utf-8 -*-
from components import logging_setup, to_dataframe, create_dir, add_en_dash
from components.builders.build_apd_report import BuildAPDReport
import pandas as pd

class APDGenerator:
    """ Responsible for generating the Advance Polling Districts Report"""

    def gen_report_table(self) -> pd.DataFrame:
        """Takes the input dataframe and filters / transforms it so that its report ready"""
        # Create data copy because we may need the orig later
        out_df = self.df.copy()

        out_df = out_df[out_df["ED_CODE"] == self.ed_num]

        # Create Poll Number field be concatenating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)
        fields = ["ADV_PD_NBR", "ADV_POLL_NAME_FIXED", 'PD_NO_CONCAT']

        # Create list of all PD numbers (concatenated) in each PD
        grouped = out_df[['PD_NO_CONCAT', 'ADV_PD_NBR']].groupby('ADV_PD_NBR').agg(list)
        grouped.rename(columns={'PD_NO_CONCAT': 'PD_LIST'}, inplace=True)

        # Join the tables together so that ADV_PD_NBR and ADV POLL name are with the list of pds
        out_df = out_df[["ADV_PD_NBR", "ADV_POLL_NAME_FIXED"]].drop_duplicates(subset='ADV_PD_NBR', keep='first').join(grouped, on="ADV_PD_NBR")

        # Drop NAN rows if any
        out_df = out_df[~out_df['ADV_PD_NBR'].isnull()]
        out_df['ADV_PD_NBR'] = out_df['ADV_PD_NBR'].astype(int)

        # Fix en dashes in the adv poll name
        out_df["ADV_POLL_NAME_FIXED"] = out_df["ADV_POLL_NAME_FIXED"].apply(lambda x: add_en_dash(x))

        out_df['TOTAL'] = out_df['PD_LIST'].apply(lambda x: len(x) if isinstance(x, list) else 0 ) # Create a field that gives us how many pds are in the apd
        out_df['PD_LIST'] = out_df['PD_LIST'].apply(lambda  x: ', '.join(x) if isinstance(x,list) else '')  # Convert from list to string (list breaks reportlab)

        return out_df


    def __init__(self, data, out_path, ed_num):

        # Setup logging
        self.logger = logging_setup()

        self.out_path = out_path
        self.ed_num = ed_num
        self.logger.info("Loading data for Advanced Polling Districts")
        self.df = to_dataframe(data, encoding='latin-1')

        self.logger.info("Generating PDP Report Table")
        self.report_df = self.gen_report_table()

        # Set a bunch of things for the report from the first line of the data and create a dict to hold them
        self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)

        self.report_dict = {
            'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Advance Polling Districts / Districts de vote par anticipation",
            'rep_order': f"Representation order of 2013 / Décret de représentation de 2013",
            'ed_name': add_en_dash(self.row1["ED_NAME_BIL"].to_list()[0]),
            'ed_code': self.row1['ED_CODE'].to_list()[0],
            'prov': add_en_dash(self.row1['PRVNC_NAME_BIL'].to_list()[0])
        }

        self.logger.info("Creating Report PDF")
        BuildAPDReport(self.report_dict, self.report_df, out_dir=self.out_path)

        self.logger.info("Report Generated")
