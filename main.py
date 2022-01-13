import configparser, argparse # for argument parsing
from dateutil.parser import parse
import sys, time, os, glob
from dateutil import rrule
from datetime import datetime, timedelta
import numpy as np

import pandas as pd
from pandas.plotting import register_matplotlib_converters

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

from functions import *
from classes import *
from scripts import *

## MAIN
if __name__ == "__main__":
    
    config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/config.ini") 
    
    ae33_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/AE33_settings.ini")
    ae31_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/AE31_settings.ini")
    ComPASV4_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/ComPAS-V4_settings.ini")
    ComPASV5_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/ComPAS-V5_settings.ini")
    PMSChinaSensor_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/PMSChinaSensor_settings.ini")
    MSPTI_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/MSPTI_Settings.ini")
    MINIPTI_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/miniPTI_Settings.ini")     
    SMPS3080_Export_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/SMPS3080_Export_Settings.ini")
    SMPS3080_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/SMPS3080_Settings.ini") # not implemented yet
    new_config_file = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0])) + "/models_settings/new_config.ini") # not implemented yet
    
    parser = argparse.ArgumentParser(description='Sensors utilities')
    
    parser.add_argument('--inifile', required=False, dest='INI', default=config_file,
                        help="Path to configuration (.ini) file ({} if omitted)".format(config_file))

    
    AE_model_parser = parser.add_mutually_exclusive_group(required=False)
    AE_model_parser.add_argument('--AE33', action='store_true',
                              help='Uses file format for AE33 datafiles (default)')
    AE_model_parser.add_argument('--AE31', action='store_true',
                              help='Uses file format for AE31 datafiles')
    parser.set_defaults(AE33=True)
    parser.set_defaults(AE31=False)
    
    
    
    ComPAS_model_parser = parser.add_mutually_exclusive_group(required=False)
    ComPAS_model_parser.add_argument('--ComPASV4', action='store_true',
                              help='Uses file format for ComPAS V4 datafiles (default)')
    ComPAS_model_parser.add_argument('--ComPASV5', action='store_true',
                              help='Uses file format for ComPAS V5 datafiles')
    parser.set_defaults(ComPASV4=True)
    parser.set_defaults(ComPASV5=False)
    
    SMPS_model_parser = parser.add_mutually_exclusive_group(required=False)
    SMPS_model_parser.add_argument('--SMPS3080_Export', action='store_true',
                              help='Uses file format for SMPS Classifier model 3080 exported datafiles (default)')
    SMPS_model_parser.add_argument('--SMPS3080', action='store_true',
                              help='Uses file format for SMPS Classifier model 3180 datafiles datafiles')
    parser.set_defaults(SMPS3080_Export=True)
    parser.set_defaults(SMPS3080=False)
    
    parser.add_argument('--intervals', required=False, dest='CSV', type=argparse.FileType('r'),
                        help='csv file with start and end timestamps columns. '
                              'First row must be the column names (i.e. "start" and "end"). '
                              'Uses minutely intervals if this parameter'
                              'is missing (as defined in config.ini).')
 
        
    parser.add_argument('--ae_config', required=False, dest='ae_ini', default=ae33_config_file,
                        help="Path to Aethalometer settings (.ini) file ({} if omitted)".format(ae33_config_file))
    parser.add_argument('--compas_config', required=False, dest='compas_ini', default=ComPASV4_config_file,
                        help="Path to ComPAS settings (.ini) file ({} if omitted)".format(ComPASV4_config_file))
    parser.add_argument('--smps_config', required=False, dest='smps_ini', default=SMPS3080_Export_config_file,
                        help="Path to SMPS settings (.ini) file ({} if omitted)".format(SMPS3080_Export_config_file))  
    parser.add_argument('--pms_config', required=False, dest='pms_ini', default=PMSChinaSensor_config_file,
                        help="Path to PMS China Sensor settings (.ini) file ({} if omitted)".format(PMSChinaSensor_config_file)) 
    parser.add_argument('--mspti_config', required=False, dest='mspti_ini', default=MSPTI_config_file,
                        help="Path to MSPTI settings (.ini) file ({} if omitted)".format(MSPTI_config_file)) 
    parser.add_argument('--minipti_config', required=False, dest='minipti_ini', default=MINIPTI_config_file,
                        help="Path to miniPTI settings (.ini) file ({} if omitted)".format(MINIPTI_config_file)) 
        
    args = parser.parse_args()
    
    # Check if any models were parsed as arguments
    if args.AE31:
        AE_model = 'AE31'
    elif args.AE33:
        AE_model = 'AE33'
        
    if args.ComPASV4:
        ComPAS_model = 'ComPAS-V4'
    elif args.ComPASV5:
        ComPAS_model = 'ComPAS-V5'
    
    PMS_Model = 'PMS1'
    
    if args.SMPS3080_Export:
        SMPS_Model = 'SMPS3080_Export'
    elif args.SMPS3080:
        SMPS_Model = 'SMPS3080'
     
    MSPTI_Model = 'MSPTI_Export'
    miniPTI_model = 'miniPTI'
    New_Model = 'New Model'
        
    
    # Check if a configuration file was provided
    config_file = args.INI
    
    # Default directory of the script
    default_dir = os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0]))) + "/"
    
    
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
        FREQ = eval(config['GENERAL_SETTINGS']['FREQ'])
        MODE = eval(config['GENERAL_SETTINGS']['MODE'])
        
        USE_AETH = eval(config['GENERAL_SETTINGS']['AETH_Bool'])
        USE_PMS = eval(config['GENERAL_SETTINGS']['PMS_Bool'])
        USE_ComPAS = eval(config['GENERAL_SETTINGS']['ComPAS_Bool'])
        USE_SMPS = eval(config['GENERAL_SETTINGS']['SMPS_Bool'])
        USE_MSPTI = eval(config['GENERAL_SETTINGS']['MSPTI_Bool'])
        USE_miniPTI = eval(config['GENERAL_SETTINGS']['miniPTI_Bool'])
        USE_NEW = eval(config['GENERAL_SETTINGS']['NEW_Bool'])
        
        DATA_PATH_SAVE_EXPORT   = eval(config['GENERAL_SETTINGS']['DATA_PATH_SAVE_EXPORT']) + '/'
        FILE_EXT_SAVE_EXPORT   =  eval(config['GENERAL_SETTINGS']['FILE_EXT_SAVE_EXPORT'])
        
        DATA_PATH_AETH   = eval(config['GENERAL_SETTINGS']['DATA_PATH_AETH']) + '/'
        FILE_EXT_AETH   =  eval(config['GENERAL_SETTINGS']['FILE_EXT_AETH'])

        DATA_PATH_PMS   = eval(config['GENERAL_SETTINGS']['DATA_PATH_PMS']) + '/'
        FILE_EXT_PMS   =  eval(config['GENERAL_SETTINGS']['FILE_EXT_PMS'])
        
        DATA_PATH_ComPAS   = eval(config['GENERAL_SETTINGS']['DATA_PATH_ComPAS']) + '/'
        FILE_EXT_ComPAS   = eval(config['GENERAL_SETTINGS']['FILE_EXT_ComPAS'])
      
        DATA_PATH_SMPS   = eval(config['GENERAL_SETTINGS']['DATA_PATH_SMPS']) + '/'
        FILE_EXT_SMPS   = eval(config['GENERAL_SETTINGS']['FILE_EXT_SMPS'])
        
        DATA_PATH_MSPTI   = eval(config['GENERAL_SETTINGS']['DATA_PATH_MSPTI']) + '/'
        FILE_EXT_MSPTI   = eval(config['GENERAL_SETTINGS']['FILE_EXT_MSPTI'])
        
        DATA_PATH_MINIPTI   = eval(config['GENERAL_SETTINGS']['DATA_PATH_MINIPTI']) + '/'
        FILE_EXT_MINIPTI   = eval(config['GENERAL_SETTINGS']['FILE_EXT_MINIPTI'])
        
        DATA_PATH_NEW   = eval(config['GENERAL_SETTINGS']['DATA_PATH_NEW']) + '/'
        FILE_EXT_NEW   = eval(config['GENERAL_SETTINGS']['FILE_EXT_NEW'])


    else: # Assume default values
        print ('Could not find the configuration file {0}'.format(config_file), file=sys.stderr)
        FREQ = 10
        MODE = 'min'
        
        USE_AETH = True
        USE_PMS = True
        USE_ComPAS = True
        USE_SMPS = True
        USE_MSPTI = False
        USE_miniPTI = False
        USE_NEW = False
        
        DATA_PATH_SAVE = default_dir
        DATA_PATH_AETH = default_dir
        DATA_PATH_PMS = default_dir
        DATA_PATH_ComPAS = default_dir
        DATA_PATH_SMPS = default_dir
        DATA_PATH_MSPTI = default_dir
        DATA_PATH_MINIPTI = default_dir
        DATA_PATH_NEW = default_dir
        
        FILE_EXT_SAVE = 'Average_out.csv'
        
        FILE_EXT_AETH   = '/models_settings/AE33_sample.dat'
        FILE_EXT_PMS = '/models_settings/PMS1_sample.csv'
        FILE_EXT_ComPAS = '/models_settings/ComPASV4_sample.txt'
        FILE_EXT_SMPS = '/models_settings/SMPS3080_Export_sample.csv'
        FILE_EXT_MSPTI = '/models_settings/MSPTI_Export_sample.csv'
        FILE_EXT_MINIPTI = '/models_settings/miniPTI_Export_sample.csv'
        FILE_EXT_NEW = '/models_settings/new_sensor.csv'
     
    # Define new constants
    SAVE_PATH_EXPORT = DATA_PATH_SAVE_EXPORT + FILE_EXT_SAVE_EXPORT
    
    AETH_File = DATA_PATH_AETH+FILE_EXT_AETH
    PMS_File = DATA_PATH_PMS+FILE_EXT_PMS
    ComPAS_File = DATA_PATH_ComPAS+FILE_EXT_ComPAS
    SMPS_File = DATA_PATH_SMPS+FILE_EXT_SMPS
    MSPTI_File = DATA_PATH_MSPTI+FILE_EXT_MSPTI
    miniPTI_File = DATA_PATH_MINIPTI+FILE_EXT_MINIPTI
    NEW_File = DATA_PATH_NEW+FILE_EXT_NEW

    Bool_List = [USE_AETH, USE_PMS, USE_ComPAS, USE_SMPS, USE_MSPTI, USE_miniPTI, USE_NEW]
    
    Models_List = [AE_model, PMS_Model, ComPAS_model, SMPS_Model, MSPTI_Model, miniPTI_model, New_Model]
    Full_Name_List = ['Aethalometer', 'PMS China Sensor', 'ComPAS', 'SMPS','MSPTI', 'miniPTI', 'mySensor']
    Path_List = [AETH_File, PMS_File, ComPAS_File, SMPS_File, MSPTI_File, miniPTI_File, NEW_File]
    #Sensor_Config_List = []
    
    
    total_df = pd.DataFrame()
    total_sensor_df = sensor_df(pd.DataFrame())
    header_list = []
    
    print('------------------------')
    print('Modus:\t\t\t', MODE)
    print('Frequency:\t\t', FREQ)
    print('USE_AETH:\t\t',USE_AETH)
    print('USE_PMS:\t\t',USE_PMS)
    print('USE_ComPAS:\t\t',USE_ComPAS)
    print('USE_SMPS:\t\t',USE_SMPS)
    print('USE_MSPTI:\t\t',USE_MSPTI)
    print('USE_miniPTI:\t',USE_miniPTI)
    print('USE_NEW:\t\t',USE_NEW)
    
    sensor_counts = 0    
    
    for USE_ME,k in zip(Bool_List,range(len(Bool_List))):
        if USE_ME:
            sensor_counts += 1
            
            print('------------------------')
            Sensor_Name = Full_Name_List[k]
            Model_Name = Models_List[k]
            Data_File = Path_List[k]            
            print ("Reading {Sensor_Name} data, model {sensor_model}.".format(Sensor_Name=Sensor_Name, sensor_model=Model_Name), file=sys.stderr)
            
            if Model_Name in ['AE33', 'AE31']:
                Sensor_Config = args.ae_ini
            elif Model_Name == 'PMS1':
                Sensor_Config = args.pms_ini
            elif Model_Name in ['ComPAS-V4','ComPAS-V5']:
                Sensor_Config = args.compas_ini
            elif Model_Name in ['SMPS3080_Export','SMPS3080']:
                Sensor_Config = args.smps_ini
            elif Model_Name in 'MSPTI_Export':
                Sensor_Config = args.mspti_ini
            elif Model_Name in 'miniPTI':
                Sensor_Config = args.minipti_ini
            else: # new model
                Sensor_Config = None
             
            
            if Sensor_Config != None:    
                config.read(Sensor_Config)
                
                separator = eval(config['GENERAL_SETTINGS']['separator'])
                skiprows = eval(config['GENERAL_SETTINGS']['skiprows'])
                TimeFormat = eval(config['GENERAL_SETTINGS']['TimeFormat'])
                TimeColumn = eval(config['GENERAL_SETTINGS']['TimeColumn'])
                append_text = eval(config['GENERAL_SETTINGS']['append_text'])
                quotechar = eval(config['GENERAL_SETTINGS']['quotechar'])
                plotkey = eval(config['GENERAL_SETTINGS']['plotkey'])
                
                header = eval(config['GENERAL_SETTINGS']['header'])
                header_export = eval(config['GENERAL_SETTINGS']['header_export'])
                signal_units_dict = eval(config['GENERAL_SETTINGS']['signal_units_dict'])
                other_dict = eval(config['GENERAL_SETTINGS']['other_dict'])
                
                
                
                if TimeFormat in ['origin']:
                    date_units = eval(config['GENERAL_SETTINGS']['date_units'])
                    origin = eval(config['GENERAL_SETTINGS']['origin'])
                    if origin == 'creation_day_of_file':
                        origin = pd.to_datetime(datetime.fromtimestamp(os.path.getctime(Data_File)).strftime('%D'))
                    SENSOR_Object = Sensor(Sensor_Name,Model_Name,Data_File,
                                         header=header,header_export=header_export,signal_units_dict=signal_units_dict,other_dict=other_dict,
                                         TimeColumn=TimeColumn,TimeFormat=TimeFormat,append_text=append_text,quotechar=quotechar,
                                         separator=separator, skiprows=skiprows, plotkey=plotkey, date_units=date_units,origin=origin)
                
                else:
                    SENSOR_Object = Sensor(Sensor_Name,Model_Name,Data_File,
                                         header=header,header_export=header_export,signal_units_dict=signal_units_dict,other_dict=other_dict,
                                         TimeColumn=TimeColumn,TimeFormat=TimeFormat,append_text=append_text,quotechar=quotechar,
                                         separator=separator, skiprows=skiprows, plotkey=plotkey)
                
            else: # new Model:
                skiprows = eval(config['GENERAL_SETTINGS']['NEW_SKIPROWS'])
                TimeColumn = eval(config['GENERAL_SETTINGS']['TIME_COLUMN'])
                TimeFormat = eval(config['GENERAL_SETTINGS']['TIME_FORMAT'])
                SENSOR_Object = Sensor(Sensor_Name,Model_Name,Data_File, skiprows=skiprows,TimeColumn=TimeColumn,TimeFormat=TimeFormat)
                                     
             
            # Calibrations and custom Scripts before
            SENSOR_Object = Check_Pre_Scripts(SENSOR_Object)
            
            # Calculate averages:  
            if args.CSV: # if CSV file is provided
                intervals_df_all = calculate_intervals_csv(args.CSV, SENSOR_Object.df1.df,column=SENSOR_Object.signals)
            else: # as config.ini or arguments given
                intervals_df_all = calculate_intervals(SENSOR_Object.df1,freq=FREQ,mode=MODE,column=SENSOR_Object.signals,decimals=9)
            
            # Calculate averages:  
            if args.CSV: # if CSV file is provided
                intervals_df_export = calculate_intervals_csv(args.CSV, SENSOR_Object.df1.df,column=SENSOR_Object.mainsignals)
            else: # as config.ini or arguments given
                intervals_df_export = calculate_intervals(SENSOR_Object.df1,freq=FREQ,mode=MODE,column=SENSOR_Object.mainsignals,decimals=9)
                                  
            # replace df in object
            SENSOR_Object.df2.df = intervals_df_all
            SENSOR_Object.df3.df = intervals_df_export
            
            # Calibrations and custom Scripts after averaging 
            SENSOR_Object = Check_Post_Scripts(SENSOR_Object)           
            
            # For Debug purposes
            # SENSOR_Object.df3.df.to_csv(DATA_PATH_SAVE_EXPORT+'Debug_df3_{model}.csv'.format(model=Model_Name), sep=';', na_rep = 0, header=SENSOR_Object.df3.df.columns.values,quotechar = '#')
            
            # # # lazy solution: drop redundant 'start' timestamp
            #total_sensor_df.removeColumn_from_df('start')
            #SENSOR_Object.removeSubset('start')   
            SENSOR_Object.df2.dropDuplicates_in_df('start')
            SENSOR_Object.df3.dropDuplicates_in_df('start')
            
            # Update df   
            intervals_df_all = SENSOR_Object.df2.df.drop_duplicates()
            intervals_df_export = SENSOR_Object.df3.df.drop_duplicates()
            
            total_sensor_df.removeColumn_from_df('start')
            SENSOR_Object.removeSubset('start')   
            
            # Get Columns and units (if given)  
            #sensor_columns = intervals_df_export.columns.values # .tolist()
            #sens_units = (SENSOR_Object.units[key] for key in sensor_columns if key in SENSOR_Object.units)
            
            # Make 1 Graph, defined per plotkey
            y = intervals_df_export[SENSOR_Object.plotkey]
            plotTitle = "{Sensor_Name}, Model: {sensor_model}".format(Sensor_Name=Sensor_Name,sensor_model=Model_Name)
            create_plot(y, yunits=SENSOR_Object.signal_units_dict.get(SENSOR_Object.plotkey), title=plotTitle, ytitle=str(SENSOR_Object.plotkey))
            
            total_df = total_sensor_df.df.join(intervals_df_export,rsuffix='_{}'.format(Model_Name),how='outer')
            #total_df = total_df.drop_duplicates()
            #total_df = total_df.backfill().ffill()
            
            del(total_sensor_df)
            total_sensor_df = sensor_df(total_df)
            
            
            # total_sensor_df.drop_duplicates_in_df()
            
            # del(intervals_df_all)
            # del(intervals_df_export)
            # del(SENSOR_Object)
            # del(total_df)
            
    # Save exports
    total_sensor_df.df.to_csv(SAVE_PATH_EXPORT, sep=';', na_rep = 0,quotechar = '#')


print('Done')


            # # or
            # # Look for earliest timestamp...
            #
            # SENSOR_Object.df2.Rename_df_Column('start','start_{sensor_model}'.format(sensor_model=Model_Name))
            # SENSOR_Object.df3.Rename_df_Column('start','start_{sensor_model}'.format(sensor_model=Model_Name))
            #
            # # Find first data point
            # if sensor_counts == 0:
            #     first_date = intervals_df_export.first_valid_index()
            #     first_sensor = k
            #     first_model_name = Model_Name
            # else:
            #     new_date = intervals_df_export.first_valid_index()
            #     if new_date < first_date:
            #         old_column = 'start_{sensor_model}'.format(sensor_model=first_model_name)
            #         first_date = new_date
            #         first_sensor = k
            #         first_model_name = Model_Name
            #     else:
            #         old_column = 'start_{sensor_model}'.format(sensor_model=Model_Name)            
            #     total_sensor_df.removeColumn_from_df(old_column)
            #     SENSOR_Object.removeSubset(old_column)     