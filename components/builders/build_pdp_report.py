# -*- coding: utf-8-*-
import datetime
import numpy as np
import pandas as pd
from components.commons import logging_setup
import os, sys
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, PageBreak
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .common_builds import *
from .report_parameters import PDPSettings

registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

"""
Builder class for the PDP Report
"""

class BuildPDPReport:
    """Builds the report pdf with a header and footer"""

    def pdp_report_pages(self) -> None:
        """Setups the template for the pdp report"""

        def add_report_table(c_widths: list) -> Table:
            """Sets the table"""
            ts = [
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]

            # Copy the dataframe and style the pd number column
            df = self.data_df.copy()
            df['PD_NO_CONCAT'] = df['PD_NO_CONCAT'].apply(lambda x: Paragraph(x, style=self.styles['CellText']))

            # Make the electors listed values prettier
            df["ELECTORS_LISTED"] = df["ELECTORS_LISTED"].astype("string").fillna('')
            df["ELECTORS_LISTED"] = df["ELECTORS_LISTED"].apply(lambda x: Paragraph(str(int(float(x))), style=self.styles['CellText']) if len(x) > 0 else x)

            # Build the table
            lista = [[Paragraph(f"<b>{x}</b>", style=self.styles['ColHeaderTxt']) for x in self.settings_dict['table_header']]] + df.values.tolist()
            tbl = Table(lista, style=ts, repeatRows=1, colWidths=c_widths)

            return tbl

        def add_summary_box(c_widths:list) -> Table:
            """Adds the summary stats box at the bottom of the main table."""

            # Table Style Setup
            ts = [
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), "BOTTOM"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]

            # Apply cell text style to text based fields
            for c in ["POLL_NAME_FIXED", 'PD_NO_CONCAT']:
                self.data_df[c] = self.data_df[c].apply(
                    lambda x: Paragraph(x, style=self.styles['CellText']))


            stats_df = self.data_df[self.data_df['VOID_IND']=='']  # '' because 'N' gets removed in the generator

            # Calc Stats
            total_active_pd = str(int(len(stats_df)))  # Total # of pd's with VOID_IND == 'N'
            total_electors = str(int(stats_df['ELECTORS_LISTED'].sum()))

            # Because sometimes the values might be NaN
            try:
                avg_ele_per_pd = str(int(round(stats_df['ELECTORS_LISTED'].dropna(how='all').mean(),0)))

            except ValueError:
                self.logger.warn(f"AVERAGE ELECTOR PER PD: summary statistic cannot be converted to an integer check elector count values. Replacing Null Value with NaN")
                avg_ele_per_pd = np.NaN

            total_void = str(int(len(self.data_df[self.data_df['VOID_IND'] =='Y'])))

            # Setup Summary Stats DF
            cols = [self.settings_dict['ss_table_header'], '']
            stats = [(Paragraph(self.settings_dict['ss_total_apd'], self.styles['SingleCellText']), total_active_pd),
                     (Paragraph(self.settings_dict['ss_total_noe'], self.styles['SingleCellText']), total_electors),
                     (Paragraph(self.settings_dict['ss_avg_noe_per_apd'], self.styles['SingleCellText']), avg_ele_per_pd),
                     (Paragraph(self.settings_dict['ss_total_vpd'], self.styles['SingleCellText']), total_void)]

            # Convert the df to a table and export
            stats_df = pd.DataFrame(stats,index=range(len(stats)), columns=cols)
            ss_list = [[Paragraph(c, self.styles['ColHeaderTxt']) for c in cols]] + stats_df.values.tolist()

            # Take the column widths for the main table and make each column worth half its total width
            col_widths = [(sum(c_widths)/2)] *2

            table = Table(ss_list, style=ts, colWidths=col_widths)
            return table


        def _header_footer(canvas, doc) -> None:
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            # Header
            header = Paragraph(self.header_text, self.styles['HeaderTxt'])
            w, h = header.wrap(doc.width, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - (h -self.header_margin))

            # Footer
            footer = Paragraph(f"{self.settings_dict['footer_text']}: {datetime.date.today()}", self.styles['Normal'])
            w, h = footer.wrap(doc.width, doc.bottomMargin)
            footer.drawOn(canvas, doc.leftMargin, h)

            # Release the canvas
            canvas.restoreState()

        # Add custom text styles
        self.styles.add(set_table_text_style('CellText'))
        self.styles.add(set_col_header_txt_style('ColHeaderTxt'))
        self.styles.add(set_header_custom_style("HeaderTxt"))
        self.styles.add(set_single_cell_tbl_style('SingleCellText'))

        # Create report elements
        elements = [add_report_table(self.column_widths), PageBreak(), add_summary_box(self.column_widths)]

        # Build the document from the elements we have and using the custom canvas with numbers
        self.pdf.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer, canvasmaker=NumberedCanvas)


    def __init__(self,in_dict, data_df, out_dir, pagesize='Letter', orientation='Portrait') -> None:
        self.logger = logging_setup()

        # Parameters sets from inputs
        self.in_dict = in_dict
        self.out_dir = out_dir
        self.data_df = data_df
        self.pagesize = pagesize
        self.orientation = orientation

        if pagesize == 'Letter':
            self.pagesize = letter

        # Import special e/f headings and title parameters based on location
        self.settings_dict = PDPSettings(self.in_dict['ed_code']).settings_dict

        # Setup other parameters
        self.width, self.height = self.pagesize
        self.font = self.settings_dict['font']
        self.report_name = self.settings_dict['report_name']
        self.header_margin = self.settings_dict['header_margin']
        self.column_widths = self.settings_dict['column_widths']
        self.page_margins = self.settings_dict['page_margins']

        self.styles = getSampleStyleSheet()

        # This is like this because we need to newline characters for the header to work properly
        self.header_text =  f"""<b>{self.settings_dict['header']['dept_nme']}</b><br/>
        {self.settings_dict['header']['report_type']}<br/>
        {self.settings_dict['header']['rep_order'].replace('YR', str(self.in_dict['rep_yr']))}<br/>
        {self.in_dict['prov']}<br/>
        <b>{self.in_dict['ed_name']}</b><br/>
        <b>{self.in_dict['ed_code']}</b> 
        """

        # Setup document
        # If things are overlapping the header / footer change the margins below
        self.pdf = SimpleDocTemplate(os.path.join(self.out_dir, f"{self.report_name}_{self.in_dict['ed_code']}.pdf"),
                            page_size=self.pagesize,
                            leftMargin=self.page_margins['leftMargin'],
                            rightMargin=self.page_margins['rightMargin'],
                            topMargin=self.page_margins['topMargin'],
                            bottomMargin=self.page_margins['bottomMargin']
        )

        # Creates the document for the report and exports
        self.pdp_report_pages()
