import json, sys, os
from collections import OrderedDict
from .commons import logging_setup, create_dir
from .apd_generator import APDGenerator
from .pdp_generator import PDPGenerator
from .pdd_generator import PDDGenerator
from .dpk_generator import DPKGenerator
from .mps_generator import MPSGenerator
from .idr_generator import IDRGenerator

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

        for k in self.order.keys():  # Process the data key by key

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

                    if k == 'PDP': # For Polling District Profiles
                        PDPGenerator(self.data_path, out_path, r)

                    if k == 'APD': # For Advance Polling Districts
                        APDGenerator(self.data_path, out_path, r)

                    if k == "PDD": # For Polling District Descriptions
                        PDDGenerator(self.data_path, out_path, r)

                    if k == "DPK": # For District Poll Key
                        DPKGenerator(self.data_path, out_path, r)

                    if k == "MPS": # For Mobile Polls Summary
                        MPSGenerator(self.data_path, out_path, r)

                    if k == "IDR": # For Indigenous Lands Report
                        IDRGenerator(self.data_path, out_path, r)

                    else:  # For those cases where the input key does not match any of the valid report types
                        self.logger.warning(f"{k} does not match a valid report type. Check the project documentation and edit your workflow")

    def __init__(self, workflow, data_path):

        self.logger = logging_setup()

        self.data_path = data_path
        self.out_dir = ".\\out"

        self.workflow = workflow # Path to json workflow

        self.logger.info("Extracting order from the input workflow")
        self.order = self.extract_order() # Get the order from the json as a dictionary
        self.process_order()

        self.logger.info("DONE!")
