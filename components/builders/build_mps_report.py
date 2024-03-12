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
from .report_parameters import MPSSettings

registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

class BuildMPSReport:
    """Builds the report pdf with a header and footer"""

    def pdp_report_pages(self):
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
            ]

            df = self.data_df.copy()
            df['PD_NO_CONCAT'] = df['PD_NO_CONCAT'].apply(lambda x: Paragraph(x, style=self.styles['CellText']))

            # Build the table
            t_list = [[Paragraph(x, style=self.styles['ColHeaderTxt']) for x in self.settings_dict['table_header']]] + df.values.tolist()
            tbl = Table(t_list, style=ts, repeatRows=1, colWidths=c_widths)

            return tbl

        def add_summary_box(c_widths:list) -> Table:
            """Adds the summary stats box at the bottom of the main table."""

            # Table Style Setup
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

            # Apply cell text style to text based fields
            for c in ['PD_NO_CONCAT']:
                self.data_df[c] = self.data_df[c].apply(
                    lambda x: Paragraph(x, style=self.styles['CellText']))

            # Calc Stats
            total_active_pd = len(self.data_df)
            total_electors = self.data_df['ELECTORS_LISTED'].sum()
            total_num_inst = int(self.data_df.loc[:, 'TOTAL_INST'].sum())

            # Setup Stats DF
            cols = [f"{self.settings_dict['ss_table_header']}", '']
            stats = [(Paragraph(self.settings_dict['ss_total_pd'], self.styles['SingleCellText']), total_active_pd),
                     (Paragraph(self.settings_dict['ss_total_inst'], self.styles['SingleCellText']), total_num_inst),
                     (Paragraph(self.settings_dict['ss_total_noe'], self.styles['SingleCellText']), total_electors)]

            # Convert the df to a table and export
            stats_df = pd.DataFrame(stats,index=range(len(stats)), columns=cols)
            ss_list = [stats_df.columns[:, ].values.astype(str).tolist()] + stats_df.values.tolist()

            # Take the column widths for the main table and make each column worth half its total width
            col_widths = [(sum(c_widths)/2)] *2

            table = Table(ss_list, style=ts, colWidths=col_widths)
            return table


        def _header_footer(canvas, doc):
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            # Header
            header = Paragraph(self.header_text, self.styles['HeaderTxt'])
            w, h = header.wrap(doc.width, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

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

        column_widths = [130, 130, 130,130]
        # Create report elements
        elements = [add_report_table(column_widths), Spacer(0 * cm, 2 * cm), add_summary_box(column_widths)]

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
        self.settings_dict = MPSSettings(self.in_dict['ed_code']).settings_dict

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
        self.logger.info("Creating MPS document")
        self.pdf = SimpleDocTemplate(os.path.join(self.out_dir, f"SUMINS_{self.in_dict['ed_code']}.pdf"),
                            page_size=self.pagesize,
                            leftMargin=2.2 * cm,
                            rightMargin=2.2 * cm,
                            topMargin=7 * cm,
                            bottomMargin=2.5 * cm
        )
        self.logger.info("Creating document tables")
        # Creates the document for the report and exports
        self.pdp_report_pages()