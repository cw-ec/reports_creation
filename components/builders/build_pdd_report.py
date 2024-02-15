# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import registerFont
import datetime
import pandas as pd
from components.commons import logging_setup
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Frame
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .common_builds import *
from .report_parameters import PDDSettings

registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

class BuildPDDReport:

    def pdd_report_pages(self):
        """Sets up the pages for the pdd report"""

        def create_table_title(pd_number:str, pd_nme:str, width:int):
            """Creates the table header which contains: polling div name, polling div number, etc"""

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            para = Paragraph(f"{self.settings_dict['table_title']}: {pd_number} <br/> ({pd_nme})")

            tbl = Table([[para]], style=ts, colWidths=[width])

            return tbl

        def add_report_table(df) -> Table:
            """Sets the table for normal PD tables (mobile polls, single building, and strm's excluded)"""

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            data_df = df.copy()

            # Replace the nan's in the columns as needed to make the report table prettier
            for c in ['FROM_CIV_NUM', 'TO_CIV_NUM']:
                data_df[c].fillna('----', inplace=True)  # Replace nan with '----' to make the report prettier
                data_df[c] = data_df[c].apply(lambda x: str(int(x) if isinstance(x, float) else x))
            for c in ['FROM_CROSS_FEAT', 'TO_CROSS_FEAT']:
                data_df[c].fillna('', inplace=True)  # Replace nan with '' for the features same reason as above

            # COMMENTED OUT UNLESS WE WANT TO APPLY SPECIFIC SIZING TO THE OUTPUT TABLE
            # config the widths and heights of this specific table
            # colwidths_2 = [120] * len(self.settings_dict['table_header_range'])
            # rowheights_2 = [50] * len(self.settings_dict['table_header'])

            element_list = [self.settings_dict['table_header_range']] + data_df.values.tolist()
            tbl = Table(element_list, style=ts, repeatRows=1)

            return tbl

        def add_strm_table(df) -> Table:
            """Add a table containing all strms in the df with the strm custom formatting"""

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

        def add_mp_table(df) -> Table:
            """Add a table for all mobile polls with the mobile poll custom formatting"""

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            data_df = df[['FROM_CROSS_FEAT', 'STREET_NME_FULL']].copy() # Copy the df so prevent warnings


            element_list = [[Paragraph(x, style=self.styles['BodyText']) for x in self.settings_dict['table_header_mp']] + data_df.values.tolist()]
            tbl = Table(element_list, style=ts, repeatRows=1, colWidths=mp_widths)

            return tbl

        def add_sbp_table(df) -> Table:
            """Add single building poll table with the single building poll custom formatting"""

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            data_df = df['STREET_NME_FULL'].copy() # Copy data

            element_list = data_df.values.tolist()
            tbl = Table(element_list, style=ts, repeatRows=1)

            return tbl

        def _header_footer(canvas, doc):
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            # Header
            header = Paragraph(self.header_text, self.styles['header'])
            w, h = header.wrap(self.page_width - 0.4 * inch, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin - 1 * inch, (3.0 * inch) + doc.topMargin - h)

            # Footer
            footer = Paragraph(f"{self.settings_dict['footer_text']}: {datetime.date.today()}", self.styles['Normal'])
            w, h = footer.wrap(self.page_width, doc.bottomMargin)
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
                                      alignment=TA_CENTER,
                                      spaceAfter=14)
        self.styles.add(header_style)

        # Create list of elements that will go into the report using the input list of PD's dataframes
        elements = []

        # Build each table based of its type and specifications
        for pd_df in self.df_list:

            # Get the header name and num then drop those columns
            pd_num = pd_df["PD_NO_CONCAT"].values.tolist()[0]
            pd_name = pd_df["POLL_NAME_FIXED"].values.tolist()[0]
            pd_df.drop(labels=["PD_NO_CONCAT", "POLL_NAME_FIXED"], inplace=True, axis=1)

            pd_pre = int(pd_num.split('-')[0])

            # Generate the table for the pd based on the dataframes contents
            if pd_pre <= 399: # for regular tables
                elements.append(add_report_table(pd_df))
                elements.append(Spacer(0 * cm, 2 * cm)) # Spacer is needed to create a gap between the tables

            if (pd_pre >= 400) and (pd_pre < 500): # for single building poll tables

                if len(pd_df) > 1: # Single building poll should be a single location
                    self.logger.error("Single Building Poll greater than 1 location")
                    sys.exit()

                elements.append(add_sbp_table(pd_df))
                elements.append(Spacer(0 * cm, 2 * cm)) # Spacer is needed to create a gap between the tables

            if pd_pre >= 500: # for mobile polls (MOB)

                mp_widths = [250, 250, 150]

                elements.append(create_table_title(pd_num, pd_name, width=sum(mp_widths)))
                elements.append(add_mp_table(pd_df))
                elements.append(Spacer(0 * cm, 2 * cm)) # Spacer is needed to create a gap between the tables

        #self.pdf.addPageTemplates([PageTemplate(id='landscape', pagesize=landscape(letter))])
        # Build the document from the elements we have and using the custom canvas with numbers
        self.pdf.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer,
                       canvasmaker=NumberedCanvasLandscape)

    def __init__(self,in_dict, df_list, out_dir):
        self.logger = logging_setup()

        # Parameters sets from inputs
        self.in_dict = in_dict
        self.out_dir = out_dir
        self.df_list = df_list

        # Setup other parameters
        self.font = 'Arial'
        self.styles = getSampleStyleSheet()
        self.page_height = 8.5 * inch
        self.page_width = 11 * inch

        # Import special e/f headings and title parameters based on location
        self.settings_dict = PDDSettings(self.in_dict['ed_code']).settings_dict

        # This is like this because we need to newline characters for the header to work properly
        self.header_text = f"""<b>{self.settings_dict['header']['dept_nme']}</b><br/>
        {self.settings_dict['header']['report_type']}<br/>
        {self.settings_dict['header']['rep_order']}<br/>
        {self.in_dict['prov']}<br/>
        <b>{self.in_dict['ed_name']}</b><br/>
        <b>{self.in_dict['ed_code']}</b><br/>
        """

        # Setup document
        # If things are overlapping the header / footer change the margins below
        self.logger.info("Creating PDD document")
        self.pdf = SimpleDocTemplate(os.path.join(self.out_dir, f"DESCRIPTIONS_{self.in_dict['ed_code']}.pdf"),
                                     leftMargin=2 * cm,
                                     rightMargin=-5 * cm,
                                     topMargin=13 * cm,
                                     bottomMargin=2.5 * cm,
                                     showBoundary=1
                                     )
        self.logger.info("Creating document tables")
        # Creates the document for the report and exports
        self.pdd_report_pages()
