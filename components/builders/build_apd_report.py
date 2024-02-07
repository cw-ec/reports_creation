import datetime
import pandas as pd
from components.commons import logging_setup
from io import BytesIO
import sys, os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .common_builds import NumberedCanvas

registerFont(TTFont('Times','TIMES.ttf'))

class BuildAPDReport:
    """Builds the report pdf with a header and footer"""

    def apd_report_pages(self):
        """Setups the template for the pdp report"""

        def add_report_table() -> Table:
            """Sets the table"""
            ts = [
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            self.data_df['PD_LIST'] = self.data_df['PD_LIST'].apply(lambda x: Paragraph(x, style=self.styles['BodyText']))

            # Prep data for table conversion
            data_summary = [["NO. / Nº", "NAME / NOM", "POLLING DIVISIONS / SECTIONS DE VOTE", "TOTAL / TOTAL"]] + self.data_df.values.tolist()

            # config the widths and heights of this specific table
            # colwidths_2 = [175] * len(data_summary)
            # rowheights_2 = [20] * len(data_summary)

            tbl = Table(data_summary, style=ts, repeatRows=1,)# colWidths=colwidths_2, rowHeights=rowheights_2)

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
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
            ]

            # Calc Stats
            total_apd = len(self.data_df)

            # Setup Stats DF
            cols = ['Statistics', '']
            stats = [(Paragraph('Total number of advanced polling districts /Nombre total de districts de vote par anticipation', self.styles['BodyText']),
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
            footer = Paragraph(f"Printed on / Imprimé le: {datetime.date.today()}", self.styles['Normal'])
            w, h = footer.wrap(doc.width, doc.bottomMargin)
            footer.drawOn(canvas, doc.leftMargin, h)

            # Release the canvas
            canvas.restoreState()

        # Setup basic styles

        self.styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        # Header style changes

        header_style = ParagraphStyle('header',
                                      fontName="Helvetica",
                                      fontSize=12,
                                      parent=self.styles['Heading2'],
                                      alignment=1,
                                      spaceAfter=14)
        self.styles.add(header_style)

        # Create report elements
        # elements = [add_summary_box()]
        elements = [add_report_table(), Spacer(0 * cm, 2 * cm), add_summary_box()]

        # Build the document from the elements we have
        self.pdf.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer,  canvasmaker=NumberedCanvas)

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
        self.font = 'Helvetica'
        self.styles = getSampleStyleSheet()

        # This is like this because we need to newline characters for the header to work properly
        self.header_text = f"""{self.in_dict['dept_nme']}
{self.in_dict['report_type']}
{self.in_dict['rep_order']}
{self.in_dict['prov']}
{self.in_dict['ed_name']}
{self.in_dict['ed_code']} 
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
