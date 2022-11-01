# sensor-data-sync

Time-synchronizes several sensor datas in the given time intervals, with optional custom scripts for pre- and post-processing.

Note: Working on update for cleaner Code :) (50% done).

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

### Python 3.9+

configparser  
argparse  
sys  
os  
glob  
pandas  
numpy  
dateutil  
allantools
matplotlib

## 1.) Setup new sensor model settings.ini

### a.) Set input parameters for new model in config.ini

Open config.ini and set all values in section [INIT_SETTINGS]:

- INIT_NEW_SENSOR : True  
  set to True to create new settings.ini file for new model (no data synchronization). i.e., if set to True, all "USE_SENSOR_i" will be interpreted as False.

- MODELNAME_NEW  
  ID Name to recognize the model later

- DATA_PATH_NEW & FILE_EXT_NEW  
  Provide valid data path for input datas

- SKIPROWS_NEW  
  Skip rows before header (important to set correctly!).

- SEPARATOR_NEW  
  Separator in the dataset, use None to interpret datas with python-interpreter
  or "," , "\t", ";", " " ...

- TIME_FORMAT_NEW  
  Time Format for the time datas.  
  Allowed Formats: None, 'Excel', 'DateTime_1Column', 'DateTime_2Column', 'origin', 'DateTime_CustomFormat = <>', 'DateTime_2Column_CustomFormat = <>' or 'Format = <>'.  
  Works best with 'Format = <>', 'DateTime_CustomFormat = <>' or 'DateTime_2Column_CustomFormat = <>'.  
  For example: 'Format = %%d.%%m.%%Y %%H:%%M:%%S' for 30.12.2021 15:45:10.  
  Or 'Format = %%d/%%m/%%Y”, note that “%%f” will parse all the way up to nanoseconds.  
  Note that in this .ini file one must write '%%' instead of '%'.  
  See strftime documentation for more information on choices:  
  https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior.  
  See also help(SENSOR_Object).

