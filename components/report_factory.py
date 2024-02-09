import json, sys, os
from collections import OrderedDict
from .commons import logging_setup, create_dir
from .apd_generator import APDGenerator
from .pdp_generator import PDPGenerator

class ReportFactory:
    """Class responsible for organizing the creation of reports from input json"""

    def extract_order(self) -> OrderedDict:
        """Extracts the requested reports from the input workflow"""

        oc = OrderedDict()

        with open(self.workflow, 'r') as j:
            content = json.load(j)

            for k in content.keys():
                oc[k] = content[k]

            return oc

    def order_sums(self):
        """Creates sums table for the input order"""


    def process_order(self):
        """Processes the order after extraction"""

        for k in self.order.keys():

            # Sets data path from workflow
            if k == "NUMBERS_DATA":
                self.data_path = self.order[k]

            else:
                # Handles all the reports
                self.logger.info(f"Producing Reports: {k}")
                for r in self.order[k]:
                    self.logger.info(f"Producing {k} Report for: {r}")
                    out_path = os.path.join(self.out_dir, k)
                    create_dir(out_path)
                    if k == 'PDP':
                        PDPGenerator(self.data_path, out_path, r)

                    if k == 'APD':
                        APDGenerator(self.data_path, out_path, r)


    def __init__(self, workflow, data_path):

        self.logger = logging_setup()

        self.data_path = data_path
        self.out_dir = ".\\out"

        self.workflow = workflow # Path to json workflow

        self.logger.info("Extracting order from the input workflow")
        self.order = self.extract_order() # Get the order from the json as a dictionary
        self.process_order()

        self.logger.info("DONE!")
