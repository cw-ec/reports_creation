# Reports Creation

Suite of report creation tools created using python and leveraging additional libraries such as pandas and reportlab.
Reports are generated by Federal Electoral District (FED) and describe various aspects of the given FED. 

## Report Types and Descriptions

The following reports can be created using this tool:

|             Report Name             | Abbreviation | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:-----------------------------------:|:------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      Polling District Profile       |     PDP      | Lists all PDs in a given FED. Shows PD number, PD name, electors listed and void status. Totals are included at end of report.                                                                                                                                                                                                                                                                                                                                    |
|      Advance Polling Districts      |     APD      | Lists all APDs in a given FED. Shows APD #, APD name, PDs served, total # of PDs in each APD (includes MOBs and SBPDs). Total number of APDs included at end of report                                                                                                                                                                                                                                                                                            |
|        Mobile Polls Summary         |     MPS      | Lists all MOBs in a given FED. Shows PD #s, # of institutions, electors listed, and APD # for each MOB.                                                                                                                                                                                                                                                                                                                                                           |
|            Descriptions             |     PDD      | Lists the PD street segments for each ORD PD, lists each SBPD and MOB in a given FED. Shows PD #, PD name, and CSD name for every PD. ORD PD: Street names, FROM-TO features, FROM-TO civic # ranges, and sides. TRMs are added at the end of affected ORD PDs in the Prairies only. SBPDs: Building name and civic address associated with it. MOBs: Institution names, institution addresses, and electors listed. There is a sub-total at the end of each MOB. |
|     Electoral District Poll Key     |     DPK      | Lists every PD street segment for each ORD, SBPD and MOB in a given FED. Each PDSS shows the CSD, street name, the FROM-TO features, the FROM-TO civic # range, side, PD #, and APD #. The PDSS are grouped and ordered by street name, type, direction, and address range, and are sub-grouped by CSD name and type.                                                                                                                                             |
| Communities with Indigenous Peoples |     IDR      | Lists Communities containing Indigenous Peoples in the FED                                                                                                                                                                                                                                                                                                                                                                                                        |

## Requirements

This project will require the installation python 3.9 or newer. Package requirements can be found in the requirements.txt
and can be installed using pip or the package manager of your choice. 

Python will need to be called from the command line to test this open a command prompt window and type the command: python
into the box. If the command is not recognized add the folder containing your python.exe file to the path environment variable for your account.
If the python command opens the Windows store type the following into the search bar: "Manage app execution aliases" and turn of the two python
app installers that listed.

The required additional packages for this tool:

    - Pandas
    - Reportlab
    - oracledb
    - click
    - openpyxl

Install required packages using the provided requirements.txt using pip:

    pip install -r requirements.txt

Should pip need to be updated navigate to the folder containing your python.exe and use the following command to update pip

    python.exe pip install --upgrade pip

If running the data download tool access to the corporate database as well as several additional schemas are required.
Please consult the SQL files in order to determine if additional permissions are required

## Workflow Creation

In order to run the reports generation tool you will need to create a workflow. Example workflows can be found in the 
workflows directory at the root of this repository. Each workflow is a JSON file and contains the specific information
needed to direct the script in the creation of the desired reports.

The JSON for the reports creation tool should be formatted as follows:

    {
        "reports": [{
            "type": report appreviation,
            "feds": an array of all fed numbers to create reports for
            "data": the path to the local csv or xlsx containing the data
        },{
            "type": report appreviation,
            "feds": an array of all fed numbers to create reports for
            "data": the path to the local csv or xlsx containing the data
    }]}

Using the above format a valid workflow creating all reports for three feds would look as follows:

    {"reports":[{
          "type": "PDP",
          "feds": [47001, 48001, 24001],
          "data":".\\data\\pd_nums.csv"
          },{
          "type": "APD",
          "feds": [47001, 48001, 24001],
          "data": ".\\data\\pd_nums.csv"
          },{
          "type": "PDD",
          "feds": [47001, 48001, 24001],
          "data": ".\\data\\pd_desc.csv"
          }, {
          "type": "DPK",
          "feds": [47001, 48001, 24001],
          "data": ".\\data\\pd_desc.csv"
          }, {
          "type": "MPS",
          "feds": [47001, 48001, 24001],
          "data": ".\\data\\pd_nums.csv"
          }, {
          "type": "IDR",
          "feds": [47001, 48001, 24001],
          "data": ".\\data\\PDs and Indigenous Communities.xlsx"
      }]}

The above file can be found in workflows folder at the root of this repository and is meant to serve as a reference when 
creating other workflows.

