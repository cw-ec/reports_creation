from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import letter, landscape
import sys

registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

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
            self.setFont('Arial', 9)
            self.draw_page_number(num_pages)
            self.Canvas.showPage(self)
        self.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(200 * mm, 0 * mm + (0.2 * inch),
                             f"Page {self._pageNumber} / {page_count}")


class NumberedCanvasLandscape(canvas.Canvas):
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
            self.setFont('Arial', 9)
            self.Canvas.setPageSize(self, size=(11 * inch, 8.5 * inch))
            self.draw_page_number(num_pages)
            self.Canvas.showPage(self)
        self.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(250 * mm, 0 * mm + (0.2 * inch),
                             f"Page {self._pageNumber} / {page_count}")


def set_table_text_style(style_name='cell_text') -> ParagraphStyle:
    """Returns custom paragraph style for table cell text"""

    styles = getSampleStyleSheet()

    style = ParagraphStyle(name=style_name,
                           parent=styles['BodyText'],
                           alignment=TA_CENTER)
    return style
