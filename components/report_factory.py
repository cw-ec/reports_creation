import json, sys, os
from pathlib import Path
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


    def process_order(self):
        """Processes the order after extraction"""

        for report in self.order['reports']:  # Process the data key by key

            # Set out directory and check it exists
            out_path = os.path.join(self.out_dir, report['type'])
            create_dir(out_path)

            # Sets data path from workflow
            data_path = report['data']

            # Handles all the reports
            self.logger.info(f"Producing {len(report['feds'])} {report['type']} reports")
            for r in report['feds']:
                self.logger.info(f"Producing {report['type']} Report for: {r}")

                if report['type'] == 'PDP': # For Polling District Profiles
                    PDPGenerator(data_path, out_path, r)

                elif report['type'] == 'APD': # For Advance Polling Districts
                    APDGenerator(data_path, out_path, r)

                elif report['type'] == "PDD": # For Polling District Descriptions
                    PDDGenerator(data_path, out_path, r)

                elif report['type'] == "DPK": # For District Poll Key
                    DPKGenerator(data_path, out_path, r)

                elif report['type'] == "MPS": # For Mobile Polls Summary
                    MPSGenerator(data_path, out_path, r)

                elif report['type'] == "IDR": # For Indigenous Lands Report
                    IDRGenerator(data_path, out_path, r)

                else:  # For those cases where the input key does not match any of the valid report types
                    self.logger.warning(f"{report['type']} does not match a valid report type. Check the project documentation for all valid report types")

    def __init__(self, workflow):

        self.logger = logging_setup()

        self.out_dir = ".\\out"
        self.workflow = Path(workflow) # Path to json workflow

        self.logger.info("Extracting order from the input workflow")
        self.order = self.extract_order() # Get the order from the json as a dictionary
        self.process_order()

        self.logger.info("DONE!")
