from .commons import logging_setup
import sys, os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from functools import partial


class BuildReport:
    """Builds the report pdf with a header and footer"""

    def pdp_report_pages(self):
        """Setups the template for the pdp report"""

        def add_report_table() -> Table:
            ts = [('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                  ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                  ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                  ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
                  ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
                  ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black, 1, None, None, 4, 1),
                  ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                  ('FONT', (0, -1), (-1, -1), 'Times-Bold'),
                  ('BACKGROUND', (1, 1), (-2, -2), colors.lightgrey),
                  ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]

            lista = [self.data_df.columns[:, ].values.astype(str).tolist()] + self.data_df.values.tolist()
            table = Table(lista, style=ts)

            return table

        def header(canvas, doc, content):
            """Adds header to the document """
            canvas.saveState()
            w, h = content.wrap(doc.width, doc.topMargin)
            content.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
            canvas.restoreState()

        def footer(canvas, doc, content):
            """ Adds footer content to the document per page"""
            canvas.saveState()
            w, h = content.wrap(doc.width, doc.bottomMargin)
            content.drawOn(canvas, doc.leftMargin, h)
            canvas.restoreState()

        def h_and_f(canvas, doc, header_content, footer_content):
            header(canvas, doc, header_content)
            footer(canvas, doc, footer_content)

        def main_pages():
            """ Main page consists of header, table and footer with page counts"""

            styles = getSampleStyleSheet()

            frame = Frame(self.pdf.leftMargin, self.pdf.bottomMargin, self.pdf.width, self.pdf.height, id='normal')

            header_content = Paragraph(self.header_text)
            footer_content = Paragraph("Placeholder")

            template = PageTemplate(id='test', frames=frame, onPage=partial(h_and_f, header_content=header_content, footer_content=footer_content))
            self.pdf.addPageTemplates([template])

            elements = [add_report_table()]

            self.pdf.build(elements)

        main_pages()

        def last_page():
            """Last page consists of header table and footer as well as totals table"""



    def __init__(self, doctype, in_dict, data_df):
        self.logger = logging_setup()
        self.doctype = doctype
        self.in_dict = in_dict
        self.data_df = data_df

        self.header_text = f"""
{self.in_dict['dept_nme']}
{self.in_dict['report_type']}
{self.in_dict['rep_order']}
{self.in_dict['rep_order']}
{self.in_dict['ed_namee']}/{self.in_dict['ed_namef']} 
"""

        self.pdf = SimpleDocTemplate(f"test.pdf",
                            page_size=letter,
                            leftMargin=2.2 * cm,
                            rightMargin=2.2 * cm,
                            topMargin=1.5 * cm,
                            bottomMargin=2.5 * cm
        )

        self.pdp_report_pages()

