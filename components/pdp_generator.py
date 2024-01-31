from .commons import logging_setup, to_dataframe, check_dir, csv_to_tbl
import pandas as pd
import sys, os
import arcpy

arcpy.env.overwriteOutput = True

class PDPGenerator:

    def gen_report_table(self) -> str:
        """Generates the table that will be put into the report. Return the table with only the required fields"""

        # Create data copy because we may need the orig later
        out_df = self.df.copy()

        # Create Poll Number field be concating the poll num and suffix
        out_df['PD_NO_CONCAT'] = out_df[['PD_NBR', 'PD_NBR_SFX']].astype(str).apply('-'.join, axis=1)

        out_df['ELECTORS_LISTED'] = ''  # left blank for now until we get the electors counts added to the SQL

        #Export the table and check to ensure that the required directories exist
        out_csv_path = os.path.join(".\\scratch\\", f"{self.header_dict['ed_code']}_pdp.csv")
        check_dir(".\\scratch\\")
        out_df[['PD_NO_CONCAT', 'POLL_NAME', 'ELECTORS_LISTED', 'VOID_IND', 'RDSTRBTN_YEAR', "ED_NAMEE", "ED_NAMEF", 'ED_CODE', 'PRVNC_NAMEE']].to_csv(out_csv_path)
        csv_to_tbl(out_csv_path, f"pdp_{self.header_dict['ed_code']}", os.path.join(self.out_path, "scratch.gdb"))
        return os.path.join(os.path.join(self.out_path, "scratch.gdb"), f"pdp_{self.header_dict['ed_code']}")


    def gen_report(self) -> None:
        """Generates the report from the template using the esri reports function"""
        self.logger.info("Opening report template")
        self.template_aprx = arcpy.mp.ArcGISProject(r"C:\reports_creation\templates\blanks\blank.aprx")

        self.logger.info("Importing Report template")
        self.template_aprx.importDocument(".\\templates\\Report2.rptx")

        self.logger.info("Adding report data to map")
        m = self.template_aprx.listMaps()[0]
        addtab = arcpy.mp.Table(self.cleaned_tbl)
        m.addTable(addtab)
        l = m.listTables()[0] # find the table we just added to the map

        r =  self.template_aprx.listReports()[0]

        self.logger.info("Adding report data to report")
        r.name = f"""
{self.header_dict['dept_nme']}
{self.header_dict['report_type']}
{self.header_dict['rep_order']}
{self.header_dict['ed_namee']}
{self.header_dict['prov']}
{self.header_dict['ed_code']}
        
        """
        r.setReferenceDataSource(l)

        check_dir("\\data")
        self.logger.info("Exporting Report to PDf")
        check_dir(".\\data\\outputs")
        r.exportToPDF(os.path.join(".\\data\\outputs", f"{self.header_dict['ed_code']}_pdp.pdf"))


    def __init__(self, data, out_path):

        # Setup logging
        self.logger = logging_setup()

        self.out_path = out_path

        self.logger.info("Loading data for Polling District Profile")
        self.df = to_dataframe(data, encoding='latin-1')

        # Set a bunch of things for the report from the first line of the data and create a dict to hold them
        self.row1 = self.df.head(1)
        self.header_dict = {
            'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Polling District Profile / Profil de Section de Vote",
            'rep_order': f"Representation order of {self.row1['RDSTRBTN_YEAR'].to_list()[0]} / Décret de représentation de {self.row1['RDSTRBTN_YEAR'].to_list()[0]}",
            'ed_namee': self.row1["ED_NAMEE"].to_list()[0],
            'ed_namef': self.row1["ED_NAMEF"].to_list()[0],
            'ed_code': self.row1['ED_CODE'].tolist()[0],
            'prov': self.row1['PRVNC_NAMEE'].to_list()[0]
        }

        self.logger.info("Generating PDP Report Table")
        self.cleaned_tbl = self.gen_report_table()

        self.logger.info(f"Generating Report: PDP for {self.header_dict['ed_code']}")
        self.gen_report()

        self.logger.info("Report Generated")


if __name__ == "__main__":
    PDPGenerator(data=r"C:\reports_creation\data\ed_desc_test.csv", out_path=r"C:\reports_creation\data\outputs")
