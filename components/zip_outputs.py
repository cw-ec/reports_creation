import json
import os, sys
from collections import OrderedDict
from pathlib import Path
from shutil import copyfile, copytree, make_archive, rmtree

from .commons import logging_setup, create_dir, delete_dir

class ZipOutputs:

    def extract_params(self) -> OrderedDict:
        """Extracts the requested reports from the input workflow"""

        oc = OrderedDict()

        with open(self.workflow, 'r') as j:
            content = json.load(j)

            for k in content.keys():
                oc[k] = content[k]

            return oc

    def sort_dirs(self):
        """Combines all files from the map and report directories and puts them into a single zip file. This is exported
        to the out directory"""

        def sort_maps():
            """Code for sorting the maps before zipping. Taken from the cw-ec/map_series"""

            for file in map_dir.glob("*.pdf"):

                ptype = file.name.split('_')[0]
                fed = file.name.split('_')[1].split('.')[0]

                if ptype == 'InsetIndex':  # no suffix on inset reports use simplified workflow

                    fed = fed.split('.')[0]  # needed because fed has the file type in it and it's not needed
                    out_pdf_path = os.path.join(self.scratch_dir, fed)

                    Path(out_pdf_path).mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Sorting: {file.name}")
                    copyfile(os.path.join(map_dir, file.name), os.path.join(out_pdf_path, 'maps', f"{ptype}_{fed}.pdf"))

                else:  # Map PDFs have more components and need a more complex workflow
                    suffix = file.name.split('_')[2].split('.')[0]

                    # Add a 0 for sorting purposes if the suffix of the file name looks like this: 'A1' -> 'A01'
                    if (suffix.split('.')[0][0].isalpha()) and (len(suffix) == 2):
                        suffix = f"{suffix[0]}0{suffix[1]}"

                    out_pdf_path = os.path.join(self.scratch_dir, fed, 'maps', self.poll_type[ptype])
                    # Make sure output path exists. Create if needed
                    Path(out_pdf_path).mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Sorting: {file.name}")
                    copyfile(os.path.join(map_dir, file.name),
                             os.path.join(out_pdf_path, f"{ptype}_{fed}_{suffix}.pdf"))

        def sort_reports():
            """Sort the reports in the reports before zipping"""

            # Get all FED subdirectories from the reports_folder
            for fed_dir in report_dir.glob('*/*/'):
                self.logger.info(f"Moving all reports in {fed_dir}")

                report_path = os.path.join(self.scratch_dir, os.path.split(fed_dir)[-1], 'reports')

                if os.path.exists(report_path):
                    delete_dir(report_path)

                copytree(fed_dir, os.path.join(self.scratch_dir, os.path.split(fed_dir)[-1], 'reports'), )

        map_dir = Path(self.params['map_dir'])
        report_dir = Path(self.params['report_dir'])

        # Start Sorting: Maps first
        self.logger.info(f"Sorting Maps in: {map_dir}")
        sort_maps()

        self.logger.info(f"Sorting Reports in: {report_dir}")
        sort_reports()

    def export_files(self):
        """Zips and exports the sorted files from the scratch directory to the output directory"""

        # Get every dir in scratch and make a zip
        for d in self.scratch_dir.glob('*/'):
            if os.path.exists(d):
                fed = os.path.split(d)[-1]
                self.logger.info(f"Zipping: {fed}")
                # base_name = dir to place zip  root_dir= directory to convert into archive (zip)
                make_archive(base_name=os.path.join(self.out_dir,fed), format='zip', root_dir=d)
                if os.path.exists(d):
                    rmtree(d)
            else:
                self.logger.warn(f"{d} does not exist. No zip created")


    def __init__(self, workflow:str):
        """Combines and creates zip directories of the input map and report directories"""

        self.logger = logging_setup()

        # Validate workflow
        if (not isinstance(workflow, str)) or (not os.path.exists(workflow)):
            self.logger.exception("Parameter workflow: Must be a valid path and must exist")
            raise Exception("Parameter workflow: Must be a valid path and must exist")

        # Set Params
        self.workflow = Path(workflow)
        self.scratch_dir = Path(".\\scratch\\zipping")
        self.poll_type = {'A': 'ADV',
                          'P': 'PollDay'}

        # Create scratch directory if necessary
        create_dir(str(self.scratch_dir))

        # Extract parameters from the workflow.json
        self.params = self.extract_params()
        self.out_dir = self.params['out_dir']

        # Use params to create combined file structure
        self.sort_dirs()

        # Zip and export each file from the scratch directory to the out directory
        self.logger.info(f"Exporting sorted files to {self.out_dir}")
        self.export_files()

        self.logger.info("Deleting scratch directory")
        delete_dir(str(self.scratch_dir))

        self.logger.info("Process Complete!")
