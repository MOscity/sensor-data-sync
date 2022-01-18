# sensor-data-sync
Processes and time-synchronizes several sensor datas with custom scripts.  

 Work in progress...  
 
Overview of Readme:  
- 0.) Systems and Packages required   

- 1.) Setup new sensor model settings.ini  
a. Set input parameters for new model in config.ini    
b. Run main.py  
c. Open new created settings.ini file and check if all is correct  

- 2.) Synchronization process  
a. Configure config.ini     
b. Run main.py   

- 3.) Create Custom Scripts (optional)  
a. Add your model to the functions Check_Pre_Scripts and Check_Post_Scripts   
b. Write your own Scripts   
c. Customize Scripts     

## 0.) Systems and Packages required  
Python 3.6+  
configparser  
pandas  
numpy  
matplotlib  


## 1.) Setup new sensor model settings.ini
### a.) Set input parameters for new model in config.ini
Open config.ini and set all values in section [INIT_SETTINGS]:  

- INIT_NEW_SENSOR : True      
set to True to create new settings.ini file for new model (no data synchronization). i.e., if set to True, all "USE_SENSOR_i" will be interpreted as False.

- MODELNAME_NEW     
ID Name to recognize the model  

- DATA_PATH_NEW & FILE_EXT_NEW    
Provide valid data path for input datas   

- SKIPROWS_NEW    
Skip rows before header (important to set correctly!).

- SEPARATOR_NEW     
Separator in the dataset, use None to interpret datas with python-interpreter 
or "," , "\t", ";", " " ... 

- TIME_FORMAT_NEW       
Time Format for the time datas.   
Allowed Formats: None, 'Excel', 'DateTime_1Column', 'DateTime_2Column', 'origin' or 'Format = <>'.  
For example: 'Format = %%d.%%m.%%Y %%H:%%M:%%S' for 30.12.2021 15:45:10.  
Or 'Format = %%d/%%m/%%Y”, note that “%%f” will parse all the way up to nanoseconds.    
Note that in this .ini file one must write '%%' instead of '%'.   
See strftime documentation for more information on choices:   
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior.   
See also help(SENSOR_Object).   

- TIME_COLUMN_NEW       
Column name with the time units. Use None to use first column.   
If provided, use exact name of the time/index column. 

### b.) Run main.py


### c.) Open new created settings.ini file and check if all is correct
See output file 'myModel'_settings.ini in the directory /models_settings/:

- model : 'myModel'     
ID Name to recognize the model.        

- separator : None      
Separator in the dataset, use None to interpret datas with python-interpreter   
or "," , "\t", ";", " " ...   

- skiprows : 2      
Skip rows before header / first row of datas.
If a header is provided (!=None), one additional line will be skipped.

- TimeFormat : 'Format = %%d.%%m.%%Y %%H:%%M:%%S'       
Time Format for the time datas. See above.

- TimeColumn : ''    
Column name with the time units. Use None to use first column.   
If provided, use exact name of the time/index column. 

- append_text : ''      
Not yet implemented feature.    

- quotechar : '"'     
Character used for quotations in the datafile.     

- plotkey : ''      
Column for preview plot. Use '' or None to use last column.     

- header : []     
Overwrite header in the datafile. Use None to interpret first row as header.    

- header_export : []    
Signals to export. If None, header_export = header.    

- signal_units_dict : {}   
Dictionary for the units of the signals/columns. Use None for no units.     

- other_dict : {}     
Additional dictionary, for example wavelengths for some signals.    



## 2.) Synchronization process
### a.) Configure config.ini

Open config.ini and set all values in section [OUTPUT_SETTINGS] and [GENERAL_SETTINGS]:

- INIT_NEW_SENSOR : False     
set to False to execute the data synchronization process of the script.     

- FREQ: 1     
Freq: any integer > 0 for the equidistant time intervals.     

- MODE: 'min'     
Mode: sec, min or hours for the units of the time intervals.    

- FILL_TIMES: True/False    
Fill_Times: if True, exported dataframe will be in equidistant time intervals (and empty entries are set to 0).      
if False, only non-empty rows will be exported.    
Note: Not yet implemented     

