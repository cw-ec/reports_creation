import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from commons import logging_setup
import sys, os
import PyPDF2
from .commons import logging_setup
class BuildReport:
    """Builds the report pdf with a header and footer"""

    def gen_table(self):
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis('tight')
        ax.axis('off')

        the_table = ax.table(cellText=self.in_data.values,
                             colLabels=self.in_data.columns,
                             loc='center',
        )

        self.pdf.savefig(fig, bbox_inches='tight')

    def add_header_footer(self):
        """Adds header, footer to the document"""


        with open(self.out_file) as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            pdf_writer = PyPDF2.PdfFileWriter()
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)

                header = PyPDF2.pdf.PageObject.createBlankPage(None, page.mediaBox.getWidth(), 30)
                header.mergeTranslatedPage(page, 0, 30)
                header.mergeTranslatedPage(PyPDF2.pdf.PageObject.createTextObject(None, self.header_text), 0, 5)
                pdf_writer.addPage(header)

    def __init__(self, in_dict, in_data, out_path):
        self.logger = logging_setup()
        self.in_data = in_data
        self.out_path = out_path

        # Set Values from the inputs dict
        self.dept_nme = in_dict['dept_nme']
        self.report_type = in_dict['report_type']
        self.rep_order = in_dict['rep_order']
        self.ed_namee = in_dict['ed_namee']
        self.ed_namef = in_dict['ed_namef']
        self.prov = in_dict['prov']
        self.logger.info("Building header text")
        self. header_text = f"""
                        {self.dept_nme}
                        {self.report_type}
                        {self.rep_order}
                        {self.rep_order}
                        {self.ed_namee}/{self.ed_namef}               
        """
        self.out_file = os.path.join(self.out_path, 'test_pdf.pdf')

        self.logger.info("Creating output PDF ")
        self.pdf = PdfPages(self.out_file)
        self.logger.info("Generating Table in report")
        self.gen_table()
        self.pdf.close()
        self.logger.info("Adding Header and Footer to Document")
        self.add_header_footer()


        # sys.exit()




