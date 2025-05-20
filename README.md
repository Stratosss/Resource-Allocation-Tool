# Interactive Field Coverage Mapping Tool
## Overview
A Python-based interactive mapping tool developed to visualize engineers’ home locations and coverage areas in UKI, inspired by a gap identified in my current role where no such solution existed. It includes configurable radius zones, account overlays, and interactive team layers to support data-driven decisions on recruitment, resource allocation, and service coverage. Built with folium, pandas, and openpyxl, geopy and pgeocode the tool enhances operational visibility and helps managers identify geographical service gaps and optimize field support.
Finally the tool pulls data from excel files, downloaded from a CRM Salesforce database.

The excel file consists of the following columns: Service Team Name | Responsible Technician: Member Name	| Inventory Location: Location Name |	City | Country | Zip | Member Name
The excel file had some flaws: empty cells and duplicates.
- The tool first aims to rid the file of those flaws and then map out the coordinates of the home address of each engineer as well as account.
- The tool creates another excel file with those flaws removed, for reference.
- The tool also creates an error log, in case an error occurs, and stacks the errors based on date/time.


