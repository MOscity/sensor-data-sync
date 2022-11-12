# sensor-data-sync

Time-synchronizes several sensor datas in the given time intervals (building averages), with optional custom scripts for pre- and post-averaging.  
If writing custom scripts, consider to apply linear transformations before non-linear transformations (averaging is linear)

Note: Working on update for cleaner Code :) (80% done).

## Readme Overview:

- 0.) Installation: Systems and Packages required

- 1.) How to setup new sensor type / model  
  a. Set input parameters for new model in config.ini  
  b. Run main.py or main.sh  
  c. Open new created models_setings/'your-model-name'_settings.ini file and check if all is correct  

- 2.) Synchronization process  
  a. Configure config.ini  
  b. Run main.py or main.sh  

- 3.) Create Custom Scripts (optional)  
  a. Add your model to the functions Check_Pre_Scripts and Check_Post_Scripts  
  b. Write your own Scripts  
  c. Customize Scripts  

## 0.) Systems and Packages required  

A requirements.txt file and a pipfile is provided.  
Install your python environment as you prefer (Conda, Pipenv, ...).  

Requirements:  
#### Python 3.9+
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


### How To Run: 

#### main.py
Open your python environment in the directory with the \_\_main\_\_.py file.  
Open the \_\_main\_\_.py file and set the config file name in the setup section.  
 
If you are in the directory with the \_\_main\_\_.py file, run the python script with:  
> python \_\_main\_\_.py  
 
If you are in the parent directory, you can run the script with:  
> python sensor-data-sync  
 
#### main.sh  
Open a terminal and navigate to the directory with the main.sh file.  
Run the script with (optional args: ini, intervals, ... )  
> ./main.sh  
> ./main.sh ini  
> ./main.sh ini intervals  

## 1.) How to setup new sensor type / model  

### a.) Set input parameters for new model in config.ini  

- Open config.ini and set all values in section [settingsInit], [settingsOutput] and [settingsGeneral]  

- Set INIT_NEW_SENSOR to True if you want to initialize new sensor types.  

### b.) Run the script  
 
### c.) Open new created settings.ini file and check if all is correct  

Open the output file 'your-model-name'\_settings.ini in the directory /models_settings/:  

- modelName : 'myModel'  
  ID Name to recognize the model (needed for custom scripts).  

- dataSeparator : None  
  Separator in the dataset, use None to interpret datas with python-interpreter  
  or "," , "\t", ";", " ", ...  

- numberOfRowsToSkip : 0  
  Skip rows before header / first row of datas.  
  If a header is provided (!=None), one additional line will be skipped.  

- timeColumnFormat : 'Format = %%d.%%m.%%Y %%H:%%M:%%S', or 'DateTime_2Column_CustomFormat = %%Y-%%m-%%d %%H:%%M:%%S' etc.  
  Time Format for the time datas.  
  Allowed Formats: None, 'Excel', 'DateTime_1Column', 'DateTime_2Column', 'origin',  
  'DateTime_CustomFormat = <>', 'DateTime_2Column_CustomFormat = <>' or 'Format = <>'.  
  Works best with 'Format = <>', 'DateTime_CustomFormat = <>' or 'DateTime_2Column_CustomFormat = <>'.  
  For example: 'Format = %%d.%%m.%%Y %%H:%%M:%%S' for 30.12.2021 15:45:10.  
  Or 'Format = %%d/%%m/%%Y”, note that “%%f” will parse all the way up to nanoseconds.  
  Note that in this .ini file one must write '%%' instead of '%'.  
  See strftime documentation for more information on choices:  
  https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior.  
  See also help(SENSOR_Object).  

