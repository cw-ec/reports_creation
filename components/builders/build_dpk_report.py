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
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .common_builds import *
from .report_parameters import DPKSettings

registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

class BuildDPKReport:

    def dpk_report_pages(self):
        """Sets up the pages for the pdd report"""

        def add_report_table(df, col_widths) -> Table:
            """Sets the table for normal PD tables (mobile polls, single building, and strm's excluded)"""

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            data_df = df.copy()

            # Replace the nan's in the columns as needed to make the report table prettier
            for c in ['FROM_CIV_NUM', 'TO_CIV_NUM']:
                data_df[c].fillna('----', inplace=True)  # Replace nan with '----' to make the report prettier
                data_df[c] = data_df[c].apply(lambda x: str(int(x) if isinstance(x, float) else x))
            for c in ['FROM_CROSS_FEAT', 'TO_CROSS_FEAT', 'ST_SIDE_DESC_BIL']:
                data_df[c].fillna('', inplace=True)  # Replace nan with '' for the features same reason as above
                data_df[c] = data_df[c].apply(lambda x: Paragraph(x, style=self.styles['CellText'])) # Add cell text with word wrap

            # Build place name text for row header
            name_txt_list = data_df['FULL_PLACE_NAME'].dropna()
            if len(name_txt_list) >= 1:
                name_txt_list = data_df['FULL_PLACE_NAME'].dropna().head(1).values.tolist()[0].split(',')
                place_name_text = Paragraph(f"<b>{name_txt_list[-1]}: {name_txt_list[0]}</b>", style=self.styles['SingleCellText'])

            else:  # Some full place names are blank prevent this error by returning an empty list
                place_name_text = Paragraph(f"", style=self.styles['CellText'])

            # Create row header
            row_header = [[data_df['STREET_NME_FULL'].head(1).values.tolist()[0], place_name_text]]

            # Change or drop fields for better report presentation
            data_df.drop(columns=['FULL_PLACE_NAME'], inplace=True)
            data_df['STREET_NME_FULL'] = ''

            element_list = row_header + data_df.values.tolist()
            tbl = Table(element_list, style=ts, repeatRows=1, colWidths=col_widths)

            return tbl


        def _header_footer(canvas, doc):
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            # Header
            header = Paragraph(self.header_text, self.styles['HeaderTxt'])
            hw, hh = header.wrap(self.page_width - 0.4 * inch, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin - 1 * inch, (3.0 * inch) + doc.topMargin - hh - (1.5*cm))
            table_head = [[Paragraph(f"<b>{x}</b>", style=self.styles['ColHeaderTxt']) for x in self.settings_dict['table_header']]]
            tbl = Table(table_head, style=ts, colWidths=self.col_widths)
            tbl.wrapOn(canvas, hw, hh)
            tbl.drawOn(canvas, (self.page_width/2) -(hw/2) +(doc.leftMargin/2) + (0.2*cm), hh + (11.3 * cm))

            # Footer
            footer = Paragraph(f"{self.settings_dict['footer_text']}: {datetime.date.today()}", self.styles['Normal'])
            w, h = footer.wrap(self.page_width, doc.bottomMargin)
            footer.drawOn(canvas, doc.leftMargin, h)

            # Release the canvas
            canvas.restoreState()

        # Add custom text styles
        self.styles.add(set_table_text_style('CellText'))
        self.styles.add(set_single_cell_tbl_style('SingleCellText'))
        self.styles.add(set_place_nme_tbl_style('PlaceNmeText'))
        self.styles.add(set_col_header_txt_style('ColHeaderTxt'))
        self.styles.add(set_header_custom_style("HeaderTxt"))

        # Create list of elements that will go into the report using the input list of PD's dataframes
        elements = []

        # For each street name build a table in the report
        for str_df in self.df_list:

            elements.append(add_report_table(str_df, self.col_widths))

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
        # Column widths
        self.col_widths = [150, 125, 125, 50, 50, 100, 50, 50]  # must = 700


        # Import special e/f headings and title parameters based on location
        self.settings_dict = DPKSettings(self.in_dict['ed_code']).settings_dict

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
        self.logger.info("Creating DPK document")
        self.pdf = SimpleDocTemplate(os.path.join(self.out_dir, f"INDCIR_{self.in_dict['ed_code']}.pdf"),
                                     leftMargin=2 * cm,
                                     rightMargin=-5 * cm,
                                     topMargin=14.5 * cm,
                                     bottomMargin=2.5 * cm,
                                     )

        self.logger.info("Creating document tables")
        # Creates the document for the report and exports
        self.dpk_report_pages()

