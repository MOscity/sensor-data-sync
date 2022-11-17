# sensor-data-sync

Time-synchronizes several sensor datas in the given time intervals (building averages), with optional custom scripts for pre- and post-averaging.  
If writing custom scripts, consider to apply linear transformations before non-linear transformations (averaging is linear).

Note: Working on update for cleaner Code :) (80% done).

## Readme Overview:

- 0.) Installation: Systems and Packages required

- 1.) How to setup new sensor type / model  
  a. Set input parameters for new model in config.ini  
  b. Run main.py or main.sh  
  c. Open new created 'models_setings/your_model_settings.ini' file and check if all is correct  

- 2.) Synchronization process  
  a. Configure config.ini  
  b. Run main.py or main.sh  

- 3.) Create Custom Scripts (optional)  
  a. Add your model to the functions CheckPreScripts and CheckPostScripts in scripts_functions.py  
  b. Write your own Scripts  
  c. Customize Scripts  

## 0.) Systems and Packages required  

A requirements.txt file and a pipfile is provided.  
Install a python environment as you prefer (Conda Environment, Pipenv, ...).  
  
If you have pyenv and pipenv, install python 3.9 (from any directory) via terminal:  
> pyenv install 3.9  
  
And then mount the directory with this script and create a pipenv:  
> cd ./path/to/this/script/  
> pipenv install  

Run the environment with  
> pipenv shell  

And open your workspace with for example VS Code:  
> code .  
  
Requirements:  
##### Python 3.9  
configparser  
argparse  
pandas  
numpy  
allantools  
matplotlib  
  

### How To Run: 

#### main.py
Open your python environment in the directory with the \_\_main\_\_.py file.  
Open the \_\_main\_\_.py file and set the config file name in the setup section.  
 
If you are in the directory with the \_\_main\_\_.py file, run the python script from terminal with:  
> python \_\_main\_\_.py  
 
If you are in the parent directory, you can run the script from terminal with:  
> python sensor-data-sync  
 
#### main.sh  
Open a terminal and navigate to the directory with the main.sh file.  
Run the script with (optional args: ini, intervals, ... )  
> ./main.sh  
> ./main.sh ini  s
> ./main.sh ini csv_file  
> ./main.sh kwargs [args]
  
See 'main.sh' for args options.

## 1.) How to setup new sensor type / model  

### a.) Set input parameters for new model in config.ini  

- Open config.ini and set all values in section [settingsInit]. 

- Set isSensorNewInitialized to True if you want to initialize new sensor types.  

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
  
- plotColumn : ''  
  Column for preview plot. Use '' or None to use last column. Optional.  

- headerList : []  
  Overwrite header in the datafile. Use None to interpret first row as header. Optional.  

- exportHeaderList : []  
  Signals to export. If None, header_export = header. Optional.  

- unitsOfColumnsDictionary : {}  
  Dictionary for the units of the signals/columns. Use None for no units. Optional.  

## 2.) Synchronization process  

### a.) Configure config.ini  

Open config.ini and set isSensorNewInitialized in section [setetingsInit] to False to execute the data synchronization process of the script.  
Then set all values in section [settingsOutput] and [settingsGeneral]:  

- outputInterval: 1  
  outputInterval: any integer > 0 for the equidistant time intervals.  

- outputIntervalUnits: 'min'  
  outputIntervalUnits: 'sec', 'min', 'hours' or 'days' for the units of the time intervals.  

- exportDirectoryPathString & exportFileNameString:  
  Directory Path and file extension for the output files.  

- isFilledForward: True/False  
  if True, missing values in exported dataframe will be filled (forward in time).  
  if False, missing values will be replaced with 0's.  

- isFilledBackward: True/False  
  if True, missing values in exported dataframe will be filled (backward in time).  
  if False, missing values will be replaced with 0's.  

- isFilledFirstForwardThenBackward: True/False  
  if isFilledForward & isFilledBackward is true, choose which is applied first:  
  if True, missing values will be first filled forward in time, then additionally backward (if any values are still missing)  

- isOutputHeaderFormatted : True/False  
  Format output header: If True, all special characters (e.g. /.:&° etc) will be replaced with _  
  Note: It is then easier to import the data in 'Veusz'.  
  If False, exported header will be as in the original datafiles or as defined in model_settings.ini  

- exportStartDate & exportEndDate  
  Start and End Datetime for Export: if provided (if not None), an additional export file will be created  
  containing only data between the given start and end time.  
  Note: All datas defined in config.ini > General_Settings will be read anyway, independent of these inputs.  
  Note: Format must be 'dd.mm.YYYY' (str), e.g.:  
  exportStartDate : '8.12.2021'  
  exportEndDate : '22.12.2021'  

