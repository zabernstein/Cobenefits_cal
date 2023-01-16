import shutil
import openpyxl as xl
import os
import datetime

arcpy.env.overwriteOutput = True

carbon_calc = arcpy.GetParameterAsText(0)
#Multivalue string inputs produce semicolon delimited string
project_areas = arcpy.GetParameterAsText(1)
#counties2, joined with state_FIPS csv to include both county and state name
counties = arcpy.GetParameterAsText(2)
output_folder = arcpy.GetParameterAsText(3)

EZG_field = arcpy.GetParameterAsText(4)
#project_data_sheet = 'Project_Data'
state_field = arcpy.GetParameterAsText(5)
county_field = arcpy.GetParameterAsText(6)

#Split out project area polygons from semicolon delimited string
projects_list = project_areas.split(";")
x = 1
#Loop through each shapefile provided as inputs
for poly in projects_list:
    now = datetime.datetime.now()
    dt_f = now.strftime('%m_%d_%Y_%H_%M_%S')
    print(f'Running for shp {poly}')
    os.mkdir(os.path.join(output_folder,f'{dt_f}_shapefile{x}'))
    #Create feature layer of project shapefile, input for dissolve tool
    projects = arcpy.management.MakeFeatureLayer(in_features = poly, out_layer = f'projects_lyr{x}')
    print(f'Initial project polygons: {arcpy.management.GetCount(projects)}')

    #dissolve project maps based on EZG #, creates one feature per EZG #
    dissolved = arcpy.management.Dissolve(in_features = projects, 
                              out_feature_class = f'projects_dslv{x}', 
                              dissolve_field = EZG_field, 
                              )
    print(f'Dissolved project polygons: {arcpy.management.GetCount(dissolved)}')

    #Use Interesct to get intersection of counties and project polygons, then loop through those in the code below
    county_lyr = arcpy.management.MakeFeatureLayer(in_features = counties, out_layer = f'counties_lyr{x}')
    intersect = arcpy.analysis.Intersect(in_features = [dissolved,county_lyr], out_feature_class = f'intersect_lyr{x}', join_attributes = 'ALL')
    print(f'Intersected project counties: {arcpy.management.GetCount(intersect)}')

    #Create searchcursor to loop through interesected layer
    with arcpy.da.SearchCursor(in_table=intersect, field_names=[EZG_field, county_field, state_field]) as sc:
        for row in sc:
            #Create copy of crabon calculator
            copy = shutil.copy(carbon_calc, os.path.join(output_folder,f'{dt_f}_shapefile{x}', f'{row[0]}_{row[1]}_{row[2]}.xlsx'))
            #Load the copy of the calculator to the script
            wb = xl.load_workbook(filename = copy)
            #load the project data sheet
            sheet = wb.active
            #Paste county and state
            sheet['E48'] = row[1]
            sheet['H48'] = row[2]
            wb.save(filename = copy)
    x = x+1


