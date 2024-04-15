# Components

This folder and its subfolders contain all component files used in the tools for this repository. All files for the data
download and report generation tools can be found here. The general structure of the report generation process can be 
visualized as follows:

<img height="551" src="C:\reports_creation\docs\img\rc_process.png" width="206"/>

## Report Generation Scripts

The report generation scripts make up the majority of the scripts in this folder. These scripts are responsible for 
ingesting the csv data, cleaning that data and then converting it into a format that can be read by the report generation
scripts. These scripts all follow the same basic structure for each given report. A general description of each can be found 
below.

### Report Generators

Each report has an associated generator script responsible for organizing and prepping the report data and other associated
elements. The generator script ensures that there is data present for the given Fed number and generates the Excel file (if necessary).
Once done it then sends all relevant inputs to a builder script that is responsible for building the report PDF.

A report generator script follows the following naming convention "<report abbreviation>_generator.py" for example the
file name for the PDD report generator would be PDD_generator.py. The input parameters for each generator are standardized
and can be described as follows:

| Parameter | Description                                                                                                                                                                                             |
|:---------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   data    | The path to the primary dataset used to create the report. Ensure that the data is formatted as csv or an xlsx. Outputs from this repositories data download tool will always be in the correct format. |
| out_path  | The directory the output report will be saved to.                                                                                                                                                       |
|  ed_num   | The Fed number to generate the report for.                                                                                                                                                              |

Should a report require more than one dataset the paths to these inputs are hard coded to the data folder of this repo.
To ensure that these additional inputs are generated correctly it is recommended to use the data downloader tool provided
with this repository. 

### Report Builders

Each report has an associated report builder script. These scripts can be found in the builders folder in this directory.
The builder script is responsible for building and exporting the report PDF. This includes all parameters for text, page
and layout style. The builder take the data and other essential parameters from the generator script and uses them to 
produce the report.

For PDP, APD, MPS, IDR reports the parameters are as follows:

|  Parameter  | Required | Description                                                                                                                                                          |
|:-----------:|:--------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   in_dict   |   Yes    | Input dictionary containing parameters for building report elements such as the header.                                                                              |
|   data_df   |   Yes    | Dataframe containing the data to be written in the report as a table.                                                                                                |
|   out_dir   |   Yes    | The directory the report will be exported to once complete.                                                                                                          |
|  pagesize   | Optional | Default value is 'Letter'. Specifies the page size. While any page size is possible only Letter has been tested at this time. Use other page sizes at your own risk. |
| orientation | Optional | Default value is 'Portrait'. Specifies the page orientation. Possible values are 'Landscape' or 'Portrait.                                                           |

For DPK and PDD reports the parameters are as follows:

|          Parameter          | Required | Description                                                                             |
|:---------------------------:|:--------:|-----------------------------------------------------------------------------------------|
|           in_dict           |   Yes    | Input dictionary containing parameters for building report elements such as the header. |
|           df_list           |   Yes    | A list of all dataframes that need to be included in the report.                        |
| ps_add_df (only PDD report) |   Yes    | The path to the ps address data (this parameter is only required for PDD reports).      |
|           out_dir           |   Yes    | The directory the report will be exported to once complete.                             |

These reports do not have a page size or orientation parameter as they are hard coded to the specific page size and orientation. Alter
these variables within the code at your own risk. 

## Other Scripts

### report_factory.py

Intake script containing the workflow processing logic for the report creation script. Takes the given workflow and 
converts that into information that can be used to create the desired reports. Handles exporting the reports in an organized
manner to the given export folder.

| Parameter | Description                                                                                            |
|:---------:|--------------------------------------------------------------------------------------------------------|
| workflow  | This is a path to a workflow json file containing all the information required to produce the reports. |

### data_downloader.py

Contains the bulk of the data download logic for the data download tool. Takes the given workflow file and requests that
data from the database using the pre-constructed SQL statements. 

| Parameter | Description                                                                                 |
|:---------:|---------------------------------------------------------------------------------------------|
| settings  | This is a path to a json file containing all the information required to download the data. |

### commons.py

Contains common functions and objects that are used by more than one of the generator scripts. 

### builders/common_builds.py

Contains common functions, and objects that are used by more than one of the builder scripts.

### builders.report_parameters.py

Contains text for common text for a given report type both versions of the bilingual text can be returned from these 
classes. This script contains code that covers static text elements in the report including header and footer text.
