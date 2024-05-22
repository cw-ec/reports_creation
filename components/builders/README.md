# Report Builders

The scripts in this folder take the data cleaned / formatted by the generation scripts and uses that a baseline to build
the report pdf. A more detailed version of these descriptions can be found in the components' directory. 

## Report Builders

Report builders are the scripts responsible for buildings the pdf files. These scripts while they follow similar patterns
are unique to the report they are building and are not interchangeable. Each builder cript follows the following naming 
convention: "build_<report_type>_report.py" so for example the builder for the Polling Division Profile is call "build_pdp_report.py".

## Other Scripts

### common_builds.py

Contains common objects shared by all builder scripts such as the canvas (page template) for landscape and portrait 
page styles. Common custom text styles are also built here to be shared between reports. 

### report_parameters.py

Contains reports specific text organized by report type. These objects contain text for page text elements such as the 
header, footer and table column names, etc. 