- TIME_COLUMN_NEW  
  Column name with the time units. Use None to use first column. Use ['Column1', Column'2] if 2 date-time columns given.  
  If provided, use exact name of the time/index column.

### b.) Run main.py

### c.) Open new created settings.ini file and check if all is correct

See output file 'myModel'\_settings.ini in the directory /models_settings/:

- model : 'myModel'  
  ID Name to recognize the model (needed for custom scripts).

- separator : None  
  Separator in the dataset, use None to interpret datas with python-interpreter  
  or "," , "\t", ";", " ", ...

- skiprows : 0  
  Skip rows before header / first row of datas.
  If a header is provided (!=None), one additional line will be skipped.

- TimeFormat : 'Format = %%d.%%m.%%Y %%H:%%M:%%S', or 'DateTime_2Column_CustomFormat = %%Y-%%m-%%d %%H:%%M:%%S' etc.  
  Time Format for the time datas. See above.

- TimeColumn : ''  
  Column name with the time units. Use None to use first column. Use ['Column1', Column'2] if 2 date-time columns given.  
  If provided, use exact name of the time/index column.

- plotkey : ''  
  Column for preview plot. Use '' or None to use last column. Optional.

- header : []  
  Overwrite header in the datafile. Use None to interpret first row as header. Optional.

- header_export : []  
  Signals to export. If None, header_export = header. Optional.

- signal_units_dict : {}  
  Dictionary for the units of the signals/columns. Use None for no units. Optional.

## 2.) Synchronization process

### a.) Configure config.ini

Open config.ini and set all values in section [OUTPUT_SETTINGS] and [GENERAL_SETTINGS]:

- INIT_NEW_SENSOR : False  
  set to False to execute the data synchronization process of the script.

- FREQ: 1  
  Freq: any integer > 0 for the equidistant time intervals.

- MODE: 'min'  
  Mode: sec, min or hours for the units of the time intervals.  

- DATA_PATH_SAVE_EXPORT & FILE_EXT_SAVE_EXPORT:  
  Path for the output files.  

- FORWARD_FILL: True/False  
  if True, missing values in exported dataframe will be filled (forward in time).  
  if False, missing values will be replaced with 0's.  

- BACKWARD_FILL: True/False  
  if True, missing values in exported dataframe will be filled (backward in time).  
  if False, missing values will be replaced with 0's.  

- FIRST_FORWARD: True/False  
  if FORWARD_FILL & BACKWARD_FILL is true, choose which is applied first:  
  if True, missing values will be first filled forward in time, then additionally backward (if any values are still missing)  

- FORMAT*OUTPUT_HEADER : True/False  
  Format output header: If True, all special characters (e.g. /.:&° etc) will be replaced with *  
  Note: It is then easier to import the data in 'Veusz'.  
  If False, exported header will be as in the original datafiles or as defined in model_settings.ini  

- START_EXPORT & END_EXPORT  
  Start and End Datetime for Export: if provided (if not None), an additional export file will be created  
  containing only data between the given start and end time.  
  Note: All datas defined in config.ini > General_Settings will be read anyway, independent of these inputs.  
  Note: Format must be 'dd.mm.YYYY' (str), e.g.:  
  START_EXPORT : '8.12.2021'  
  END_EXPORT : '22.12.2021'  

- EXPORT_DAILY: True/False  
  Export Daily: if true and START_EXPORT & END_EXPORT is provided, additional files will be created  
  for every day between START_EXPORT and END_EXPORT  

- USE_SENSOR_i : True/False  
  Configuration of sensors to use for processing/synchronization.  

- DATA_PATH_SENSOR_i, FILE_EXT_SENSOR_i, SETTINGS_SENSOR_i  
  Provide valid data directories, file path extensions and settings.ini for the sensors with USE_SENSOR_i = True.  
  File extensions with for example '\*.csv' will use all datas ending with '.csv' .  
  File extensions with for example 'AE33_AE33\*' will use all datas starting with 'AE33_AE33'.  
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

If you like to use python library for data processing (instead of Excel, R, MatLab or similar),  
you can write your own python scripts for pre- or post-processing of the data (before or after the averaging).

### a.) Add your model to the functions Check_Pre_Scripts and Check_Post_Scripts in scripts.py

Open scripts.py and add your model name to the list of Check_Pre_Scripts and Check_Post_Scripts.  
'myNewModel' has to match exactly the 'model' name defined in /models_settings/myModel_settings.ini.

for example:  
in Check_Pre_Scripts add the lines (in between the other elif-statements):

> elif model_name == 'myNewModel':  
> return myNewModel_Pre_Script(SENSOR_Object_df)

in Check_Post_Scripts add the lines (in between the other elif-statements):

> elif model_name == 'myNewModel':  
> return myNewModel_Post_Script(SENSOR_Object_df)

### b.) Write your own Scripts

Open scripts.py and define the functions 'myNewModel'\_Pre_Script and 'myNewModel'\_Post_Script:

for example:

> def myNewModel_Pre_Script(SENSOR_Object_df):  
> return SENSOR_Object_df

> def myNewModel_Post_Script(SENSOR_Object_df):  
> SENSOR_Object_df.Linear_Modify_df('Concentration ug/m3', 1000,0)  
> SENSOR_Object_df.Rename_df_Column('Concentration ug/m3', 'Concentration ng/m3')  
> return SENSOR_Object_df

### c.) Customize Scripts

For more functionality, see library of pandas dataframe. New custom functions can be written and added to the scripts.py for custom processing algorithms.

For example:  
Calculate the Amplitude and Phase (polar coordinates) from the input datasets X and Y (cartesian coordinates) and return the new dataframes:

> def Amplitude_Phase(sensor_df,X_Column,Y_Column,R_Name,Theta_Name):  
> new_R = pd.DataFrame({R_Name: np.sqrt(sensor_df.df[X_Column]**2+sensor_df.df[Y_Column]**2)},index=sensor_df.df.index)  
> new_Th = pd.DataFrame({Theta_Name: np.arctan2(sensor_df.df[Y_Column],sensor_df.df[X_Column])\*180.0/np.pi},index=sensor_df.df.index)  
> return new_R, new_Th

Then use this function in your Pre/Post-Script:

> def myNewModel_Post_Script(SENSOR_Object_df):  
> new_R, new_Th = Amplitude_Phase(SENSOR_Object_df, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')  
> SENSOR_Object_df.addSubset_to_df(new_R, 'R1 [uPa]')  
> SENSOR_Object_df.addSubset_to_df(new_Th, 'Theta1 [deg]')
> return SENSOR_Object_df

Last but not least, run main.py again and see if your scripts works :)
