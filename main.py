import lib
from lib import sys, os, glob, configparser, argparse
from lib import pd, datetime

from classes import sensor_df,Sensor
from functions import calculate_intervals,calculate_intervals_csv,create_plot,create_ini_file_from_dict
from scripts import Check_Post_Scripts, Check_Pre_Scripts

## MAIN
if __name__ == "__main__":
    
    # Default directory of the script
    default_dir = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0]))) + "/"
    
    # Default path to config.ini file
    config_file = default_dir + "config.ini"
    
    # Arguments
    parser = argparse.ArgumentParser(description='Sensors utilities')
    
    parser.add_argument('--inifile', required=False, dest='INI', default=config_file,
                        help="Path to configuration (.ini) file ({} if omitted)".format(config_file))
        
    parser.add_argument('--intervals', required=False, dest='CSV', type=argparse.FileType('r'),
                        help='csv file with start and end timestamps columns. '
                              'First row must be the column names (i.e. "start" and "end"). '
                              'Uses minutely intervals if this parameter'
                              'is missing (as defined in config.ini).')
 
    args = parser.parse_args()
        
    # Check if a configuration file was provided
    config_file = args.INI
    
    USE_BOOLS = []
    DATA_PATHS = []
    SETTINGS_PATHS = []
    FULL_NAME_LIST = []
    Number_Of_Sensors = 10
     
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
        # INIT_SETTINGS
        INIT_NEW_SENSOR = eval(config['INIT_SETTINGS']['INIT_NEW_SENSOR'])
        MODELNAME_NEW = eval(config['INIT_SETTINGS']['MODELNAME_NEW'])
        
        FILE_PATH_NEW   = eval(config['INIT_SETTINGS']['DATA_PATH_NEW']) +'/'+ eval(config['INIT_SETTINGS']['FILE_EXT_NEW'])
        SKIPROWS_NEW = eval(config['INIT_SETTINGS']['SKIPROWS_NEW'])
        TIME_COLUMN_NEW = eval(config['INIT_SETTINGS']['TIME_COLUMN_NEW'])
        TIME_FORMAT_NEW = eval(config['INIT_SETTINGS']['TIME_FORMAT_NEW'])
        SEPARATOR_NEW = eval(config['INIT_SETTINGS']['SEPARATOR_NEW'])
        
        
        # OUTPUT_SETTINGS      
        FREQ = eval(config['OUTPUT_SETTINGS']['FREQ'])
        MODE = eval(config['OUTPUT_SETTINGS']['MODE'])
        FILL_TIMES = eval(config['OUTPUT_SETTINGS']['FILL_TIMES'])
        
        START_EXPORT = eval(config['OUTPUT_SETTINGS']['START_EXPORT'])
        END_EXPORT =  eval(config['OUTPUT_SETTINGS']['END_EXPORT'])
        
        DATA_PATH_SAVE_EXPORT = eval(config['OUTPUT_SETTINGS']['DATA_PATH_SAVE_EXPORT'])
        FILE_EXT_SAVE_EXPORT_0 = eval(config['OUTPUT_SETTINGS']['FILE_EXT_SAVE_EXPORT'])
        FILE_PATH_SAVE_EXPORT_0 = DATA_PATH_SAVE_EXPORT + '/' + FILE_EXT_SAVE_EXPORT_0
        
        FILE_PATH_SAVE_EXPORT = FILE_PATH_SAVE_EXPORT_0+'_{freq}{mode}.csv'.format(freq=FREQ,mode=MODE)
        if START_EXPORT!=None and END_EXPORT!=None:
            START_PD = pd.to_datetime(START_EXPORT)
            END_PD = pd.to_datetime(END_EXPORT)
            START_EXPORT = START_PD.strftime('%d-%m-%Y')
            END_EXPORT = END_PD.strftime('%d-%m-%Y')
            FILE_PATH_SAVE_STARTEND = FILE_PATH_SAVE_EXPORT_0+'_{freq}{mode}__{start}__{end}.csv'.format(freq=FREQ,mode=MODE,start=START_EXPORT,end=END_EXPORT)
        
        # GENERAL_SETTINGS and OUTPUT_SETTINGS
        for k in range(1,Number_Of_Sensors+1):
            USE_BOOLS.append(eval(config['OUTPUT_SETTINGS']['USE_SENSOR_'+str(k)]))
            DATA_PATHS.append(eval(config['GENERAL_SETTINGS']['DATA_PATH_SENSOR_'+str(k)]) +'/'+ eval(config['GENERAL_SETTINGS']['FILE_EXT_SENSOR_'+str(k)]))
            SETTINGS_PATHS.append(default_dir + eval(config['GENERAL_SETTINGS']['SETTINGS_SENSOR_'+str(k)]))
            
    else: # Assume default values
        print ('Could not find the configuration file {0}'.format(config_file), file=sys.stderr)
        
        # INIT_SETTINGS
        INIT_NEW_SENSOR = False
        
        # OUTPUT_SETTINGS 
        FREQ = 10
        MODE = 'min'
        FILL_TIMES = False

        START_EXPORT = None
        END_EXPORT = None
        
        FILE_PATH_SAVE_EXPORT = default_dir + 'output/Average_out_{freq}{mode}.csv'.format(freq=FREQ,mode=MODE)
        
        # GENERAL_SETTINGS and OUTPUT_SETTINGS                              
        FILE_PATH_AETH   = default_dir + 'models_settings/AE33_sample.dat'
        FILE_PATH_PMS = default_dir + 'models_settings/PMS1_sample.csv'
        FILE_PATH_ComPAS = default_dir + 'models_settings/ComPASV4_sample.txt'
        FILE_PATH_SMPS = default_dir + 'models_settings/SMPS3080_Export_sample.csv'
        FILE_PATH_MSPTI = default_dir + 'models_settings/MSPTI_Export_sample.csv'
        FILE_PATH_MINIPTI = default_dir + 'models_settings/miniPTI_Export_sample.csv'
        
        SETTINGS_PATH_AETH   = default_dir + 'models_settings/AE33_settings.ini'
        SETTINGS_PATH_PMS = default_dir + 'models_settings/PMSChinaSensor_settings.ini'
        SETTINGS_PATH_ComPAS = default_dir + 'models_settings/ComPAS-V4_settings.ini'
        SETTINGS_PATH_SMPS = default_dir + 'models_settings/SMPS3080_Export_Settings.ini'
        SETTINGS_PATH_MSPTI = default_dir + 'models_settings/MSPTI_settings.ini'
        SETTINGS_PATH_MINIPTI = default_dir + 'models_settings/miniPTI_settings.ini'
        
        USE_BOOLS = [True, True, True, True, True, True]    
        FULL_NAME_LIST = ['Aethalometer', 'PMS China Sensor', 'ComPAS', 'SMPS', 'MSPTI', 'miniPTI']
        DATA_PATHS = [FILE_PATH_AETH, FILE_PATH_PMS, FILE_PATH_ComPAS, FILE_PATH_SMPS, FILE_PATH_MSPTI, FILE_PATH_MINIPTI]
        SETTINGS_PATHS = [SETTINGS_PATH_AETH,SETTINGS_PATH_PMS,SETTINGS_PATH_ComPAS,SETTINGS_PATH_SMPS,SETTINGS_PATH_MSPTI,SETTINGS_PATH_MINIPTI]
        
        for k in range(7,Number_Of_Sensors+1):
            USE_BOOLS.append(False)
            DATA_PATHS.append(default_dir + 'model_settings/no_data.csv')
            FULL_NAME_LIST.append('No Sensor')
            SETTINGS_PATHS.append(default_dir + 'model_settings/no_settings.ini')              
    
    
    # Initializiation Complete    
    print('------------------------', file=sys.stderr)
    
    # if New Sensor initialization is true, skip averaging process etc.    
    if INIT_NEW_SENSOR:
        print('INIT_NEW_SENSOR:\t\t',INIT_NEW_SENSOR, file=sys.stderr)
        
        print('Initializing new sensor data...', file=sys.stderr)
        Sensor_Name = 'mySensor'

        print ("Reading {Sensor_Name} data, model {sensor_model}.".format(Sensor_Name=Sensor_Name, sensor_model=MODELNAME_NEW), file=sys.stderr)
         
        mySensor = Sensor(Sensor_Name,MODELNAME_NEW,FILE_PATH_NEW, skiprows=SKIPROWS_NEW,TimeColumn=TIME_COLUMN_NEW,TimeFormat=TIME_FORMAT_NEW)
        header_out = list(mySensor.signals)
        
        create_ini_dict = {'model': MODELNAME_NEW,
                          'separator' : SEPARATOR_NEW,
                          'skiprows' : SKIPROWS_NEW+1,
                          'TimeFormat' : TIME_FORMAT_NEW,
                          'TimeColumn' : TIME_COLUMN_NEW,
                          'append_text' : '',
                          'quotechar' : '"',
                          'plotkey' : header_out[-1],
                          'header' : header_out,
                          'header_export': header_out,
                          'signal_units_dict': mySensor.signal_units_dict,
                          'other_dict' : mySensor.other_dict
                          }
        file_path_ini_out = "models_settings/{NewModel}_settings.ini".format(NewModel=MODELNAME_NEW)
        create_ini_file_from_dict(file_path_ini_out,create_ini_dict)
        print('------', file=sys.stderr)
        print('Initialization complete.', file=sys.stderr)
        print('------', file=sys.stderr)
        print ("Saved settings .ini file for model {sensor_model} in:\n>>{fpath}".format(sensor_model=MODELNAME_NEW, fpath=default_dir+'/ \n'+file_path_ini_out), file=sys.stderr)
        print ("\nAccess sensor object functions with mySensor.<>,\nor see documentation with help(mySensor)\nor clear memory with del(mySensor).", file=sys.stderr)

        #del(mySensor)
    
    # Else, process and synchronize
    else:
        print('Synchronizing data...', file=sys.stderr)
        print('Mode:\t\t\t', MODE, file=sys.stderr)
        print('Frequency:\t\t', FREQ, file=sys.stderr)
        print('Fill_Times:\t\t', FILL_TIMES, file=sys.stderr)
        
        for use_index, value in enumerate(USE_BOOLS):
            print('Sensor {ind}:\t\t'.format(ind=use_index),value, file=sys.stderr)
       
        # create new dataframe to merge all datas in (stack horizontally)
        total_df = pd.DataFrame()
        total_sensor_df = sensor_df(pd.DataFrame())
        
        # count the sensors used, for debug purpose
        sensor_counts = 0    
        
        for USE_ME,k in zip(USE_BOOLS,range(len(USE_BOOLS))):
            if USE_ME:
                sensor_counts += 1
                print('-------------------', file=sys.stderr)
                
                # Get Data Files and Settings
                Data_File = DATA_PATHS[k]          
                Sensor_Config = SETTINGS_PATHS[k]
       
                # read sensor settings
                config.read(Sensor_Config)
                
                
                Model_Name = eval(config['MODEL_SETTINGS']['model'])
                Sensor_Name = Model_Name
                separator = eval(config['MODEL_SETTINGS']['separator'])
                skiprows = eval(config['MODEL_SETTINGS']['skiprows'])
                TimeFormat = eval(config['MODEL_SETTINGS']['TimeFormat'])
                TimeColumn = eval(config['MODEL_SETTINGS']['TimeColumn'])
                append_text = eval(config['MODEL_SETTINGS']['append_text'])
                quotechar = eval(config['MODEL_SETTINGS']['quotechar'])
                plotkey = eval(config['MODEL_SETTINGS']['plotkey'])
                
                header = eval(config['MODEL_SETTINGS']['header'])
                header_export = eval(config['MODEL_SETTINGS']['header_export'])
                signal_units_dict = eval(config['MODEL_SETTINGS']['signal_units_dict'])
                other_dict = eval(config['MODEL_SETTINGS']['other_dict'])
                
                # if Time Format is 'origin', origin and date_units must be valid inputs
                if TimeFormat in ['origin']:
                    date_units = eval(config['MODEL_SETTINGS']['date_units'])
                    origin = eval(config['MODEL_SETTINGS']['origin'])
                    if origin == 'creation_day_of_file':
                        origin = pd.to_datetime(datetime.fromtimestamp(os.path.getctime(Data_File)).strftime('%D'))
                else:
                    # Use default values
                    date_units='s'
                    origin=pd.to_datetime('1900/01/01')
                    
                print ("Reading {Sensor_Name} data, model {sensor_model}.".format(Sensor_Name=Sensor_Name, sensor_model=Model_Name), file=sys.stderr)
                slash_index = len(Data_File)-Data_File[::-1].find('/')
                print (">> {data_path}".format(data_path=Data_File[:slash_index]), file=sys.stderr)
                
                # create new dataframe if reading list of datasets, to append them (stack vertically)
                events_df = pd.DataFrame()
                events_sensor_df = sensor_df(events_df)
                
                list_of_events = glob.glob(Data_File) # * means all if need specific format then *.csv, or specific file start then <File Start>*
                
                for event_id in range(len(list_of_events)):
                    # get final data file path, if Data_File was a list
                    Data_File_Final = list_of_events[event_id]
                    slash_index = len(Data_File_Final)-Data_File_Final[::-1].find('/')
                    print ("- {data} ".format(data=Data_File_Final[slash_index:] ), file=sys.stderr)
                   
                    # Crate Sensor Object with given parameters
                    SENSOR_Object = Sensor(Sensor_Name,Model_Name,Data_File_Final,header=header,header_export=header_export,signal_units_dict=signal_units_dict,other_dict=other_dict,TimeColumn=TimeColumn,TimeFormat=TimeFormat,append_text=append_text,quotechar=quotechar,separator=separator, skiprows=skiprows, plotkey=plotkey, date_units=date_units,origin=origin)
            
                    # Calibrations and custom Scripts before
                    SENSOR_Object = Check_Pre_Scripts(SENSOR_Object)
                    # Calculate averages:  
                    if args.CSV: # if CSV file is provided
                        intervals_df_all = calculate_intervals_csv(args.CSV, SENSOR_Object.df1.df,column=SENSOR_Object.signals)
                    else: # as config.ini or arguments given
                        intervals_df_all = calculate_intervals(SENSOR_Object.df1,freq=FREQ,mode=MODE,column=SENSOR_Object.signals,decimals=9)
                       
                    # Calculate averages:  
                    if args.CSV: # if CSV file is provided
                        intervals_df_export = calculate_intervals_csv(args.CSV, SENSOR_Object.df1.df,column=SENSOR_Object.signals_export)
                    else: # as config.ini or arguments given
                        intervals_df_export = calculate_intervals(SENSOR_Object.df1,freq=FREQ,mode=MODE,column=SENSOR_Object.signals_export,decimals=9)
                                      
                    # replace df in object
                    SENSOR_Object.df2.df = intervals_df_all
                    SENSOR_Object.df3.df = intervals_df_export
 
                    # Calibrations and custom Scripts after averaging 
                    SENSOR_Object = Check_Post_Scripts(SENSOR_Object)           
                    
                    # # For Debug purposes
                    # SENSOR_Object.df1.df.to_csv(DATA_PATH_SAVE_EXPORT+'Debug_df1_{model}_{number}_id{id}.csv'.format(model=Model_Name,number=sensor_counts,id = event_id), sep=';', na_rep = 0, header=SENSOR_Object.df1.df.columns.values,quotechar = '#')
                    # if event_id == 0:
                    #     SENSOR_Object.df3.df.to_csv(DATA_PATH_SAVE_EXPORT+'Debug_df3_{model}_{number}_id{id}.csv'.format(model=Model_Name,number=sensor_counts,id = event_id), sep=';', na_rep = 0, header=SENSOR_Object.df3.df.columns.values,quotechar = '#')
                    
                    # # drop 'start' timestamp
                    SENSOR_Object.removeSubset('start')   
       
                    # Update df   
                    intervals_df_all = SENSOR_Object.df2.df
                    intervals_df_export = SENSOR_Object.df3.df
                    
                    # # Make 1 Graph, defined per plotkey
                    # y = intervals_df_export[SENSOR_Object.plotkey]
                    # plotTitle = "{Sensor_Name}, Model: {sensor_model}".format(Sensor_Name=Sensor_Name,sensor_model=Model_Name)
                    # create_plot(y, yunits=SENSOR_Object.signal_units_dict.get(SENSOR_Object.plotkey), title=plotTitle, ytitle=str(SENSOR_Object.plotkey))
                    
                    # Join Dataframes and stack vertically
                    events_df = pd.concat([events_df, intervals_df_export]).sort_values('end')
                    events_sensor_df = sensor_df(events_df)
                    
                    # # Clear Memory
                    del(intervals_df_all)
                    del(intervals_df_export)
                    del(SENSOR_Object)
                
                # # Remove time columns with 'start' timestamps. Optional...
                events_sensor_df.removeColumn_from_df('start')   
                total_sensor_df.removeColumn_from_df('start')  
                
                # # Join Dataframes and stack horizontally
                total_df = total_sensor_df.df.join(events_sensor_df.df,rsuffix='_{}'.format(Model_Name),how='outer')
                total_df = total_df.drop_duplicates()
                    
                total_df = total_df.sort_values('end')
                #total_df = total_df.backfill().ffill()
                total_sensor_df = sensor_df(total_df)
                
                # # Clear Memory
                del(events_sensor_df)
                del(total_df)
    
    
        # # Save exports
        total_sensor_df.df.to_csv(FILE_PATH_SAVE_EXPORT, sep=';', na_rep = 0,quotechar = '#')
        
        # # Save Time Subset of exports
        subtotal_df = total_sensor_df.getSubset_df(START_PD,END_PD)
        subtotal_df.to_csv(FILE_PATH_SAVE_STARTEND, sep=';', na_rep = 0,quotechar = '#')
       
        # # Clear Memory
        del(subtotal_df)
        
        
        # # Clear Memory
        #del(total_sensor_df)
        
        print('------', file=sys.stderr)
        print('Synchronization complete.', file=sys.stderr)
        print('------', file=sys.stderr)
        print ("\nAccess merged dataframe with total_sensor_df.<>,\nor see documentation with help(total_sensor_df)\nor clear memory with del(total_sensor_df).", file=sys.stderr)


print('------------------------', file=sys.stderr)
print('Done', file=sys.stderr)


