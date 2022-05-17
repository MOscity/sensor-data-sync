import lib
from lib import sys, os, glob, configparser, argparse
from lib import pd, datetime, timedelta, allantools, np

from classes import sensor_df, Sensor
from functions import calculate_intervals, calculate_intervals_csv, create_plot, create_ini_file_from_dict, my_header_formatter
from scripts import Check_Post_Scripts, Check_Pre_Scripts

# MAIN
if __name__ == "__main__":
    # Performance Check
    start_time = datetime.now()

    # Default directory of the script
    default_dir = os.path.abspath(
        os.path.abspath(os.path.dirname(sys.argv[0]))) + "/"

    # Default path to config.ini file
    config_file = default_dir + "config.ini"

    # Arguments
    parser = argparse.ArgumentParser(description='Sensors utilities')
    parser.add_argument('--inifile', required=False, dest='INI', default=config_file,
                        help="Path to configuration(.ini) file ({} if omitted)".format(config_file))

    parser.add_argument('--intervals', required=False, dest='CSV', type=argparse.FileType('r'),
                        help='csv file with start and end timestamps columns. '
                        'First row must be the column names (i.e. "start" and "end"). '
                        'Uses intervals as defined in config.ini if this argument is '
                        'not provided. Uses 10 minute intervals if this argument is '
                        'missing and config.ini is missing too.')

    args = parser.parse_args()

    # Check which configuration file was provided
    config_file = args.INI

    USE_BOOLS = []
    DATA_PATHS = []
    SETTINGS_PATHS = []

    # Change Number_Of_Sensors if you need more then 10 sensors, and then add accordingly new lines for
    # data paths, settings path, use_sensor_i, etc. in config.ini (see pattern of the first 10 sensors).
    Number_Of_Sensors = 10

    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)

        # INIT_SETTINGS
        INIT_NEW_SENSOR = eval(config['INIT_SETTINGS']['INIT_NEW_SENSOR'])
        MODELNAME_NEW = eval(config['INIT_SETTINGS']['MODELNAME_NEW'])

        FILE_PATH_NEW = eval(config['INIT_SETTINGS']['DATA_PATH_NEW']) + '/' + eval(config['INIT_SETTINGS']['FILE_EXT_NEW'])
        SKIPROWS_NEW = eval(config['INIT_SETTINGS']['SKIPROWS_NEW'])
        TIME_COLUMN_NEW = eval(config['INIT_SETTINGS']['TIME_COLUMN_NEW'])
        TIME_FORMAT_NEW = eval(config['INIT_SETTINGS']['TIME_FORMAT_NEW'])
        SEPARATOR_NEW = eval(config['INIT_SETTINGS']['SEPARATOR_NEW'])

        # OUTPUT_SETTINGS
        FREQ = eval(config['OUTPUT_SETTINGS']['FREQ'])
        MODE = eval(config['OUTPUT_SETTINGS']['MODE'])

        FORWARD_FILL = eval(config['OUTPUT_SETTINGS']['FORWARD_FILL'])
        BACKWARD_FILL = eval(config['OUTPUT_SETTINGS']['BACKWARD_FILL'])
        FIRST_FORWARD = eval(config['OUTPUT_SETTINGS']['FIRST_FORWARD'])
        
        FORMAT_OUTPUT_HEADER = eval(config['OUTPUT_SETTINGS']['FORMAT_OUTPUT_HEADER'])
      
        START_EXPORT = eval(config['OUTPUT_SETTINGS']['START_EXPORT'])
        END_EXPORT = eval(config['OUTPUT_SETTINGS']['END_EXPORT'])
        EXPORT_DAILY = eval(config['OUTPUT_SETTINGS']['EXPORT_DAILY'])

        DATA_PATH_SAVE_EXPORT = eval(config['OUTPUT_SETTINGS']['DATA_PATH_SAVE_EXPORT'])
        FILE_EXT_SAVE_EXPORT_0 = eval(config['OUTPUT_SETTINGS']['FILE_EXT_SAVE_EXPORT'])
        FILE_PATH_SAVE_EXPORT_0 = DATA_PATH_SAVE_EXPORT + '/' + FILE_EXT_SAVE_EXPORT_0

        FILE_PATH_SAVE_EXPORT = FILE_PATH_SAVE_EXPORT_0 + '_{freq}{mode}.csv'.format(freq=FREQ, mode=MODE)
        if START_EXPORT != None and END_EXPORT != None:
            START_PD = pd.to_datetime(START_EXPORT, format='%d.%m.%Y')
            END_PD = pd.to_datetime(END_EXPORT, format='%d.%m.%Y')
            START_EXPORT = START_PD.strftime('%Y-%m-%d')
            END_EXPORT = END_PD.strftime('%Y-%m-%d')
            FILE_PATH_SAVE_STARTEND = FILE_PATH_SAVE_EXPORT_0 + '_{freq}{mode}__{start}__{end}.csv'.format(freq=FREQ, mode=MODE, start=START_EXPORT, end=END_EXPORT)

        # GENERAL_SETTINGS and OUTPUT_SETTINGS
        for k in range(1, Number_Of_Sensors+1):
            USE_BOOLS.append(eval(config['OUTPUT_SETTINGS']['USE_SENSOR_'+str(k)]))
            DATA_PATHS.append(eval(config['GENERAL_SETTINGS']['DATA_PATH_SENSOR_'+str(k)]) + '/' + eval(config['GENERAL_SETTINGS']['FILE_EXT_SENSOR_'+str(k)]))
            SETTINGS_PATHS.append(default_dir + eval(config['GENERAL_SETTINGS']['SETTINGS_SENSOR_'+str(k)]))

    else:  # Assume default values
        print('Could not find the configuration file {0}'.format(config_file), file=sys.stderr)

        # INIT_SETTINGS
        INIT_NEW_SENSOR = False

        # OUTPUT_SETTINGS
        FREQ = 10
        MODE = 'min'

        FORWARD_FILL = True
        BACKWARD_FILL = True
        FIRST_FORWARD = True
        
        FORMAT_OUTPUT_HEADER = True

        START_EXPORT = None
        END_EXPORT = None
        EXPORT_DAILY = False

        FILE_PATH_SAVE_EXPORT = default_dir + 'output/Sample_Average_out_{freq}{mode}.csv'.format(freq=FREQ, mode=MODE)

        # GENERAL_SETTINGS and OUTPUT_SETTINGS
        FILE_PATH_AETH = default_dir + 'sample_datas/AE33_sample.dat'
        FILE_PATH_PMS = default_dir + 'sample_datas/PMS1_sample.csv'
        FILE_PATH_ComPAS = default_dir + 'sample_datas/ComPASV4_sample.txt'
        FILE_PATH_SMPS = default_dir + 'sample_datas/SMPS3080_Export_sample.csv'
        FILE_PATH_MSPTI = default_dir + 'sample_datas/MSPTI_Metas_Export_sample.csv'
        FILE_PATH_MINIPTI = default_dir + 'sample_datas/miniPTI_Export_sample.csv'

        SETTINGS_PATH_AETH = default_dir + 'models_settings/AE33_settings.ini'
        SETTINGS_PATH_PMS = default_dir + 'models_settings/PMSChinaSensor_settings.ini'
        SETTINGS_PATH_ComPAS = default_dir + 'models_settings/ComPAS-V4_settings.ini'
        SETTINGS_PATH_SMPS = default_dir + 'models_settings/SMPS3080_Export_Settings.ini'
        SETTINGS_PATH_MSPTI = default_dir + 'models_settings/MSPTI_Metas_settings.ini'
        SETTINGS_PATH_MINIPTI = default_dir + 'models_settings/miniPTI_settings.ini'

        USE_BOOLS = [True, True, True, True, True, True]
        DATA_PATHS = [FILE_PATH_AETH, FILE_PATH_PMS, FILE_PATH_ComPAS,FILE_PATH_SMPS, FILE_PATH_MSPTI, FILE_PATH_MINIPTI]
        SETTINGS_PATHS = [SETTINGS_PATH_AETH, SETTINGS_PATH_PMS, SETTINGS_PATH_ComPAS,SETTINGS_PATH_SMPS, SETTINGS_PATH_MSPTI, SETTINGS_PATH_MINIPTI]

        for k in range(7, Number_Of_Sensors+1):
            USE_BOOLS.append(False)
            DATA_PATHS.append(default_dir + 'model_settings/no_data.csv')
            SETTINGS_PATHS.append(default_dir + 'model_settings/no_settings.ini')

    # Initializiation Complete
    print('---------------------------------', file=sys.stderr)

    # if New Sensor initialization is true, skip averaging process etc.
    if INIT_NEW_SENSOR:
        print('INIT_NEW_SENSOR:\t\t', INIT_NEW_SENSOR, file=sys.stderr)

        print('Initializing new sensor data...', file=sys.stderr)
        Sensor_Name = 'mySensor'

        print("Reading {Sensor_Name} data, model {sensor_model}.".format(Sensor_Name=Sensor_Name, sensor_model=MODELNAME_NEW), file=sys.stderr)

        # if Time Format is 'origin', origin and date_units must be valid inputs
        if TIME_FORMAT_NEW in ['origin']:
            DATE_UNITS_NEW = eval(config['INIT_SETTINGS']['DATE_UNITS_NEW'])
            ORIGIN_NEW = eval(config['INIT_SETTINGS']['ORIGIN_NEW'])
            if ORIGIN_NEW == 'creation_day_of_file':
                ORIGIN_NEW = pd.to_datetime(datetime.fromtimestamp(
                    os.path.getctime(FILE_PATH_NEW)).strftime('%d-%m-%Y %H:%M:%S'))
            elif ORIGIN_NEW == 'modification_day_of_file':
                ORIGIN_NEW = pd.to_datetime(datetime.fromtimestamp(
                    os.path.getmtime(FILE_PATH_NEW)).strftime('%d-%m-%Y %H:%M:%S'))
            else:
                ORIGIN_NEW = pd.to_datetime(ORIGIN_NEW)
        else:
            # Use default values
            DATE_UNITS_NEW = 'D'
            ORIGIN_NEW = pd.to_datetime('1900/01/01')
            
        mySensor = Sensor(Sensor_Name, MODELNAME_NEW, FILE_PATH_NEW, skiprows=SKIPROWS_NEW, TimeColumn=TIME_COLUMN_NEW, TimeFormat=TIME_FORMAT_NEW, origin=ORIGIN_NEW, date_units=DATE_UNITS_NEW)
        header_out = list(mySensor.signals)

        create_ini_dict = {'model': MODELNAME_NEW,
                           'separator': SEPARATOR_NEW,
                           'skiprows': SKIPROWS_NEW,
                           'TimeFormat': TIME_FORMAT_NEW,
                           'TimeColumn': TIME_COLUMN_NEW,
                           'origin': ORIGIN_NEW,
                           'date_units' : DATE_UNITS_NEW,
                           'plotkey': header_out[-1],
                           'header': header_out,
                           'header_export': header_out,
                           'signal_units_dict': mySensor.signal_units_dict
                           }
        file_path_ini_out = "models_settings/{NewModel}_settings.ini".format(NewModel=MODELNAME_NEW)
        create_ini_file_from_dict(file_path_ini_out, create_ini_dict)
        print('------', file=sys.stderr)
        print('Initialization complete.', file=sys.stderr)
        print('------', file=sys.stderr)
        print("Saved settings .ini file for model {sensor_model} in:\n>>{fpath}".format(sensor_model=MODELNAME_NEW, fpath=default_dir+'/ \n'+file_path_ini_out), file=sys.stderr)
        print("\nAccess sensor object functions with mySensor.<>,\nor see documentation with help(mySensor)\nor clear memory with del(mySensor).", file=sys.stderr)

        # del(mySensor)

    # Else, process and synchronize
    else:
        print('Synchronizing data', file=sys.stderr)
        print('Mode:\t\t\t\t', MODE, file=sys.stderr)
        print('Frequency:\t\t\t', FREQ, file=sys.stderr)
        print('Forward Fill:\t\t', FORWARD_FILL, file=sys.stderr)
        print('Back Fill:\t\t\t', BACKWARD_FILL, file=sys.stderr)
        print('First Forward Fill?:', FIRST_FORWARD, file=sys.stderr)
        print('Format Header:\t\t', FORMAT_OUTPUT_HEADER, file=sys.stderr)
        print('---------------------------------', file=sys.stderr)

        for use_index, value in enumerate(USE_BOOLS):
            print('Sensor {ind}:\t\t\t'.format(ind=use_index+1), value, file=sys.stderr)

        # create new dataframe to merge all datas in (stack horizontally)
        total_sensor_df = sensor_df(pd.DataFrame())
        header_export_renamed = []

        # count the sensors used, for debug purpose
        sensor_counts = 0

        for USE_ME, k in zip(USE_BOOLS, range(len(USE_BOOLS))):
            if USE_ME:
                sensor_counts += 1
                print('------------------------', file=sys.stderr)

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
                plotkey = eval(config['MODEL_SETTINGS']['plotkey'])

                header = eval(config['MODEL_SETTINGS']['header'])
                header_export = eval(config['MODEL_SETTINGS']['header_export'])
                signal_units_dict = eval(config['MODEL_SETTINGS']['signal_units_dict'])

                # if Time Format is 'origin', origin and date_units must be valid inputs
                if TimeFormat in ['origin']:
                    date_units = eval(config['MODEL_SETTINGS']['date_units'])
                    origin = eval(config['MODEL_SETTINGS']['origin'])
                    if origin == 'creation_day_of_file':
                        origin = pd.to_datetime(datetime.fromtimestamp(
                            os.path.getctime(Data_File)).strftime('%d-%m-%Y %H:%M:%S'))
                    elif origin == 'modification_day_of_file':
                        origin = pd.to_datetime(datetime.fromtimestamp(
                            os.path.getmtime(Data_File)).strftime('%d-%m-%Y %H:%M:%S'))
                    else:
                        origin = pd.to_datetime(origin)
                else:
                    # Use default values
                    date_units = 'D'
                    origin = pd.to_datetime('1900/01/01')

                print("Reading #{sensor_count}: Sensor {k}, model {sensor_model}.".format(sensor_count=sensor_counts, k=k+1, sensor_model=Model_Name), file=sys.stderr)
                slash_index = len(Data_File)-Data_File[::-1].find('/')
                print(">> {data_path}".format(data_path=Data_File[:slash_index]), file=sys.stderr)

                # create new dataframe if reading list of datasets, to append them (stack vertically)
                events_sensor_df = sensor_df(pd.DataFrame())

                # * means all if need specific format then *.csv, or specific file start then <File Start>*
                list_of_events = glob.glob(Data_File)

                for event_id in range(len(list_of_events)):
                    # get final data file path, if Data_File was a list
                    Data_File_Final = list_of_events[event_id]
                    slash_index = len(Data_File_Final) - Data_File_Final[::-1].find('/')
                    print("- {data} ".format(data=Data_File_Final[slash_index:]), file=sys.stderr)

                    # Crate Sensor Object with given parameters
                    SENSOR_Object = Sensor(Sensor_Name, Model_Name, Data_File_Final, 
                                           header=header, header_export=header_export, 
                                           signal_units_dict=signal_units_dict,
                                           TimeColumn=TimeColumn, TimeFormat=TimeFormat, 
                                           separator=separator, skiprows=skiprows, 
                                           plotkey=plotkey, 
                                           date_units=date_units, origin=origin)
                    

                    SENSOR_Object = Check_Pre_Scripts(SENSOR_Object)
                    # Calculate averages of export signals:
                    if args.CSV:  # if CSV file is provided
                        intervals_df_export = calculate_intervals_csv(args.CSV, SENSOR_Object.df1, column=SENSOR_Object.signals_export)
                    else:  # as config.ini or arguments given
                        intervals_df_export = calculate_intervals(SENSOR_Object.df1, freq=FREQ, mode=MODE, column=SENSOR_Object.signals_export, decimals=9)

                    # Calibrations and custom Scripts after average
                    if len(intervals_df_export) > 0:
                        SENSOR_Object.df2 = sensor_df(intervals_df_export.copy())
                        # SENSOR_Object.df2 = Check_Post_Scripts(sensor_df(intervals_df_export.copy()), model_name=Model_Name)
                        SENSOR_Object = Check_Post_Scripts(SENSOR_Object)
        
                        # # Make 1 Graph, defined per plotkey
                        if (SENSOR_Object.df2.df.columns.values.tolist().count(SENSOR_Object.plotkey) > 0):
                            y = SENSOR_Object.df2.df[SENSOR_Object.plotkey]
                            plotTitle = "Sensor: {sensor_model}".format(sensor_model=Model_Name)
                            if len(y) > 0:
                                if SENSOR_Object.signal_units_dict != None:
                                    create_plot(y, yunits=SENSOR_Object.signal_units_dict.get(SENSOR_Object.plotkey, ''), title=plotTitle, ytitle=str(SENSOR_Object.plotkey))
                                else:
                                    create_plot(y, yunits='', title=plotTitle, ytitle=str(SENSOR_Object.plotkey))
                        
                        
                        if FIRST_FORWARD and FORWARD_FILL:
                            SENSOR_Object.df2.df = SENSOR_Object.df2.df.ffill()
                        
                        if BACKWARD_FILL:
                            SENSOR_Object.df2.df = SENSOR_Object.df2.df.backfill()
                          
                        if (not FIRST_FORWARD) and FORWARD_FILL:
                            SENSOR_Object.df2.df = SENSOR_Object.df2.df.ffill()
                            
                        # Join Dataframes and stack vertically
                        events_df = pd.concat([events_sensor_df.df, SENSOR_Object.df2.df]).sort_values('end')
                        events_sensor_df = sensor_df(events_df)
                        del(events_df)


                    # # Clear Memory
                    del(intervals_df_export)
                    del(SENSOR_Object)
                    
                
                # # Remove time columns with 'start' timestamps.
                events_sensor_df.removeColumn_from_df('start')
                total_sensor_df.removeColumn_from_df('start')


                # # Format Header
                if FORMAT_OUTPUT_HEADER:
                    new_cols_to_add = my_header_formatter(events_sensor_df.df.columns.values.tolist())
                else:
                    new_cols_to_add = events_sensor_df.df.columns.values.tolist()

                for str_indx, str_value in enumerate(new_cols_to_add):
                    new_cols_to_add[str_indx] = '{}_'.format(Model_Name).replace('-', '_') + str_value
                    header_export_renamed.append(new_cols_to_add[str_indx])

                # # Join Dataframes and stack horizontally
                total_df = total_sensor_df.df.join(events_sensor_df.df, rsuffix='_{}'.format(Model_Name), how='outer')

                total_df = total_df.sort_values('end')

                # # If even more misssing data should be filled, uncomment this:
                #
                # total_df = total_df.backfill()
                # total_df = total_df.ffill()

                total_sensor_df = sensor_df(total_df)

                # # Clear Memory
                del(events_sensor_df)
                del(total_df)

        # drop duplicate entries at the end
        total_sensor_df.df = total_sensor_df.df.drop_duplicates()

        # # Save exports
        total_sensor_df.df.to_csv(FILE_PATH_SAVE_EXPORT, sep=';',header=header_export_renamed, na_rep=0, quotechar='#')


        # =============================================================================
        #         # # Calculate Allan Deviation of a signal:
        #         #
        #         # if MODE == 'sec':
        #         #     rates = FREQ
        #         # elif MODE == 'min':
        #         #     rates = FREQ*60
        #         # else:
        #         #     rates = FREQ*60*24
        #         
        #         # data_all = total_sensor_df.df['R1 [uPa]'].tolist()
        #         # (taus_out_all, ad_all, ade_all, adn_all) = allantools.oadev(data_all, rate=1.0/rates, data_type="freq", taus="all")
        #         # allan_df_all = pd.DataFrame({'Taus_min_all': taus_out_all/60, 'ad_all': ad_all, 'ad_error_all': ade_all, 'ad_number_all': adn_all})   
        #         # allan_df_all.to_csv(DATA_PATH_SAVE_EXPORT+'/'+FILE_EXT_SAVE_EXPORT_0+'_{freq}{mode}__AllanDeviation_All.csv'.format(freq=FREQ,mode=MODE), sep=';', na_rep=0, quotechar='#')
        # 
        # =============================================================================

        # Options START_EXPORT and END_EXPORT are defined:
        if START_EXPORT != None and END_EXPORT != None:
            # # Save Time Subset of exports
            subtotal_df = total_sensor_df.getSubset_df(START_PD, END_PD)
            subtotal_df.to_csv(FILE_PATH_SAVE_STARTEND, sep=';',header=header_export_renamed, na_rep=0, quotechar='#')

            # # Clear Memory
            del(subtotal_df)

        # Option EXPORT_DAILY is True:
        if EXPORT_DAILY and START_EXPORT != None and END_EXPORT != None:
            START_EXPORT_Day = pd.to_datetime(START_EXPORT, format='%Y-%m-%d')
            END_EXPORT_Day = pd.to_datetime(END_EXPORT, format='%Y-%m-%d')
            START_PD_N = START_EXPORT_Day

            dcount = 0
            while START_PD_N < END_EXPORT_Day:
                START_PD_N = START_EXPORT_Day + timedelta(days=dcount)
                END_PD_N = START_EXPORT_Day + timedelta(days=dcount+1)

                START_EXPORT_N = START_PD_N.strftime('%Y-%m-%d')
                END_EXPORT_N = END_PD_N.strftime('%Y-%m-%d')

                FILE_PATH_SAVE_STARTEND_N = FILE_PATH_SAVE_EXPORT_0 + '_{freq}{mode}__{start}__{end}.csv'.format(freq=FREQ, mode=MODE, start=START_EXPORT_N, end=END_EXPORT_N)

                # # Save Time Subset of exports
                subtotal_df = total_sensor_df.getSubset_df(START_PD_N, END_PD_N)
                if len(subtotal_df) > 0:
                    subtotal_df.to_csv(FILE_PATH_SAVE_STARTEND_N, sep=';',header=header_export_renamed, na_rep=0, quotechar='#')

                # # Clear Memory
                del(subtotal_df)

                # # Count Days
                dcount += 1

        # # Clear Memory
        # del(total_sensor_df)

        print('------', file=sys.stderr)
        print('Synchronization complete.', file=sys.stderr)
        print('------', file=sys.stderr)
        print("\nAccess merged dataframe with total_sensor_df.<>,\nor see documentation with help(total_sensor_df)\nor clear memory with del(total_sensor_df).", file=sys.stderr)

    end_time = datetime.now()
    print('------------------------', file=sys.stderr)
    print('Done. Code executed in', end_time - start_time, file=sys.stderr)
