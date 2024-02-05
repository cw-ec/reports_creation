from .commons import logging_setup, to_dataframe
from .build_report import BuildReport
import pandas as pd



class PDPGenerator:

    def gen_report_table(self) -> pd.DataFrame:
        """Generates the table that will be put into the report. Return the table with only the required fields"""

        # Create data copy because we may need the orig later
        out_df = self.df.copy()

        # Create Poll Number field be concatenating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)

        out_df['ELECTORS_LISTED'] = 123  # 123 placeholder for now until we get the electors counts added to the SQL

        return out_df[['PD_NO_CONCAT', 'POLL_NAME', 'ELECTORS_LISTED', 'VOID_IND']]


    def __init__(self, data, out_path, ed_num):

        # Setup logging
        self.logger = logging_setup()

        self.out_path = out_path
        self.ed_num = ed_num
        self.logger.info("Loading data for Polling District Profile")
        self.df = to_dataframe(data, encoding='latin-1')

        self.logger.info("Generating PDP Report Table")
        self.report_df = self.gen_report_table()

        # Set a bunch of things for the report from the first line of the data and create a dict to hold them
        self.row1 = self.df.head(1)

        self.report_dict = {
            'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Polling District Profile / Profil de Section de Vote",
            'rep_order': f"Representation order of {self.row1['RDSTRBTN_YEAR'].to_list()[0]} / Décret de représentation de {self.row1['RDSTRBTN_YEAR'].to_list()[0]}",
            'ed_namee': self.row1["ED_NAMEE"].to_list()[0],
            'ed_namef': self.row1["ED_NAMEF"].to_list()[0],
            'ed_code': self.row1['ED_CODE'].to_list()[0],
            'prov': self.row1['PRVNC_NAMEE'].to_list()[0]
        }

        self.logger.info("Creating Report PDF")
        self.template = BuildReport('pdp', self.report_dict, self.report_df, out_dir=self.out_path)

        self.logger.info("Report Generated")


if __name__ == "__main__":
    PDPGenerator(data=r"C:\reports_creation\data\47001_nums.csv",
                 out_path=r"C:\reports_creation\data\outputs",)