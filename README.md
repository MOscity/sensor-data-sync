# sensor-data-sync
Processes and time-synchronizes several sensor datas.

## Systems and Packages required
Python 3.6+,
configparser,
pandas,
numpy,
matplotlib


## 1.) Setup new sensor settings data 
### a.) Create new settings.ini for your model  
Open config.ini and set all values in section [INIT_SETTINGS]:  

- INIT_NEW_SENSOR : True      
set to True to create new settings.ini file for new model (no data synchronization). i.e., if set to True, all "USE_SENSOR_i" will be interpreted as False.

- MODELNAME_NEW     
ID Name to recognize the model  

- DATA_PATH_NEW & FILE_EXT_NEW    
Provide valid data path for input datas   

- SKIPROWS_NEW    
Skip rows before header (important to set correctly!) 

- SEPARATOR_NEW     
Separator : "," , "\t", ";", " " ... or set to None to read first row (=NEW_SKIPROWS+1) as header row 

- TIME_FORMAT_NEW       
Time_Format: Allowed Formats: 'Excel', 'DateTime_1Column', 'DateTime_2Column', 'origin', 'Format = <>'. 
See also help(SENSOR_Object). 

- TIME_COLUMN_NEW       
Time Column has to match with the name of the time/index column. 


### b.) Run main.py


### c.) Open new created settings.ini file and check if all is correct
See output file 'myModel'_settings.ini in the directory /models_settings/:

- model : 'myModel'     
ID Name to recognize the model      

- separator : None      
separator in the dataset, use None to interpret datas with python-interpreter or ',' , '\t', ';' etc.       

- skiprows : 2      
Number of rows to skip before first row of datas / header.      

- TimeFormat : 'Format = %%d.%%m.%%Y %%H:%%M:%%S'       
Time Format for the time datas.   
'Excel', 'DateTime_1Column', 'DateTime_2Column', 'origin', 'Format = <>'.     
See also help(SENSOR_Object).   

- TimeColumn : None     
Column name with the time units. Use None to use first column     

- append_text : ''      
not yet implemented feature.    

- quotechar : '"'     
char used for quotations in the datafile.     

- plotkey : ''      
Column for preview plot. Use '' or None to use last column.     

- header : None     
Overwrite header in the datafile. Use None to interpret first row as header.    

- header_export : None    
Signals to export. If None, header_export = header    

- signal_units_dict : None    
Dictionary for the units of the signals/columns. Use None for no units.     

- other_dict : None     
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
Save new model settings in that directory.    

### b.) Run main.py
Run main.py with optional arguments     

- '--inifile' :     
Path to configuration (.ini) file. "default-directory"/config.ini if omitted    

- '--intervals' :     
csv file with start and end timestamps columns. First row must be the column names (i.e. "start" and "end").      
Uses intervals as defined in config.ini if this argument is not provided.     
Uses 10 minute intervals if this argument is missing and config.ini is missing too.
