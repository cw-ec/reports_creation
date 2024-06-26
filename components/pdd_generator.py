from .commons import logging_setup, to_dataframe, create_dir,  to_excel, get_excel_header
from .builders import BuildPDDReport
import pandas as pd
import os, sys

pd.options.mode.chained_assignment = None  # default='warn'

"""
Process the input data for the PDD report and calls the PDD builder function to finish the report. 
"""

class PDDGenerator:

    def is_valid(self, data, out_path, ed_num, strm_data_path, pd_add_data_path) -> None:
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
        if not os.path.exists(strm_data_path):
            self.logger.exception(f"Parameter strm_data_path does not exists: strm.csv must exist and be in the same directory as pd_desc.csv")
        if not os.path.exists(pd_add_data_path):
            self.logger.exception(f"Parameter pd_add_data_path does not exists: pd_add.csv must exist and be in the same directory as pd_desc.csv")

    def gen_report_tables(self) -> list:
        """Generates the table that will be put into the report. Return the table with only the required fields"""

        # Create data copy because we may need the orig later
        out_df = self.df[self.df["ED_CODE"] == self.ed_num].copy()
        ed_strm_df = self.strm_df[self.strm_df['ED_CODE'] == self.ed_num].copy()
        ed_strm_df.dropna(subset=['TWNSHIP'], inplace=True)

        if len(out_df) == 0:  # If no data available return empty list
            return []

        # Create Poll Number field be concatenating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)
        out_df = out_df.sort_values(by=['PD_NBR', 'PD_NBR_SFX', 'ST_PARSED_NAME', 'ST_TYP_CDE', 'ST_DRCTN_CDE', 'FROM_CIV_NUM', 'FROM_CROSS_FEAT'], na_position='first') # Sort ascending

        for f in ['ED_NAMEE', 'ED_NAMEF', 'POLL_NAME_FIXED']:  # en-dashes for report excel file
            out_df[f] = out_df[f].apply(lambda x: x.replace('--', '—'))

        to_excel(df=out_df[["ED_CODE", "ED_NAMEE", "ED_NAMEF", "FULL_PD_NBR", "PD_NBR", "PD_NBR_SFX", "POLL_NAME_FIXED", "PLACE_NAME",
             "CSD_TYP_DESC_BIL", "ST_NME", "ST_TYP_CDE", "ST_DRCTN_CDE", "FROM_CROSS_FEAT", "TO_CROSS_FEAT","FROM_CIV_NUM", "TO_CIV_NUM", "ST_SIDE_DESC_BIL", "ADV_PD_NBR"]],
                 out_dir=self.out_path,
                 out_nme=f"DESCRI_{self.ed_num}",
                 header=get_excel_header(self.ed_num, 'PDD'))

        # Set dataframes field order and keep only essential fields
        out_df = out_df[['PD_NO_CONCAT', 'STREET_NME_FULL','STREET_NME_FULL_ENG', 'STREET_NME_FULL_FRE', 'FROM_CROSS_FEAT', 'TO_CROSS_FEAT', 'FROM_CIV_NUM', 'TO_CIV_NUM', 'ST_SIDE_DESC_BIL', 'POLL_NAME_FIXED', "FULL_PLACE_NAME"]]
        ed_strm_df = ed_strm_df[['FULL_PD_NBR', 'TWNSHIP', 'RNGE', 'MRDN', 'SECTION']]
        ed_strm_df = ed_strm_df.sort_values(by=['FULL_PD_NBR', 'MRDN', 'TWNSHIP','RNGE'], na_position='first')

        # Add en dashes to text
        out_df['POLL_NAME_FIXED'] = out_df['POLL_NAME_FIXED'].apply(lambda x: x.replace('--', '—'))

        df_list = []
        # Create a df for each pd and append it to the df list
        for pd in out_df['PD_NO_CONCAT'].unique().tolist(): # Iterate over list of unique pd numbers
            pd_df = out_df[out_df['PD_NO_CONCAT'] == pd ].copy()
            pd_df.sort_values('STREET_NME_FULL')
            df_list.append(pd_df)

            # if the ed contains strms then add that to the list of tables check to make sure the records are populated
            pd_strms = ed_strm_df[ed_strm_df['FULL_PD_NBR'] == pd]
            if (len(pd_strms['TWNSHIP'].unique().tolist()) >= 1):
                pd_strms.drop(columns=['FULL_PD_NBR'], inplace=True)
                df_list.append(pd_strms)

        return df_list


    def __init__(self, data, out_path, ed_num):
        # Setup logging
        self.logger = logging_setup()

        strm_path = os.path.join(os.path.split(data)[0], 'strm.csv')
        pd_add_path = os.path.join(os.path.split(data)[0], 'ps_add.csv')

        self.is_valid(data, out_path, ed_num, strm_path, pd_add_path)

        self.out_path = out_path
        self.ed_num = ed_num
        self.df = to_dataframe(data, encoding='latin-1')
        self.strm_df = to_dataframe(strm_path, encoding='latin-1')  # STRM Data
        self.ps_add = to_dataframe(pd_add_path, encoding='latin-1')  # PD Address full data

        self.report_dfs = self.gen_report_tables()

        if len(self.report_dfs) == 0:
            self.logger.warn(f"No data available for {self.ed_num}. Check input data or workflow")
            self.logger.info(f"No PDD report generated for {self.ed_num}")

        else:
            # Set a bunch of things for the report from the first line of the data and create a dict to hold them
            self.row1 = self.df[self.df['ED_CODE'] == self.ed_num].head(1)

            self.ps_add = self.ps_add[(self.ps_add['PD_NBR'] >= 400) & (self.ps_add['ED_CODE'] == self.ed_num)]  # We only need the records for single building and mobile polls for the ed we're working with
            # Drop PD_ID from this list after database is updated as it will no longer be needed (only needed for join to electos xlsx)
            self.ps_add = self.ps_add[['FULL_PD_NBR', 'SITE_NAME_BIL', 'FINAL_SITE_ADDRESS', 'FULL_SBPD_PLACE', 'CPC_PRVNC_NAME', 'SITE_PSTL_CDE', 'SITE_PLACE_NAME', 'ELECTORS_LISTED', 'PD_ID']]

            # Electors listed join data until database get updated
            self.ec_df = to_dataframe(".\\data\ELECTOR_COUNTS.xlsx", encoding='latin-1')  # Placeholder until database table gets updates
            self.ps_add =  self.ps_add.merge(self.ec_df[["PD_ID", "ELECTOR_COUNT"]], on="PD_ID", how='left')
            self.ps_add.drop(columns=['ELECTORS_LISTED', 'PD_ID'], inplace=True)
            self.ps_add.rename(columns={"ELECTOR_COUNT": "ELECTORS_LISTED"}, inplace=True)
            self.ps_add['ELECTORS_LISTED'] = self.ps_add['ELECTORS_LISTED'].fillna(0)

            self.report_dict = {
                'ed_name': self.row1["ED_NAME_BIL"].to_list()[0].replace('--', '—'),
                'ed_code': self.row1['ED_CODE'].to_list()[0],
                'prov': self.row1['PRVNC_NAME_BIL'].to_list()[0],
                'rep_yr': self.row1['RDSTRBTN_YEAR'].to_list()[0]
            }

            # Ensure that the output directory exists
            create_dir(self.out_path)

            # Build the report
            BuildPDDReport(self.report_dict, self.report_dfs, self.ps_add, out_dir=self.out_path)

            self.logger.info("Report Generated")