The above script would create reports of every type for each of the three FED's listed in the array (47001, 48001, and 24001) 
Only the report types being generated need an array unneeded report types can be removed from the workflow.

For the data download tool the format for the workflow JSON is very similar:

    {
        "data": [{
            "type": report appreviation,
            "feds": an array of all fed numbers to create reports for
            "data": the path to the local csv or xlsx containing the data
        }]
    }
A complete workflow for this tool would look as follows:

    {"data": [
        {   
            "username": "usrnme",
            "password": "pwd",
            "database": "db.connect.string",
            "sql_path": "C:\\reports_creation\\sql\\pd_desc.sql",
            "ed_list": [48001, 48004, 48005, 24001]
        },{
            "username": "usrnme",
            "password": "pwd",
            "database": "db.connect.string",
            "sql_path": "C:\\reports_creation\\sql\\pd_nums.sql",
            "ed_list": [48001, 48004, 48005, 24001] 
        },{
            "username": "usrnme",
            "password": "pwd",
            "database": "db.connect.string",
            "sql_path": "C:\\reports_creation-Build-PDF-Report\\sql\\ps_add.sql",
            "ed_list": [48001, 48004, 48005, 24001]
        },{
            "username": "usrnme",
            "password": "pwd",
            "database": "db.connect.string",
            "sql_path": "C:\\reports_creation\\sql\\strm.sql",
            "ed_list": [48001, 48004, 48005, 24001]
        }
    ]}

The above script would download all data for the four listed FEDs. A copy of this script can be found in the workflows
for the folder but not in a working form as that would contain sensitive information. Care should be taken to protect 
this file once created, and it should not be shared or placed on a shared drive.

## Usage

The tools in this repository are designed to be run from a command line interface (CLI) and running the tool outside of 
this type of interface is not recommended or supported. Please note that when run the tools will overwrite any preexisting
files in their respective output folders. If needing to retain any files for archival purposes please make a copy in another
directory.

### Data Download

This tool is responsible for downloading the data from the databases and into local csv files for the reports creation
tool. This tool must be run on a production machine, so it can access the database. Ensure that you have been granted 
all necessary permissions to databases and schemas before running the tool. There are a number of queries each downloading 
data needed for specific reports. To check what data the reports you're downloading need check the Report Creation
tool description below. Below is a table that identifies the csv file each sql query creates

| SQL Query Name | CSV File Name |
|:--------------:|:-------------:|
|  pd_nums.sql   |  pd_nums.csv  |
|  pd_desc.sql   |  pd_desc.csv  |
|    strm.sql    |   strm.csv    |
|   ps_add.sql   |  ps_add.csv   |

The csv files produced above contain all the information necessary to create every report except for the Communities with
Indigenous Peoples report which requires the PDs and Indigenous Communities.xlsx file which is not one of the files produced
by this tool and must be retrieved from a location TBD.

### Report Creation

This tool is responsible for creating the reports

To run the reports creation tool follow the following steps:

    1.) Open the command line and use the cd command to navigate to the root folder of thisa directory.
    
    2.) Type a command to run the tool using the following formula:
            python <tool_name.py> <path_to_workflow.json>
        - python refers to the python environment the project requirements were installed with. Should this keyword not work
          you can replace it with the path to the correct python.exe file.
        - <tool_name.py> refers to the name of the python file you want to run. These files can be found in this projects 
          root folder. 
        - <path_to_workflow.json> this refers to a path to the workflow json file described in the prior section. 
        
    3.) Once the command is created hit enter to run it 

Another method that can be used is to create a .bat file containing the above command. This can be used to chain several
workflows together as needed.

Each report requires certain datasets to be present in the data folder in order for the report to be produced. The table
below shows the report and the required datasets (as csv's). Ensure that the data is present for the specific FED's needed
as the data is only downloaded partially as per the data download tool at any one time.

|               Report                | Abbreviation |          Required Datasets          |
|:-----------------------------------:|:------------:|:-----------------------------------:|
|      Polling District Profile       |     PDP      |             pd_nums.csv             |
|      Advance Polling Districts      |     APD      |             pd_nums.csv             |
|        Mobile Polls Summary         |     MPS      |             pd_nums.csv             |
|            Descriptions             |     PDD      |  pd_desc.csv, strm.csv, ps_add.csv  |
|     Electoral District Poll Key     |     DPK      |             pd_desc.csv             |
| Communities with Indigenous Peoples |     IDR      | PDs and Indigenous Communities.xlsx |

The pdf files will be output in a folder called 'out' in the root folder of this repository. Within the out folder the 
files are sorted into their own folder based on report type