- areAdditionalFilesExportedForEachDay: True/False  
  Export Daily: if true and exportStartDate & exportEndDate is provided, additional files will be created  
  for every day between exportStartDate and exportEndDate  

- isSensorProcessed_i : True/False  
  Configuration of sensors to use for processing/synchronization.  

- sensorDataDirectoryPathString_i, sensorDataFileExtensionString_i, sensorModelSettingsRelativePathString_i  
  Provide existing data directories, file path extensions and settings.ini for the sensors with isSensorProcessed_i = True.  
  File extensions with for example '\*.csv' will use all datas ending with '.csv' .  
  File extensions with for example 'AE33_AE33\*' will use all datas starting with 'AE33_AE33'.  
  Model Settings directory is in the same directory as this script and should not be moved.  
  Save new model settings in that directory and provide a valid path for sensorModelSettingsRelativePathString_i (see other models as example).  
  
### b.) Run the script  
  
Run main.py or main.sh with optional arguments.  
See './main.sh' for arguments or './\_\_main\_\_.py'  
  
## 3.) Create Custom Scripts (optional)  
  
If you like to use python for further data analysis or processing (instead of Excel, R, MatLab or similar), look no further!  
Here you can write your own python scripts for pre- or post-processing of the data (before or after the averaging).  
  
### a.) Create default script names and structure in /custom_scripts/:

Open the './custom_scripts/' directory and add a new python script, e.g. 'my_custom_script.py'.  
You can use the given scripts as templates.  
  
The default structure looks like this:  
  
> from lib import np # import numpy if you like to. See '/lib/\_\_init\_\_.py' for loaded libraries.
>
> def myNewModel_Pre_Script(sensorObject):
>> return sensorObject
>  
> def myNewModel_Post_Script(sensorObject):
>> return sensorObject
  

- If you need more libraries, add them with an import statement in '/lib/\_\_init\_\_.py' as the other libraries.
  

### b.) Add your model to scripts_functions.py  

Then add your model to './scripts_functions.py':  
Import it as the other functions and add it to the if-else cases below (both Pre and Post script).  
  
- In CheckPreScripts add the lines (in between the other elif-statements):  
  
> ...  
> elif model_name == 'modelName':  # <----  
>>  return myNewModelScriptName.myNewModel_Pre_Script(sensorObject)  # <----  
  
 where 'modelName' has to match exactly the 'modelName' name defined in '/models_settings/myModel_settings.ini'.  
  
- Then, in CheckPostScripts add the lines (in between the other elif-statements):  
  
> ...  
> elif model_name == 'modelName':  
>> return myNewModelScriptName.myNewModel_Post_Script(sensorObject)  
  
Make sure to replace the names with your names:  
- modelName  
- my_custom_script  
- myNewModel_Pre_Script  
- myNewModel_Post_Script  
  
 
### c.) Customize your scripts in more details  

Open your './custom_scripts/my_custom_script.py' file and define the functions in more details.  
For possible transformations and operations, see help(sensor) in /classes/sensor.py or access pd.DataFrame() methods by calling sensorObject.df1.df or sensorObject.df2.df  
See implemented functions in /classes/sensor.py and /classes/sensor_df.py.  
- sensor_df is child class of sensor and holds a pd.Dataframe() (accessed via sensor_df.df)  
- sensor_df is essentialy a pandas DataFrame with some custom functions added.  
- sensor is parent class of sensor_df, and child class of object. sensor has 3 sensor_df subclasses, which can be accessed via  
> sensor.df1  # (for raw data and data after prescript)
> sensor.df2  # (for data after averaging and postscripts)
> sensor.df3  # (not used) allowing to handle different sub-dataframes.  
  
For more functionality, see library of pandas dataframe.  

Note: sensorObject.df1.df is the pd.Dataframe used to load the data, and transform with PreScripts before averaging.  
and sensorObject.df2.df is populated during averaging process and then transformed in the PostScripts.  
Therefore:  
- In your PreScripts, access, transform or play with sensorObject.df1  
- In your PostScripts, access, transform or play with sensorObject.df2  
  
For example:  
  
> def myNewModel_Pre_Script(sensorObject):  
>> sensorObject.addSubset(np.arange(len(sensorObject.df1.df)), ['OldIndex'], newUnits=['count'], dfIndex=1)  
>> return sensorObject  
>  
> def myNewModel_Post_Script(sensorObject):  
>> sensorObject.LinearModify('Concentration ug/m3', 1000,0, dfIndex=2)  
>> sensorObject.renameColumnInSensorDf('Concentration ug/m3', 'Concentration ng/m3', dfIndex=2)  
>> sensorObject.addSubset(np.arange(len(sensorObject.df2.df)), ['NewIndex'], newUnits=['count'], dfIndex=2)  
>> return sensorObject  
  
Last but not least, run sensor-data-sync again and see if your custom scripts works :)  
  
### Happy Coding :)
  
