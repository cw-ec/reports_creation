# Reports Creation

Suite of report creation tools. The following reports can be created using this tool:

|         Report Name         | Abbreviation | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:---------------------------:|:------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  Polling District Profile   |     PDP      | Lists all PDs in a given FED. Shows PD number, PD name, electors listed and void status. Totals are included at end of report.                                                                                                                                                                                                                                                                                                                                    |
|  Advance Polling Districts  |     APD      | Lists all APDs in a given FED. Shows APD #, APD name, PDs served, total # of PDs in each APD (includes MOBs and SBPDs). Total number of APDs included at end of report                                                                                                                                                                                                                                                                                            |
|    Mobile Polls Summary     |     MPS      | Lists all MOBs in a given FED. Shows PD #s, # of institutions, electors listed, and APD # for each MOB.                                                                                                                                                                                                                                                                                                                                                           |
|        Descriptions         |     PDD      | Lists the PD street segments for each ORD PD, lists each SBPD and MOB in a given FED. Shows PD #, PD name, and CSD name for every PD. ORD PD: Street names, FROM-TO features, FROM-TO civic # ranges, and sides. TRMs are added at the end of affected ORD PDs in the Prairies only. SBPDs: Building name and civic address associated with it. MOBs: Institution names, institution addresses, and electors listed. There is a sub-total at the end of each MOB. |
| Electoral District Poll Key |     DPK      | Lists every PD street segment for each ORD, SBPD and MOB in a given FED. Each PDSS shows the CSD, street name, the FROM-TO features, the FROM-TO civic # range, side, PD #, and APD #. The PDSS are grouped and ordered by street name, type, direction, and address range, and are sub-grouped by CSD name and type.                                                                                                                                             |

## Requirements

This project will require the installation python 3.9 or newer. Package requirements can be found in the requirements.txt
and can be installed using pip or the package manager of your choice. 

Python will need to be called from the command line to test this open a command prompt window and type the command: python
into the box. If the command is not recognized add the folder containing your python.exe file to the path environment variable for your account.
If the python command opens the Windows store type the following into the search bar: "Manage app execution aliases" and turn of the two python
app installers that listed.

Install required packages using pip:

pip install -r requirements.txt

should pip need to be updated navigate to the folder containing your python.exe and use the following command to update pip

python.exe pip install --upgrade pip



## Usage 

In order to run the reports generation tool you will need to create a workflow. Example workflows can be found in the 
workflows directory at the root of this repository. Each workflow is a JSON file and contains the specific information
needed to direct the script in the creation of the desired reports.

The JSON should be formatted as follows:

{
    "Report Abbreviation": [Array of ED Numbers, etc, etc]
}

Using the above format a valid workflow would look as follows:

{
    "PDP": [47001,48001, 24001],
    "PDD": [24005]
}

The above script would create a PDP report for each of the three ED's listed in the array and a PDD report for the single
ED listed in its associated array. 

## More to come
