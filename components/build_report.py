from commons import logging_setup
import bs4
import sys, os

class BuildReport:
    """Builds the report pdf with a header and footer"""

    def create_report(self):
        """Creates report from html template"""
        def add_tag_text(soup_data: bs4.BeautifulSoup, tag_type: str, tag_id: str, new_tag_text: str):
            """ Adds tag text to the template. Finds tag by looking for the id attribute"""
            old_tag = soup_data.find(tag_type, {"id": tag_id})
            new_tag = soup_data.new_tag("h1", attrs={"id": tag_id})
            new_tag.string = new_tag_text
            old_tag.replace_with(new_tag)

        with open(self.template_path) as temp:
            self.logger.info("Reading in report template")
            txt = temp.read()
            soup = bs4.BeautifulSoup(txt, "html.parser")

            self.logger.info("Adding Header Text")
            for k in self.header_dict.keys():
                self.logger.info(f"Populating: {k}")
                # Writes the report header text into the template. edNamee and edNamef left like this as place holder fix to check if they are the same or different later. add logic for that before release
                if k == "ed_namee":
                    add_tag_text(soup, tag_type='h1', tag_id='ed_name', new_tag_text=self.header_dict[k])
                    continue
                if k == "ed_namef":
                    continue
                else:
                    add_tag_text(soup, tag_type='h1', tag_id=k, new_tag_text=self.header_dict[k], )

            self.logger.info("Adding table(s) to html")



    def __init__(self, in_dict, in_data, out_path):
        self.logger = logging_setup()

        self.in_data = in_data
        self.out_path = out_path
        self.template_path = ".\\templates\\pdp_template.html"

        # Set Values from the inputs dict
        self.dept_nme = in_dict['dept_nme']
        self.report_type = in_dict['report_type']
        self.rep_order = in_dict['rep_order']
        self.ed_namee = in_dict['ed_namee']
        self.ed_namef = in_dict['ed_namef']
        self.prov = in_dict['prov']
        self.logger.info("Building header text")
        self. header_dict = {
                        "dept_name": self.dept_nme,
                        "report_type": self.report_type,
                        "rep_order": self.rep_order,
                        "ed_namee": self.ed_namee,
                        "ed_namef": self.ed_namef,
                        "prov": self.prov
                        }

        self.out_file = os.path.join(self.out_path, 'test_pdf.pdf')

        self.create_report()

        # sys.exit()




