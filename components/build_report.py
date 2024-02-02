import datetime

from .commons import logging_setup
from io import BytesIO
import sys, os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Frame, PageTemplate, PageBreak, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from functools import partial
registerFont(TTFont('Times','TIMES.ttf'))

class NumberedCanvas(canvas.Canvas):
    """ Adds page numbers to the canvas.
    Numbered Canvas from: https://gist.github.com/nenodias/8c54500eb27884935d05b3ed3b0dd793
    """
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.Canvas = canvas.Canvas
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.setFont('Times', 8)
            self.draw_page_number(num_pages)
            self.Canvas.showPage(self)
        self.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(200 * mm, 5 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))


class BuildReport:
    """Builds the report pdf with a header and footer"""

    def pdp_report_pages(self):
        """Setups the template for the pdp report"""

        def add_report_table() -> Table:
            """Sets the table"""
            ts = [
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
                ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]

            lista = [self.data_df.columns[:, ].values.astype(str).tolist()] + self.data_df.values.tolist()
            table = Table(lista, style=ts)

            return table

        def _header_footer(canvas, doc):
            # Save the state of our canvas so we can draw on it
            canvas.saveState()
            styles = getSampleStyleSheet()

            # Header
            header = Paragraph(self.header_text, styles['Normal'])
            w, h = header.wrap(doc.width, doc.topMargin)
            header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

            # Footer
            footer = Paragraph(f"Printed on / Imprimé le: {datetime.date.today()}", styles['Normal'])
            w, h = footer.wrap(doc.width, doc.bottomMargin)
            footer.drawOn(canvas, doc.leftMargin, h)

            # Release the canvas
            canvas.restoreState()

        def main_pages():
            """ Main page consists of header, table and footer with page counts"""

            elements = []
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

            #header_content = Paragraph(self.header_text)
            #footer_content = Paragraph(f"Printed on / Imprimé le: {datetime.date.today()}")

            #template = PageTemplate(id='test', frames=frame, onPage=partial(_header_footer, header_content=header_content, footer_content=footer_content))
            #self.pdf.addPageTemplates([template])

            elements = [add_report_table()]

            self.pdf.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer,  canvasmaker=NumberedCanvas)
            #self.pdf.append(PageBreak())

        main_pages()

        def last_page():
            """Last page consists of header table and footer as well as totals table"""



    def __init__(self, doctype, in_dict, data_df, buffer=BytesIO(), pagesize='Letter', orientation='Portrait'):
        self.logger = logging_setup()
        self.doctype = doctype
        self.in_dict = in_dict
        self.data_df = data_df
        self.buffer = buffer
        self.pagesize = pagesize
        self.orientation = orientation

        if pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

        self.header_text = f"""
{self.in_dict['dept_nme']}
{self.in_dict['report_type']}
{self.in_dict['rep_order']}
{self.in_dict['rep_order']}
{self.in_dict['ed_namee']}/{self.in_dict['ed_namef']} 
"""

        self.pdf = SimpleDocTemplate(f"test.pdf",
                            page_size=self.pagesize,
                            leftMargin=2.2 * cm,
                            rightMargin=2.2 * cm,
                            topMargin=4 * cm,
                            bottomMargin=2.5 * cm
        )

        self.pdp_report_pages()

