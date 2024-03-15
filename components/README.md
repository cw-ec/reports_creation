# Components

This folder and its subfolders contain all component files used in the tools for this repository. All files for the data
download and report generation tools can be found here.

## Report Generation Scripts

The report generation scripts make up the majority of the scripts in this folder. These scripts are responsible for 
ingesting the csv data, cleaning that data and then converting it into a format that can be read by the report generation
scripts. These scripts all follow the same basic structure.

## Other Scripts

### report_factory.py

Intake script containing the workflow processing logic for the report creation script.  

### data_downloader.py

Contains the bulk of the data download logic for the data download tool.

### commons.py

Contains common functions and objects that are used by more than one of the generator functions
