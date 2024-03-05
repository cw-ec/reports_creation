# Reports Creation

Suite of report creation tools created using python and leveraging additional libraries such as pandas and reportlab.
Reports are generated by Federal Electoral District (FED) and describe various aspects of the given FED. 

The following reports can be created using this tool:

|         Report Name         | Abbreviation | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:---------------------------:|:------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  Polling District Profile   |     PDP      | Lists all PDs in a given FED. Shows PD number, PD name, electors listed and void status. Totals are included at end of report.                                                                                                                                                                                                                                                                                                                                    |
|  Advance Polling Districts  |     APD      | Lists all APDs in a given FED. Shows APD #, APD name, PDs served, total # of PDs in each APD (includes MOBs and SBPDs). Total number of APDs included at end of report                                                                                                                                                                                                                                                                                            |
|    Mobile Polls Summary     |     MPS      | Lists all MOBs in a given FED. Shows PD #s, # of institutions, electors listed, and APD # for each MOB.                                                                                                                                                                                                                                                                                                                                                           |
|        Descriptions         |     PDD      | Lists the PD street segments for each ORD PD, lists each SBPD and MOB in a given FED. Shows PD #, PD name, and CSD name for every PD. ORD PD: Street names, FROM-TO features, FROM-TO civic # ranges, and sides. TRMs are added at the end of affected ORD PDs in the Prairies only. SBPDs: Building name and civic address associated with it. MOBs: Institution names, institution addresses, and electors listed. There is a sub-total at the end of each MOB. |
| Electoral District Poll Key |     DPK      | Lists every PD street segment for each ORD, SBPD and MOB in a given FED. Each PDSS shows the CSD, street name, the FROM-TO features, the FROM-TO civic # range, side, PD #, and APD #. The PDSS are grouped and ordered by street name, type, direction, and address range, and are sub-grouped by CSD name and type.                                                                                                                                             |
|      Indigenous Lands       |     IDR      | Lists Indigenous Lands in the FED                                                                                                                                                                                                                                                                                                                                                                                                                                 |

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

Install required packages using the provided requirements.txt using pip:

    pip install -r requirements.txt

Should pip need to be updated navigate to the folder containing your python.exe and use the following command to update pip

    python.exe pip install --upgrade pip

## Usage 

In order to run the reports generation tool you will need to create a workflow. Example workflows can be found in the 
workflows directory at the root of this repository. Each workflow is a JSON file and contains the specific information
needed to direct the script in the creation of the desired reports.

The JSON should be formatted as follows:

    {
        "reports": [{
            "type": report appreviation,
            "feds": an array of all fed numbers to create reports for
            "data": the path to the local csv or xlsx containing the data
        }]
    }

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

## More to come
