# ArcGIS Tool for Automating Creation of Co-Benefit Calculation Spreadsheets
## What is this tool used for

The co-benefit calculator spreadsheet requires that a new version of the spreadsheet be created for each project, and for each county that each project covers.
When running the calculator on a high volume of projects, creating this many copies of the spreadsheet adds a lot of time to the process. This tool takes the 
project polygons for given projects and outputs a copy of the co-benefits calculator for each county in each project. The spreadsheets are then filled in with the project number, county, and state in the designated fields in the spreadsheet.

## How to set up for use

This tool is an ArcGIS toolbox (.atbx) file containing a script tool. In order to use it, save this folder in a location that you will be able to find and create a folder connection to that location in the catalog pane. You will then be able to open the script tool from the catalog pane.

## Inputs and requirements for inputs

This tool takes the following inputs:


1. Project area shapefiles
	1. The project area shapefiles must have a field for the project number. If providing multiple shapefiles as inputs, this field must have the *exact* same name in each
	2. The tool can handle shapefile inputs of any geometry, however within our organization project area shapefiles are always polygons
	3. The area of the project area shapefiles should be considered. If the geometry is polgyon and the polygons are very large, the tool could output a very large number of spreadsheets (multiple thousands). The user should make sure that each project area does not cover more than a few counties.
	4. The tool can take multiple shapefiles as inputs. In the output, a separate folder will be created for each shapefile given as an input
2. A copy of the co-benefits calculator spreadsheet
	 * Any .xlsx document will work as an input, however the output locations for the project number, county, and state in the spreadsheet are based on where those fields are in the co-benefits calculator
3. A shapefile with all US counties
	1. This shapefile must include fields for state name and county name. The county names should NOT include the word "county," a requirement based on the input parameters of the co-benefits calculator spreadsheet
	2. In the county shapefile provided in the test data, the state name field is "State" and the county name field is "Name"
4. The co-benefits calculator, and thus this tool, only works with projects in the US

## Outputs

This tool will create a folder for each shapefile provided as an input. In that folder it will output a copy of the input spreadsheet named with the project number, county, and state for that copy of the spreadsheet, and with the project number, county, and state values filled in to designated cells in the spreadhseet

## How to use

1. Open the "CobenCalc" toolbox in the catalog pane and select the "Cobenefits Calculator" script tool. Under "Cobenefits Calculator Spreadsheet" navigate to the cobenefits calculator.
	* In the sample data use 'testfile.xlsx'
2. Under "Project Polygons" select the shapefiles for one or more project polygon shapefiles.
	* In the sample data use 'sample_proj_polys' and 'sample_proj_polys2'
3. Under "County Shapefile" select the US county shapefile
	* In the sample data select 'US_counties'
4. Under "Output Folder" navigate to the folder where you want the outputs saved
5. Under "Project Number Field" select the field from the project polygon shapefile that contains the project numbers
	* In the sample date this field is titled "ProjectNum"
6. Under "State Field" and "County Field" select the fields from the county shapefile that contain the state and county names respectively
	* In the sample data these fields are "State" and "Name" respectively


Click Run. The outputs will be saved in folders in the output folder.