- START_EXPORT & END_EXPORT     
Start and End Datetime for Export: if provided (if not None), an additional export file will be created     
containing only data between the given start and end time.      
Note: All datas defined in config.ini > General_Settings will be read anyway, independent of these inputs.    

- DATA_PATH_SAVE_EXPORT & FILE_EXT_SAVE_EXPORT:     
Path for the output files     

- USE_SENSOR_i : True/False     
Configuration of sensors to use for processing/synchronization.     

- DATA_PATH_SENSOR_i, FILE_EXT_SENSOR_i, SETTINGS_SENSOR_i    
Provide valid data directories, file path extensions and settings.ini for the sensors with USE_SENSOR_i = True.    
File extensions with for example '*.csv' will use all datas ending with '.csv'  .  
File extensions with for example 'AE33_AE33*' will use all datas starting with 'AE33_AE33'.    
Model Settings directory is in the same directory as this script and should not be moved.     
Save new model settings in that directory and provide a valid path for SETTINGS_SENSOR_i (see other models as example).    

### b.) Run main.py
Run main.py with optional arguments     

- '--inifile' :     
Path to configuration (.ini) file. "default-directory"/config.ini if omitted    

- '--intervals' :     
csv file with start and end timestamps columns. First row must be the column names (i.e. "start" and "end").      
Uses intervals as defined in config.ini if this argument is not provided.     
Uses 10 minute intervals if this argument is missing and config.ini is missing too.

## 3.) Create Custom Scripts (optional)
If you like to use python library for data processing instead for example excel.        
Write your custom python scripts for pre- or post-processing of the data (before or after average).   

### a.) Add your model to the functions Check_Pre_Scripts and Check_Post_Scripts        
Open scripts.py and add your model name to the list of Check_Pre_Scripts and Check_Post_Scripts.        
'myNewModel' has to match exactly the name defined in the model_settings.ini.   

for example:  
in Check_Pre_Scripts, add the lines:  
> elif model_name == 'myNewModel':   
> return myNewModel_Pre_Script(SENSOR_Object)  
        
in Check_Post_Scripts, add the lines:   
> elif model_name == 'myNewModel':   
> return myNewModel_Post_Script(SENSOR_Object)   
        
        
### b.) Write your own Scripts  
Open scripts.py and define the functions 'myNewModel'_Pre_Script and _Post_Script: 

for example:  
> def myNewModel_Pre_Script(SENSOR_Object):  
> return SENSOR_Object    
    
> def myNewModel_Post_Script(SENSOR_Object):   
> SENSOR_Object.Linear_Modify('Concentration ug/m3', 1000,0)  
> SENSOR_Object.Rename_sensor_signals('Concentration ug/m3', 'Concentration ng/m3', 'ng/m$^3$')         
> return SENSOR_Object   

### c.) Customize Scripts   
For more functionality, see library of pandas dataframe. New custom functions can be written and added to the scripts.py for custom processing algorithms.  
For example:  

Calculate the Amplitude and Phase (polar coordinates) from the input datasets with X and y (cartesian coordinates) and return the new dataframes:   
> def Amplitude_Phase(sensor_df,X_Column,Y_Column,R_Name,Theta_Name):      
> new_R = pd.DataFrame({R_Name: np.sqrt(sensor_df.df[X_Column]**2+sensor_df.df[Y_Column]**2)},index=sensor_df.df.index)   
> new_Th = pd.DataFrame({Theta_Name: np.arctan2(sensor_df.df[Y_Column],sensor_df.df[X_Column])*180.0/np.pi},index=sensor_df.df.index)   
> return new_R, new_Th    
        
Then use this function in your Pre/Post-Script: 
> def myNewModel_Post_Script(SENSOR_Object):    
> new_R, new_Th = Amplitude_Phase(SENSOR_Object.df2, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')    
> SENSOR_Object.addSubset(new_R, ['R1 [uPa]'], ['uPa'], df_index = [2,3])   
> SENSOR_Object.addSubset(new_Th, ['Theta1 [deg]'], ['deg'], df_index = [2,3])
> return SENSOR_Object    

Last but not least, run main.py again and see if your scripts works :)
