# Interactive Field Coverage Mapping Tool
## Overview
A Python-based interactive mapping tool developed to visualize engineers’ home locations and coverage areas in UKI, inspired by a gap identified in my current role where no such solution existed. It includes configurable radius zones, account overlays, and interactive team layers to support data-driven decisions on recruitment, resource allocation, and service coverage. Built with folium, pandas, and openpyxl, geopy and pgeocode the tool enhances operational visibility and helps managers identify geographical service gaps and optimize field support.
Finally the tool pulls data from the excel file, downloaded from a CRM Salesforce database handled by my employer.

The excel file consists of the following columns: Service Team Name | Responsible Technician: Member Name	| Inventory Location: Location Name |	City | Country | Zip | Member Name - And it is always named us "UK&I - Technicians-2025-03-28-14-05-41", depending on the date and time of download. The tool looks for the excel file that includes the word "technicians".
The excel file had some flaws: empty cells and duplicates.
- The tool first asks the user of the desired radius in miles. Then it converts it to kilometers for its calculations.
- Then it aims to rid the downloaded excel file of the aforementioned flaws.
- Then it creates another excel file with those flaws removed, for reference.
- IT also creates an error log, in case an error occurs, and stacks the errors based on date/time.
- Finally, the tool generates an HTML file including an interactive map. In there, the user can turn on/off the locations of engineers, accounts as well as the desired radius (travelling distance) around the home address of each individual.
- The user can click on each pin to get information about each engineer and account.
- The user can also toggle on/off each and every one of the engineers, their radiuses and accounts individually.
  
![image](https://github.com/user-attachments/assets/824ef84e-274c-4bdd-8de8-999c4814ad39)
