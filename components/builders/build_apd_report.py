# -*- coding: utf-8 -*-
import datetime
import sys

import pandas as pd
from components.commons import logging_setup
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
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
class BuildAPDReport:
    """Builds the report pdf using the input data"""

    def apd_report_pages(self):
        """Setups the template for the pdp report"""

        def add_report_table() -> Table:
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
            ]

            # Convert the strings in the PD_LIST field into Paragraph objects to allow us to apply styling (esp word wrap)
            self.data_df['PD_LIST'] = self.data_df['PD_LIST'].apply(lambda x: Paragraph(x, style=self.styles['CellText']))

            # Convert certain types of text to body text to ensure no cell overruns with longer strings
            self.data_df["ADV_POLL_NAME_FIXED"] = self.data_df["ADV_POLL_NAME_FIXED"].apply(
                lambda x: Paragraph(x, style=self.styles['CellText']))

            data_list = []
            for h in self.settings_dict['table_header']:
                data_list.append(Paragraph(h,style=self.styles['BodyText']))

            # Prep data for table conversion
            data_summary = [data_list] + self.data_df.values.tolist()

            # config the widths and heights of this specific table
            colwidths_custom = [50, 180, 220, 70]

            tbl = Table(data_summary, style=ts, repeatRows=1, colWidths=colwidths_custom) #rowHeights=rowheights_2)

            return tbl

        def add_summary_box() -> Table:
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
            ]

            # Calculate Summary Statistics
            total_apd = len(self.data_df)

            # Setup Stats DF
            cols = [f"{self.settings_dict['ss_table_header']}", '']
            stats = [(Paragraph(self.settings_dict['ss_total_apd'], self.styles['CellText']),
                      total_apd),
                     ]

            # Convert the df to a table and export
            stats_df = pd.DataFrame(stats,index=range(len(stats)), columns=cols)
            listb = [stats_df.columns[:, ].values.astype(str).tolist()] + stats_df.values.tolist()

            table = Table(listb, style=ts, colWidths=[245,245])
            return table


        def _header_footer(canvas, doc):
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            # Header
            header = Paragraph(self.header_text.replace("\n", "<br/>"), self.styles['header'])
            w, h = header.wrap(doc.width, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

            # Footer
            footer = Paragraph(f"{self.settings_dict['footer_text']}: {datetime.date.today()}", self.styles['Normal'], encoding=self.encoding)
            w, h = footer.wrap(doc.width, doc.bottomMargin)
            footer.drawOn(canvas, doc.leftMargin, h)

            # Release the canvas
            canvas.restoreState()

        # Setup basic styles
        self.styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Header style changes
        header_style = ParagraphStyle('header',
                                      fontName=f"{self.font}",
                                      fontSize=12,
                                      parent=self.styles['Heading2'],
                                      alignment=1,
                                      spaceAfter=14)
        self.styles.add(header_style)

        # Add cell text style
        self.styles.add(set_table_text_style('CellText'))

        # Create report elements
        # elements = [add_summary_box()]
        elements = [add_report_table(), Spacer(0 * cm, 2 * cm), add_summary_box()]

        # Build the document from the elements we have
        self.pdf.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer, canvasmaker=NumberedCanvas)

    def __init__(self, in_dict, data_df, out_dir, pagesize='Letter', orientation='Portrait'):
        self.logger = logging_setup()

        # Parameters sets from inputs
        self.in_dict = in_dict
        self.out_dir = out_dir
        self.data_df = data_df
        self.pagesize = pagesize
        self.orientation = orientation

        # Setup other parameters
        if pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize
        self.font = 'Arial'
        self.encoding = 'LATIN-1'
        self.styles = getSampleStyleSheet()

        # Import e/f text objects based on report location
        self.settings_dict = APDSettings(self.in_dict['ed_code']).settings_dict

        # This is like this because we need to newline characters for the header to work properly
        self.header_text = f"""<b>{self.settings_dict['header']['dept_nme']}</b>
{self.settings_dict['header']['report_type']}
{self.settings_dict['header']['rep_order']}
{self.in_dict['prov']}
<b>{self.in_dict['ed_name']}</b>
<b>{self.in_dict['ed_code']}</b> 
"""
        # Setup document
        # If things are overlapping the header / footer change the margins below
        self.logger.info("Creating APD document")
        self.pdf = SimpleDocTemplate(os.path.join(self.out_dir, f"ADVANC_{self.in_dict['ed_code']}.pdf"),
                            page_size=self.pagesize,
                            leftMargin=2.2 * cm,
                            rightMargin=2.2 * cm,
                            topMargin=7 * cm,
                            bottomMargin=2.5 * cm
        )
        self.logger.info("Creating document tables")
        # Creates the document for the report and exports
        self.apd_report_pages()