- timeColumnName : ''  
  Column name with the time units. Use None to use first column. Use ['Column1', Column'2] if 2 date-time columns given.  
  If provided, use exact name of the time/index column.  
 
- dateTimeOrigin : '2022-03-14 22:58:47'  
  If timeColumnFormat is 'origin', provide the origin date.  
  See https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html  
 
- timeIntervalUnitsString : 's'  
  If timeColumnFormat is 'origin', provide the time units.  
  See https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html  
  
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

Open config.ini and set all values in section [settingsOutput] and [settingsGeneral]:  

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


### b.) Run the script  

Run main.py with optional arguments  

- '--inifile' :  
  Path to configuration (.ini) file. "default-directory"/config.ini if omitted  

- '--intervals' :  
  csv file with start and end timestamps columns. First row must be the column names (i.e. "start" and "end").  
  Uses intervals as defined in config.ini if this argument is not provided.  
  Uses 10 minute intervals if this argument is missing and config.ini is missing too.  


## 3.) Create Custom Scripts (optional)  

If you like to use python for further data analysis or processing (instead of Excel, R, MatLab or similar), look no further!  
Here you can write your own python scripts for pre- or post-processing of the data (before or after the averaging).  

### a.) Add your model to the functions CheckPreScripts and CheckPostScripts in scripts_functions.py  

Open the /custom_scripts/ directory and add a new python script, e.g. my_custom_script.py  
You can use the given scripts as templates.  
Then add your model to scripts_functions.py:  
Import it as the other functions and add it to the if-else cases below (both Pre and Post script).  
'myNewModel' has to match exactly the 'model' name defined in /models_settings/myModel_settings.ini.  

For example:  
in Check_Pre_Scripts add the lines (in between the other elif-statements):  

> ...  
> elif modelName == 'ComPAS-V6':  
>> return ComPAS_scripts_V6.ComPASV6PreScript(sensorObject)  
  
> elif model_name == 'myNewModel':  <----  
>>  return myNewModelScriptName.myNewModel_Pre_Script(sensorObject)  <----  
  
> elif modelName == 'PAX':  
>>  return PAX_scripts.PAXPreScript(sensorObject)  
  
 

in Check_Post_Scripts add the lines (in between the other elif-statements):  
  
> elif model_name == 'myNewModel':  
>> return myNewModelScriptName.myNewModel_Post_Script(sensorObject)  
  
Make sure to replace the 4 names with your names:  
- myNewModel  
- myNewModelScriptName  
- myNewModel_Pre_Script  
- myNewModel_Post_Script  
  
 
### b.) Write your own Scripts  

Open your scripts file and define the functions 'myNewModel'\_Pre_Script and 'myNewModel'\_Post_Script:  
  
For example:  

> def myNewModel_Pre_Script(sensorObject):  
>> 'Do Nothing...'  
>> return sensorObject  
  
> def myNewModel_Post_Script(sensorObject):  
>> sensorObject.LinearModify('Concentration ug/m3', 1000,0)  
>> sensorObject.renameColumnInSensorDf('Concentration ug/m3', 'Concentration ng/m3')  
>> return sensorObject  

### c.) Customize Scripts

New custom functions can be written and added to the /custom_scripts/ directory for custom processing algorithms.  

For example:  
Calculate the Amplitude and Phase (polar coordinates) from the input datasets X and Y (cartesian coordinates) and return the new dataframes:  

> def Amplitude_Phase(sensor_df,X_Column,Y_Column,R_Name,Theta_Name):  
>> new_R = pd.DataFrame({R_Name: np.sqrt(sensor_df.df[X_Column]**2+sensor_df.df[Y_Column]**2)},index=sensor_df.df.index)  
>> new_Th = pd.DataFrame({Theta_Name: np.arctan2(sensor_df.df[Y_Column],sensor_df.df[X_Column])\*180.0/np.pi},index=sensor_df.df.index)  
>> return new_R, new_Th  
  
Then use this function in your Pre/Post-Script:  
  
> def myNewModel_Post_Script(sensorObject):  
>> new_R, new_Th = Amplitude_Phase(sensorObject, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')  
>> sensorObject.addSubsetToDf(new_R, 'R1 [uPa]')  
>> sensorObject.addSubsetToDf(new_Th, 'Theta1 [deg]')  
>> return sensorObject  
  
Last but not least, run sensor-data-sync again and see if your custom scripts works :)  
  
Note:  
  
See implemented functions in /classes/Sensor.py and /classes/sensor_df.py.  
- sensor_df is subclass of Sensor  
- sensor_df is essentialy a pandas DataFrame with some custom functions added.  
- Sensor is a wraparound class, allowing to handle different sub-dataframes.  

For more functionality, see library of pandas dataframe.  
