# -*- coding: latin-1 -*-
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import registerFont
import datetime
import pandas as pd
from components.commons import logging_setup
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .common_builds import *
from .report_parameters import PDDSettings

registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

class BuildPDDReport:

    def pdd_report_pages(self):
        """Sets up the pages for the pdd report"""
        def add_report_table(df) -> Table:
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
            ]

            data_df = df.copy()

            # Split because we have multiple different types of poll in this report, and they are handled differently
            if len(data_df) > 1: # For regular polls

                # COMMENTED OUT UNLESS WE WANT TO APPLY SPECIFIC SIZING TO THE OUTPUT TABLE
                # config the widths and heights of this specific table
                # colwidths_2 = [120] * len(self.settings_dict['table_header_range'])
                # rowheights_2 = [50] * len(self.settings_dict['table_header'])

                lista = [self.settings_dict['table_header_range']] + data_df.values.tolist()
                tbl = Table(lista, style=ts, repeatRows=1)

                return tbl

            else: # For single building polls

                # COMMENTED OUT UNLESS WE WANT TO APPLY SPECIFIC SIZING TO THE OUTPUT TABLE
                # config the widths and heights of this specific table
                # colwidths_2 = [120] * len(self.settings_dict['table_header_ind'])
                # rowheights_2 = [50] * len(self.settings_dict['table_header'])

                lista = [self.settings_dict['table_header_ind']] + data_df.values.tolist()
                tbl = Table(lista, style=ts, repeatRows=1)

                return tbl

        def _header_footer(canvas, doc):
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            # Header
            header = Paragraph(self.header_text.replace("\n", "<br/>"), self.styles['header'])
            w, h = header.wrap(doc.width, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

            # Footer
            footer = Paragraph(f"{self.settings_dict['footer_text']}: {datetime.date.today()}", self.styles['Normal'])
            w, h = footer.wrap(doc.width, doc.bottomMargin)
            footer.drawOn(canvas, doc.leftMargin, h)

            # Release the canvas
            canvas.restoreState()

            # Setup basic styles

        self.styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Header style changes
        header_style = ParagraphStyle('header',
                                      fontName=self.font,
                                      fontSize=12,
                                      parent=self.styles['Heading2'],
                                      alignment=1,
                                      spaceAfter=14)
        self.styles.add(header_style)

        # Create list of elements that will go into the report using the input list of PD's dataframes
        elements = []
        for pd in self.df_list:
            elements.append(add_report_table(pd))

    def __init__(self,in_dict, df_list, out_dir, pagesize='Letter', orientation='Landscape'):
        self.logger = logging_setup()

        # Parameters sets from inputs
        self.in_dict = in_dict
        self.out_dir = out_dir
        self.df_list = df_list
        self.pagesize = pagesize
        self.orientation = orientation

        # Setup other parameters
        if pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
        self.font = 'Arial'
        self.styles = getSampleStyleSheet()

        # Import special e/f headings and title parameters based on location
        self.settings_dict = PDDSettings(self.in_dict['ed_code']).settings_dict

        # This is like this because we need to newline characters for the header to work properly
        self.header_text = f"""{self.settings_dict['header']['dept_nme']}
        {self.settings_dict['header']['report_type']}
        {self.settings_dict['header']['rep_order']}
        {self.in_dict['prov']}
        {self.in_dict['ed_name']}
        {self.in_dict['ed_code']} 
        """

        # Setup document
        # If things are overlapping the header / footer change the margins below
        self.logger.info("Creating PDD document")
        self.pdf = SimpleDocTemplate(os.path.join(self.out_dir, f"PD_LOCATOR_{self.in_dict['ed_code']}.pdf"),
                                     page_size=self.pagesize,
                                     leftMargin=2.2 * cm,
                                     rightMargin=2.2 * cm,
                                     topMargin=7 * cm,
                                     bottomMargin=2.5 * cm
                                     )
        self.logger.info("Creating document tables")
        # Creates the document for the report and exports
        self.pdd_report_pages()
