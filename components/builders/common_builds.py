from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import letter, landscape
import sys

# Non-standard for in reportlab needs to be registered (both bold and non-bold versions
registerFont(TTFont('Arial','ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARLRDBD.TTF'))

# Custom objects and functions for use in the building of reports

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


# Additional custom text styles for specific pieces of various reports

def set_table_text_style(style_name='CellText') -> ParagraphStyle:
    """Returns custom paragraph style for table cell text"""

    styles = getSampleStyleSheet()

    style = ParagraphStyle(name=style_name,
                           parent=styles['BodyText'],
                           alignment=TA_CENTER)
    return style

def set_single_cell_tbl_style(style_name='SingleCellText') -> ParagraphStyle:
    """Returns the custom paragraph style for single building poll tables"""

    styles = getSampleStyleSheet()

    style = ParagraphStyle(name=style_name,
                           parent=styles['BodyText'],
                           alignment=TA_LEFT)
    return style

def set_place_nme_tbl_style(style_name='place_nme_text') -> ParagraphStyle:
    """Returns the paragraph style for place name text boxes (top right of table title)"""

    styles = getSampleStyleSheet()

    style = ParagraphStyle(name=style_name,
                           parent=styles['BodyText'],
                           alignment=TA_RIGHT)

    return style

def set_col_header_txt_style(style_name='ColHeaderTxt'):
    """Sets the custom style for the Column Names"""

    styles = getSampleStyleSheet()

    style = ParagraphStyle(name=style_name,
                           parent=styles['BodyText'],
                           alignment=TA_CENTER,
                           font= 'Arial-Bold')

    return style

def set_header_custom_style(style_name="HeaderTxt"):
    """Sets custom text style for the header"""

    styles = getSampleStyleSheet()

    style = ParagraphStyle(name=style_name,
                           parent=styles['BodyText'],
                           alignment=TA_CENTER,
                           font='Arial',
                           fontSize=14
                           )

    return style
