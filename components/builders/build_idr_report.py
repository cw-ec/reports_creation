# -*- coding: utf-8-*-
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
from .report_parameters import IDRSettings

registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

class BuildIDRReport:
    """Builds the report pdf with a header and footer"""

    def idr_report_pages(self):
        """Setups the template for the pdp report"""

        def add_report_table(c_widths: list) -> Table:
            """Sets the table"""
            ts = [
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]

            # Fix table text
            self.data_df['C_NAME'] = self.data_df['C_NAME'].apply(lambda x: Paragraph(x, style=self.styles['CellText']))

            # Build the table
            t_list = [[Paragraph(x, style=self.styles['ColHeaderTxt']) for x in self.settings_dict['table_header']]] + self.data_df.values.tolist()
            tbl = Table(t_list, style=ts, repeatRows=1, colWidths=c_widths)

            return tbl

        def _header_footer(canvas, doc):
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            # Header
            header = Paragraph(self.header_text, self.styles['HeaderTxt'])
            w, h = header.wrap(doc.width, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - (h - self.header_margin))

            # Footer
            footer = Paragraph(f"{self.settings_dict['footer_text']}: {datetime.date.today()}", self.styles['Normal'])
            w, h = footer.wrap(doc.width, doc.bottomMargin)
            footer.drawOn(canvas, doc.leftMargin, h)

            # Release the canvas
            canvas.restoreState()

        # Add custom text styles
        self.styles.add(set_table_text_style('CellText'))
        self.styles.add(set_single_cell_tbl_style('SingleCellText'))
        self.styles.add(set_place_nme_tbl_style('PlaceNmeText'))
        self.styles.add(set_col_header_txt_style('ColHeaderTxt'))
        self.styles.add(set_header_custom_style("HeaderTxt"))

        column_widths = [300, 110, 110]
        # Create report elements
        elements = [add_report_table(column_widths)]

        # Build the document from the elements we have and using the custom canvas with numbers
        self.pdf.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer, canvasmaker=NumberedCanvas)

    def __init__(self,in_dict, data_df, out_dir, pagesize='Letter', orientation='Portrait'):
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
        self.styles = getSampleStyleSheet()

        # Import special e/f headings and title parameters based on location
        self.settings_dict = IDRSettings(self.in_dict['ed_code']).settings_dict

        # This is like this because we need to newline characters for the header to work properly
        self.header_text =  f"""<b>{self.settings_dict['header']['dept_nme']}</b><br/>
        {self.settings_dict['header']['report_type']}<br/>
        {self.settings_dict['header']['rep_order']}<br/>
        {self.in_dict['prov']}<br/>
        <b>{self.in_dict['ed_name']}</b><br/>
        <b>{self.in_dict['ed_code']}</b> 
        """

        # Setup document
        # If things are overlapping the header / footer change the margins below
        self.pdf = SimpleDocTemplate(os.path.join(self.out_dir, f"INDIAN_{self.in_dict['ed_code']}.pdf"),
                            page_size=self.pagesize,
                            leftMargin=2.2 * cm,
                            rightMargin=2.2 * cm,
                            topMargin=5.0 * cm,
                            bottomMargin=2.5 * cm
        )
        self.header_margin =  2* cm  # Modifies the distance the top of the header is from the top of the page

        # Creates the document for the report and exports
        self.idr_report_pages()
