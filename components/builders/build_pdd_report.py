# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import letter
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

        def add_report_table(df, col_widths) -> Table:
            """Sets the table for normal PD tables (mobile polls, single building, and strm's excluded)"""

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

            data_df = df.copy()

            # Build place name text for row header
            name_txt_list = data_df['FULL_PLACE_NAME'].dropna()
            if len(name_txt_list) >= 1:
                name_txt_list = data_df['FULL_PLACE_NAME'].dropna().head(1).values.tolist()[0].split(',')
                place_name_text = Paragraph(f"{name_txt_list[-1]}: {name_txt_list[0]}", style=self.styles['CellText'])

            else:  # Some full place names are blank prevent this error by returning an empty list
                place_name_text = Paragraph(f"", style=self.styles['CellText'])

            title_para = [Paragraph(f"<b>{self.settings_dict['table_title']}: {pd_num} <br/> ({pd_name})</b>"), '','','','', place_name_text]

            data_df.drop(columns=['FULL_PLACE_NAME'], inplace=True)

            # Replace the nan's in the columns as needed to make the report table prettier
            for c in ['FROM_CIV_NUM', 'TO_CIV_NUM']:
                data_df[c] = data_df[c].astype(str)
                data_df[c] = data_df[c].fillna('----')  # Replace nan with '----' to make the report prettier
                data_df[c] = data_df[c].apply(lambda x: str(int(x) if isinstance(x, float) else x))
            for c in ['FROM_CROSS_FEAT', 'TO_CROSS_FEAT']:
                data_df[c] = data_df[c].astype(str)
                data_df[c] = data_df[c].fillna('')  # Replace nan with '' for the features same reason as above
                data_df[c] = data_df[c].apply(lambda x: Paragraph(x, style=self.styles['CellText'])) # Add cell text with word wrap

            element_list = [title_para] + [ [Paragraph(f"<b>{x}</b>", style=self.styles['ColHeaderTxt']) for x in self.settings_dict['table_header_range']]] + data_df.values.tolist()
            tbl = Table(element_list, style=ts, repeatRows=2, colWidths=col_widths)

            return tbl

        def add_strm_table(df, col_widths) -> Table:
            """Add a table containing all strms in the df with the strm custom formatting"""

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            data_df = df

            element_list = [[Paragraph(f"<b>{x}</b>", style=self.styles['ColHeaderTxt']) for x in self.settings_dict['table_header_strm']]] + data_df.values.tolist()

            tbl = Table(element_list, style=ts, repeatRows=1, colWidths=col_widths)

            return tbl

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
                ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            title_para = [Paragraph(f"<b>{self.settings_dict['table_title']}: {pd_num} <br/> ({pd_name})</b>"), '', '']
            data_df = df[['FROM_CROSS_FEAT', 'STREET_NME_FULL']].copy()  # Copy the df so prevent warnings

            # Load and filter the ps add dataframe and create the full address field with the correct paragraph style
            ps_add = self.ps_add[self.ps_add['FULL_PD_NBR'] == pd_num]
            ps_add['mp_add_full'] = self.ps_add[['FINAL_SITE_ADDRESS', 'SITE_PLACE_NAME', 'CPC_PRVNC_NAME', 'SITE_PSTL_CDE']].apply(lambda x: Paragraph(f"{x.iloc[0]}<br/> {x.iloc[1]} {x.iloc[2]} {x.iloc[3]}", style=self.styles['SingleCellText']),axis=1)

            element_list = [title_para] + [[Paragraph(f"<b>{x}</b>", style=self.styles['ColHeaderTxt']) for x in self.settings_dict['table_header_mp']]] + ps_add[["SITE_NAME_BIL", 'mp_add_full', 'ELECTORS_LISTED']].values.tolist()
            tbl = Table(element_list, style=ts, repeatRows=2, colWidths=mp_widths)

            return tbl

        def add_sbp_table(df, col_widths) -> Table:
            """Add single building poll table with the single building poll custom formatting"""

            ts = [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('FONT', (0, 0), (-1, 0), f'{self.font}-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), # Top row background
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey), # Bottom row background
                ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            # Set the place name box text. Leave blank if no placename is listed
            place_nme_list = self.ps_add[self.ps_add['FULL_PD_NBR'] == pd_num]['FULL_SBPD_PLACE']
            if len(place_nme_list) >= 1:
                place_nme_list = place_nme_list.values.tolist()[0].split(',')
                place_nme = Paragraph(f"{place_nme_list[-1]}: {place_nme_list[1]}", style=self.styles['PlaceNmeText'])

            else:  # for cases where there is no placename set the place_nme to nothing
                place_nme =  Paragraph(f"", style=self.styles['PlaceNmeText'])

            title_para = [Paragraph(f"<b>{self.settings_dict['table_title']}: {pd_num}</b> <br/> <b>({pd_name})</b>"),
                          place_nme]
            footer_para = [Paragraph(f"<b>{self.settings_dict['table_note']}</b>", style=self.styles['SingleCellText'])]

            # Text for the main cell of the table
            site_add = Paragraph(f"{df['FROM_CROSS_FEAT'].values.tolist()[0]}<br/>{int(df['FROM_CIV_NUM'].values.tolist()[0])} {df['STREET_NME_FULL'].values.tolist()[0]} / {int(df['FROM_CIV_NUM'].values.tolist()[0])} {df['STREET_NME_FULL'].values.tolist()[0]}", style=self.styles['SingleCellText'])

            element_list = [title_para] + [[site_add]] + [footer_para]
            tbl = Table(element_list, style=ts, repeatRows=1, colWidths=col_widths)

            return tbl

        def _header_footer(canvas, doc):
            # Save the state of our canvas, so we can draw on it
            canvas.saveState()

            # Header
            header = Paragraph(self.header_text, self.styles['HeaderTxt'])
            w, h = header.wrap(self.page_width - 0.4 * inch, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin - 0.5 * inch, (3.0 * inch) + doc.topMargin - h)

            # Footer
            footer = Paragraph(f"{self.settings_dict['footer_text']}: {datetime.date.today()}", self.styles['Normal'])
            w, h = footer.wrap(self.page_width, doc.bottomMargin)
            footer.drawOn(canvas, doc.leftMargin, h)

            # Release the canvas
            canvas.restoreState()

            # Setup basic styles

        self.styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Add custom text styles
        self.styles.add(set_table_text_style('CellText'))
        self.styles.add(set_single_cell_tbl_style('SingleCellText'))
        self.styles.add(set_place_nme_tbl_style('PlaceNmeText'))
        self.styles.add(set_col_header_txt_style('ColHeaderTxt'))
        self.styles.add(set_header_custom_style("HeaderTxt"))

        # Create list of elements that will go into the report using the input list of PD's dataframes
        elements = []

        # Build each table based of its type and specifications
        for pd_df in self.df_list:

            # If TRM Table it will not have a pd id and should be run before that code
            if "TWNSHIP" in pd_df.columns.tolist(): # For TRM Tables should have TWNSHIP as a field

                trm_widths = [150, 150, 150, 100, 150] # Sums to 700

                elements.append(add_strm_table(pd_df, trm_widths))
                elements.append(Spacer(0 * cm, 2 * cm))
                continue

            # If not a trm then process normally
            # Get the header name and num then drop those columns
            pd_num = pd_df["PD_NO_CONCAT"].values.tolist()[0]
            pd_name = pd_df["POLL_NAME_FIXED"].values.tolist()[0]
            pd_df.drop(labels=["PD_NO_CONCAT", "POLL_NAME_FIXED"], inplace=True, axis=1)

            pd_pre = int(pd_num.split('-')[0])

            # Generate the table for the pd based on the dataframes contents
            if pd_pre <= 399: # for regular tables

                reg_widths = [220, 120, 120, 50, 50, 140] # Sums to 700

                elements.append(add_report_table(pd_df, reg_widths))
                elements.append(Spacer(0 * cm, 2 * cm)) # Spacer is needed to create a gap between the tables

            elif (pd_pre >= 400) and (pd_pre < 500): # for single building poll tables

                if len(pd_df) > 1: # Single building poll should be a single location
                    self.logger.error("Single Building Poll greater than 1 location")
                    sys.exit()

                sbp_widths = [500, 200]  # Sums to 700

                elements.append(add_sbp_table(pd_df, sbp_widths))
                elements.append(Spacer(0 * cm, 2 * cm)) # Spacer is needed to create a gap between the tables

            elif pd_pre >= 500: # for mobile polls (MOB)

                mp_widths = [250, 250, 200] # Sums to 700

                elements.append(add_mp_table(pd_df))
                elements.append(Spacer(0 * cm, 2 * cm)) # Spacer is needed to create a gap between the tables

        # Build the document from the elements we have and using the custom canvas with numbers
        self.pdf.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer,
                       canvasmaker=NumberedCanvasLandscape)

    def __init__(self,in_dict, df_list, ps_add_df, out_dir):
        self.logger = logging_setup()

        # Parameters sets from inputs
        self.in_dict = in_dict  # Dictionary of text for important page elements
        self.out_dir = out_dir  # The directory where the pdf will be placed
        self.df_list = df_list  # List of the dataframes to be put in the document
        self.ps_add = ps_add_df  # Dataframe containing the complete address information for sbp and mobile polls

        # Setup other parameters for the page and element styles
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
                                     )

        self.logger.info("Creating document tables")
        # Creates the document for the report and exports
        self.pdd_report_pages()
