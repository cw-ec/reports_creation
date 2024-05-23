import json, sys, os, shutil, fnmatch
from pathlib import Path
from collections import OrderedDict
from .commons import logging_setup, create_dir, delete_dir , get_prov_from_code
from .apd_generator import APDGenerator
from .pdp_generator import PDPGenerator
from .pdd_generator import PDDGenerator
from .dpk_generator import DPKGenerator
from .mps_generator import MPSGenerator
from .idr_generator import IDRGenerator

class ReportFactory:
    """Class responsible for organizing the creation of reports from input json"""

    @staticmethod
    def is_valid(workflow) -> None:
        """Checks to see if inputs are valid"""

        if not isinstance(workflow, str) or not os.path.exists(workflow):
            raise Exception(f"Parameter workflow: Must be of stype string and must point to an existing valid workflow file")

    def extract_order(self) -> OrderedDict:
        """Extracts the requested reports from the input workflow"""

        oc = OrderedDict()

        with open(self.workflow, 'r') as j:
            content = json.load(j)

            for k in content.keys():
                oc[k] = content[k]

            return oc

    def process_order(self) -> None:
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

    def export_order(self):
        """Exports the order to the given export directory"""

        export_dir = self.order['export_directory']
        temp_dir = Path(self.out_dir)

        self.logger.info(f"Exporting reports to: {export_dir}")

        for f in [ t for t_ in [temp_dir.glob(f"**/*{t}") for t in ('.pdf', '.xlsx')] for t in t_]:  # Process excel and pdf files

            if not isinstance(f, str) and not isinstance(f, Path):
                self.logger.warning(f"{f} is not a valid type string or Path object and cannot be exported")
                continue  # Make sure only strings are processed

            f_name = os.path.split(f)[-1]
            self.logger.info(f"Exporting {f_name}")

            fed_num = f_name.split("_")[-1].split(".")[0]  # Extract the fed number from the file name
            prov_abv = get_prov_from_code(int(fed_num), type='abv')

            fed_dir = os.path.join(export_dir, prov_abv, fed_num)  # Build the fed dir from the component parts
            create_dir(fed_dir)  # Ensure that the directory exists

            # Because we're exporting to a shared drive use try except to catch files that are open and note in logs
            try:
                shutil.copy(f, os.path.join(fed_dir, f_name)) # Copy the file to the export subdirectory

            except PermissionError:
                self.logger.exception(f"Permission Error: {f_name} could not be overwritten in export directory. Please ensure the file isn't open and try again.")

    def __init__(self, workflow):

        self.logger = logging_setup()

        self.is_valid(workflow)

        self.out_dir = ".\\scratch"
        delete_dir(self.out_dir)  # If the out_directory (scratch) exists from a prior run delete it and its contents

        self.workflow = Path(workflow) # Path to json workflow

        self.logger.info("Extracting order from the input workflow")
        self.order = self.extract_order() # Get the order from the json as a dictionary
        self.process_order()

        create_dir(self.order['export_directory'])  # Check to make sure the export directory exists before exporting
        self.export_order()

        self.logger.info("DONE!")
