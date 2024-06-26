# -*- coding: utf-8 -*-
import datetime
import sys

import pandas as pd
from components.commons import logging_setup
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, PageBreak
from reportlab.platypus.flowables import TopPadder
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .report_parameters import APDSettings
from .common_builds import *

registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

"""
Builder class for the APD Report
"""
class BuildAPDReport:
    """Builds the report pdf using the input data"""

    def apd_report_pages(self) -> None:
        """Setups the template for the pdp report"""

        def add_report_table(col_widths: list) -> Table:
            """Sets the table"""

            # Defines the table style
            ts = [
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f"{self.font}-Bold"),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]

            df = self.data_df.copy()
            df['ADV_PD_NBR'] = df['ADV_PD_NBR'].apply(lambda x: Paragraph(str(x), style=self.styles['CellText']))

            # Convert the strings in the PD_LIST field into Paragraph objects to allow us to apply styling (esp word wrap)
            df['PD_LIST'] = df['PD_LIST'].apply(lambda x: Paragraph(x, style=self.styles['CellText']))

            # Convert certain types of text to body text to ensure no cell overruns with longer strings
            df["ADV_POLL_NAME_FIXED"] = df["ADV_POLL_NAME_FIXED"].apply(
                lambda x: Paragraph(x, style=self.styles['CellText']))

            # Prep data for table conversion
            data_summary = [[Paragraph(f"<b>{x}</b>", style=self.styles['ColHeaderTxt']) for x in self.settings_dict['table_header']]]  + df.values.tolist()

            # config the widths of this specific table
            colwidths_custom = col_widths
            # col heights are calculated dynamically because the data can have varying lengths. Word wrap means that this translates to varying heights.

            tbl = Table(data_summary, style=ts, repeatRows=1, colWidths=colwidths_custom)

            return tbl

        def add_summary_box(col_widths: list) -> Table:
            """Adds the summary stats box at the bottom of the main table.
            For a PDP this consists of: Total de sections de votes actives / Total of Active Polling Divisions,Nombre moyen d'électeurs par section de vote ordinaire /
            Average Number of Electors per Ordinary Polling Division"""

            # Table Style Setup
            ts = [
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f"{self.font}-Bold"),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]

            # Calculate Summary Statistics
            total_apd = len(self.data_df)

            # Setup Stats DF
            cols = [f"{self.settings_dict['ss_table_header']}", '']
            stats = [(Paragraph(self.settings_dict['ss_total_apd'], self.styles['SingleCellText']),
                      total_apd),
                     ]

            # Convert the df to a table and export
            stats_df = pd.DataFrame(stats,index=range(len(stats)), columns=cols)
            listb = [[Paragraph(c, self.styles['ColHeaderTxt']) for c in cols]] + stats_df.values.tolist()

            c_widths = [(sum(col_widths) / 2)] * 2 # Make sure the summary stats table is same width as main table
            table = Table(listb, style=ts, colWidths=c_widths)
            return table


        def _header_footer(canvas, doc) -> None:
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            # Header
            header = Paragraph(self.header_text.replace("\n", "<br/>"), self.styles['HeaderTxt'])
            w, h = header.wrap(doc.width, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - (h -self.header_margin))

            # Footer
            footer = Paragraph(f"{self.settings_dict['footer_text']}: {datetime.date.today()}", self.styles['Normal'], encoding=self.encoding)
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
        elements = [add_report_table(col_widths=self.column_widths), PageBreak(), add_summary_box(col_widths=self.column_widths)]

        # Build the document from the elements we have
        self.pdf.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer, canvasmaker=NumberedCanvas)

    def __init__(self, in_dict, data_df, out_dir, pagesize='Letter', orientation='Portrait') -> None:
        self.logger = logging_setup()

        # Parameters sets from inputs
        self.in_dict = in_dict
        self.out_dir = out_dir
        self.data_df = data_df
        self.pagesize = pagesize
        self.orientation = orientation

        if pagesize == 'Letter':
            self.pagesize = letter

        # Import e/f text objects based on report location
        self.settings_dict = APDSettings(self.in_dict['ed_code']).settings_dict

        # Setup other parameters
        self.font =  self.settings_dict['font']
        self.encoding = self.settings_dict['encoding']
        self.report_name = self.settings_dict['report_name']
        self.header_margin = self.settings_dict['header_margin']  # Modifies the distance the top of the header is from the top of the page
        self.column_widths = self.settings_dict["column_widths"]
        self.page_margins = self.settings_dict["page_margins"]

        self.styles = getSampleStyleSheet()
        self.width, self.height = self.pagesize

        # This is like this because we need to newline characters for the header to work properly
        self.header_text = f"""<b>{self.settings_dict['header']['dept_nme']}</b>
{self.settings_dict['header']['report_type']}
{self.settings_dict['header']['rep_order'].replace('YR', str(self.in_dict['rep_yr']))}
{self.in_dict['prov']}
<b>{self.in_dict['ed_name']}</b>
<b>{self.in_dict['ed_code']}</b> 
"""
        # Setup document
        # If things are overlapping the header / footer change the margins below
        self.logger.info("Creating APD document")
        self.pdf = SimpleDocTemplate(os.path.join(self.out_dir, f"{self.report_name}_{self.in_dict['ed_code']}.pdf"),
                                     page_size=self.pagesize,
                                     leftMargin=self.page_margins['leftMargin'],
                                     rightMargin=self.page_margins['rightMargin'],
                                     topMargin=self.page_margins['topMargin'],
                                     bottomMargin=self.page_margins['bottomMargin']
        )

        # Creates the document for the report and exports
        self.apd_report_pages()
