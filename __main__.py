from lib import sys, os, glob, configparser, argparse
from lib import pd, datetime, timedelta, allantools
from classes import sensor, sensor_df
from plot_functions import createSimplePlot, createAllanDeviationPlot
from util_functions import calculateIntervals, calculateIntervalsAsDefinedInCSVFile, createInitFileFromDictionary, headerFormatter
from scripts_functions import CheckPostScripts, CheckPreScripts

# MAIN
if __name__ == "__main__":
    #################################
    # PLEASE ADJUST BEFORE RUNNING:
    CONFIG_FILE_NAME = "./../configs/config_template_local_testing.ini"
    # and also check the contents of these files, if all is setup as you wish:
    # - ./configs/<your-config-file>.iniss
    # - ./custom_scripts/<your-script>.py
    # -
    # Change NUMBER_OF_MAX_SENSORS if you need more then 10 sensors, and then add accordingly new lines for
    # data paths, settings path, use_sensor_i, etc. in config.ini (see pattern of the first 10 sensors).
    NUMBER_OF_MAX_SENSORS = 10
    #################################

    # Time Performance Check
    dateTimeStart = datetime.now()

    # Default directory of the script
    defaultDir = os.path.abspath(
        os.path.dirname(sys.argv[0]))

    # Default path to config.ini file
    configFilePath = os.path.join(
        defaultDir, "configs", CONFIG_FILE_NAME)

    # Arguments
    parser = argparse.ArgumentParser(description='Sensors utilities')
    parser.add_argument('--inifile', required=False, dest='INI', default=configFilePath,
                        help=f"Path to configuration(.ini) file ({configFilePath} if omitted)")

    parser.add_argument('--csv_intervals', required=False, dest='CSV', default=None,  # type=argparse.FileType('r'),
                        help='csv file with start and end timestamps columns. '
                        'First row must be the column names (i.e. "start" and "end"). '
                        'Uses intervals as defined in config.ini if this argument is '
                        'not provided. Uses default intervals if this argument is '
                        'missing and config.ini is missing too.'
                        'If a csv_intervals file is provided, --interval and --units are ignored.')

    parser.add_argument('--custom_args', required=False, action='store_true', dest='custom_args', default=False,
                        help='Activate custom arguments mode. Add optional arguments afterwards.'
                        'See readme.md or look at the other arguments defined here in main.py.'
                        )

    parser.add_argument('--interval', required=False, metavar='N', dest='N', type=int,
                        help='Interval value between time stamps (int)'
                        )
    parser.add_argument('--units', required=False, dest='units',
                        help='Interval unit between time stamps i.e. ["sec","min","hours", "days"]'
                        )

    parser.add_argument('--export_dir', required=False, dest='export_dir', default=None,
                        help=f'Specify an export directory path (Only the directory!). '
                        'Note: If the directory does not exist, it will be created.'
                        )

    # parser.add_argument('--ffill', required=False, action='store_true', dest='ffill_arg', default=False,
    #                     help=f'Activate Forward Fill. See readme.md about isFilledForward for more information.'
    #                     )

    # parser.add_argument('--bfill', required=False, action='store_true', dest='bfill_arg', default=False,
    #                     help=f'Activate Backward Fill. See readme.md about isFilledBackward for more information.'
    #                     )

    # parser.add_argument('--ffbb', required=False, action='store_true', dest='ffbb_arg', default=False,
    #                     help=f'Activate Fill Forward before Fill Backward, if both others are true.'
    #                     ' See readme.md about isFilledFirstForwardThenBackward for more information.'
    #                     )

    # parser.add_argument('--format_header', required=False, action='store_true', dest='format_header_arg', default=False,
    #                     help=f'Format the resulting header replacing all special characters'
    #                     'with _ or another custom-defined character.'
    #                     )

    # parser.add_argument('--sensor', required=False, metavar='sensorProcess_i_arg', dest='sensorProcess_i_arg', type=list,
    #                     help=f'Activate processing of sensor i. Provide a list like [1,2,3,...]'.
    #                     )

    # parser.add_argument('--addDailyFiles', required=False, action='store_true', dest='addDaily_args', default=False,
    #                 help=f'Export Daily Files between given start and end date'
    #                 )

    args = parser.parse_args()

    # Check which configuration file was provided
    configFilePath = args.INI

    # List Initialization
    sensorsToBeProcessedBooleanList = []
    sensorDataPathsList = []
    sensorModelSettingsPathsList = []

    config = configparser.ConfigParser()

    # Cool shortcut for writng 30 times '-'
    print(f'{"":-^36}', file=sys.stderr)
    print(f'Reading config file: {configFilePath}', file=sys.stderr)

    if os.path.exists(configFilePath):
        isProcessStarted = True
        config.read(configFilePath)

        # settingsInit
        isSensorNewInitialized = eval(
            config['settingsInit']['isSensorNewInitialized'])
        newSensorModelName = eval(config['settingsInit']['newSensorModelName'])

        newSensorDataCompletePath = os.path.join(eval(config['settingsInit']['newSensorDataDirectoryPathString']),
                                                 eval(config['settingsInit']['newSensorDataFileNameString']))
        numberOfRowsToSkipInNewSensorData = eval(
            config['settingsInit']['numberOfRowsToSkipInNewSensorData'])
        nameOfTimeColumnInNewSensorData = eval(
            config['settingsInit']['nameOfTimeColumnInNewSensorData'])
        formatStyleOfTimeColumnInNewSensorData = eval(
            config['settingsInit']['formatStyleOfTimeColumnInNewSensorData'])
        dataSeparatorInNewSensorData = eval(
            config['settingsInit']['dataSeparatorInNewSensorData'])

        # settingsOutput
        if args.N:
            outputInterval = args.N
        else:
            outputInterval = eval(config['settingsOutput']['outputInterval'])

        if args.units:
            outputIntervalUnits = args.units
        else:
            outputIntervalUnits = eval(
                config['settingsOutput']['outputIntervalUnits'])

        if args.CSV:
            CSV_df = pd.read_csv(args.CSV,
                                 index_col=False,
                                 parse_dates=['start', 'end'])
            outputInterval = int(pd.to_datetime(
                CSV_df['end']).diff(1).dt.total_seconds().mean())
            outputIntervalUnits = 'sec'

        isFilledForward = eval(config['settingsOutput']['isFilledForward'])
        isFilledBackward = eval(config['settingsOutput']['isFilledBackward'])
        isFilledFirstForwardThenBackward = eval(
            config['settingsOutput']['isFilledFirstForwardThenBackward'])

        isOutputHeaderFormatted = eval(
            config['settingsOutput']['isOutputHeaderFormatted'])

        exportStartDate = eval(config['settingsOutput']['exportStartDate'])
        exportEndDate = eval(config['settingsOutput']['exportEndDate'])
        areAdditionalFilesExportedForEachDay = eval(
            config['settingsOutput']['areAdditionalFilesExportedForEachDay'])

        if (args.export_dir is not None):
            if not os.path.exists(args.export_dir):
                print(f'{"":#^5}')
                print(
                    f'WARNING: Directory doest not exist, attempting to create {args.export_dir} ...', file=sys.stderr)
                try:
                    os.makedirs(args.export_dir)
                except:
                    print(f'Could not create directory.', file=sys.stderr)
            exportDirectoryPathString = args.export_dir
        else:
            exportDirectoryPathString = eval(
                config['settingsOutput']['exportDirectoryPathString'])

        exportFileNameString = eval(
            config['settingsOutput']['exportFileNameString'])

        try:
            exportBasePathString = os.path.abspath(exportDirectoryPathString)
        except:
            print(f'Please check the export directory path.')

        try:
            exportCompletePathString = os.path.join(
                exportBasePathString, f'{exportFileNameString}_{outputInterval}{outputIntervalUnits}.csv')
        except:
            print(f'{"":#^30}', file=sys.stderr)
            print(
                f'No Interval and units given. Please specify with --interval and --units.', file=sys.stderr)
            print(f'{"":#^30}', file=sys.stderr)

        if exportStartDate != None and exportEndDate != None:
            exportStartPandaDateTime = pd.to_datetime(
                exportStartDate, format='%d.%m.%Y')
            exportEndPandaDateTime = pd.to_datetime(
                exportEndDate, format='%d.%m.%Y')
            exportStartDate = exportStartPandaDateTime.strftime('%Y-%m-%d')
            exportEndDate = exportEndPandaDateTime.strftime('%Y-%m-%d')

        # settingsGeneral and settingsOutput
        for k in range(NUMBER_OF_MAX_SENSORS):
            sensorsToBeProcessedBooleanList.append(
                eval(config['settingsOutput']['isSensorProcessed_'+str(k+1)]))
            sensorDataPathsList.append(os.path.join(eval(config['settingsGeneral']['sensorDataDirectoryPathString_'+str(
                k+1)]), eval(config['settingsGeneral']['sensorDataFileExtensionString_'+str(k+1)])))
            sensorModelSettingsPathsList.append(os.path.join(defaultDir, eval(
                config['settingsGeneral']['sensorModelSettingsRelativePathString_'+str(k+1)])))

    else:  # Assume default values

        print(f'{"":-^36}', file=sys.stderr)
        print(
            f'Could not find the configuration file "{os.path.basename(os.path.normpath(configFilePath))}"', file=sys.stderr)
        print(f'Full path: {configFilePath}', file=sys.stderr)

        print(f'{"":-^36}', file=sys.stderr)
        isDemoString = input(
            f'Start Demo Mode? (type Y or Yes to start, or anything else for No): ')
        isProcessStarted = True if (isDemoString.lower() == 'y'
                                    or isDemoString.lower() == 'yes') else False

        # settingsInit
        isSensorNewInitialized = False

        # settingsOutput
        outputInterval = 30
        outputIntervalUnits = 'sec'

        isFilledForward = True
        isFilledBackward = True
        isFilledFirstForwardThenBackward = True
        isOutputHeaderFormatted = True

        exportStartDate = None
        exportEndDate = None
        areAdditionalFilesExportedForEachDay = False

        exportCompletePathString = os.path.join(
            defaultDir, 'sample_output', f'Sample_Average_out_{outputInterval}{outputIntervalUnits}.csv')

        sampleDataDir = os.path.join(defaultDir, 'sample_datas')
        modelsDataDir = os.path.join(defaultDir, 'models_settings')

        # settingsGeneral and settingsOutput
        sensorDataFiles = ['AE33_sample.dat',
                           'PMS1_sample.csv',
                           'ComPASV4_sample.txt',
                           'SMPS3080_Export_sample.csv',
                           'MSPTI_Metas_Export_sample.csv',
                           'miniPTI_sample.csv']

        sensorConfigFiles = ['AE33_settings.ini',
                             'PMSChinaSensor_settings.ini',
                             'ComPAS-V4_settings.ini',
                             'SMPS3080_Export_Settings.ini',
                             'MSPTI_Metas_settings.ini',
                             'miniPTI_settings.ini']

        sensorsToBeProcessedBooleanList = [
            True if k < 6 else False for k in range(NUMBER_OF_MAX_SENSORS)]
        sensorDataPathsList = [os.path.join(
            sampleDataDir, sensorDataFiles[k]) for k in range(len(sensorDataFiles))]
        sensorModelSettingsPathsList = [os.path.join(
            modelsDataDir, sensorConfigFiles[k]) for k in range(len(sensorConfigFiles))]

    # Initializiation Complete
    print(f'{"":-^36}', file=sys.stderr)

    # if isSensorNewInitialized is true, skip averaging process etc.
    if isSensorNewInitialized:
        print('New Sensor:\t\t',
              isSensorNewInitialized, file=sys.stderr)

        print('Initializing new sensor data...', file=sys.stderr)
        sensorName = newSensorModelName

        print(
            f"Reading {sensorName} data, model {newSensorModelName}.", file=sys.stderr)

        # if Time Format is 'Origin', dateTimeOrigin and timeIntervalUnitsString must be valid inputs
        if formatStyleOfTimeColumnInNewSensorData in ['Origin']:
            timeIntervalUnitsStringNewSensor = eval(
                config['settingsInit']['timeIntervalUnitsStringNewSensor'])
            dateTimeOriginNewSensor = eval(
                config['settingsInit']['dateTimeOriginNewSensor'])

            if dateTimeOriginNewSensor == 'creationDayOfFile':
                dateTimeOriginNewSensor = pd.to_datetime(datetime.fromtimestamp(
                    os.path.getctime(newSensorDataCompletePath)).strftime('%d-%m-%Y %H:%M:%S'))
            elif dateTimeOriginNewSensor == 'modificationDayOfFile':
                dateTimeOriginNewSensor = pd.to_datetime(datetime.fromtimestamp(
                    os.path.getmtime(newSensorDataCompletePath)).strftime('%d-%m-%Y %H:%M:%S'))
            else:
                dateTimeOriginNewSensor = pd.to_datetime(
                    dateTimeOriginNewSensor)
        else:
            # Use default values
            timeIntervalUnitsStringNewSensor = 'D'
            dateTimeOriginNewSensor = pd.to_datetime('1900/01/01')

        newSensorDataCompletePathToFile = glob.glob(newSensorDataCompletePath)
        # Create sensor object and read data
        mySensor = sensor.Sensor(sensorName,
                                 newSensorModelName,
                                 newSensorDataCompletePathToFile[0],
                                 headerList=None,
                                 numberOfRowsToSkip=numberOfRowsToSkipInNewSensorData,
                                 timeColumnName=nameOfTimeColumnInNewSensorData,
                                 timeColumnFormat=formatStyleOfTimeColumnInNewSensorData,
                                 dateTimeOrigin=dateTimeOriginNewSensor,
                                 timeIntervalUnitsString=timeIntervalUnitsStringNewSensor
                                 )
        headerListOut = list(mySensor.signals)

        # create new dictionary for modelsettings file
        newInitDictionary = {'modelName': newSensorModelName,
                             'dataSeparator': dataSeparatorInNewSensorData,
                             'numberOfRowsToSkip': numberOfRowsToSkipInNewSensorData,
                             'timeColumnFormat': formatStyleOfTimeColumnInNewSensorData,
                             'timeColumnName': nameOfTimeColumnInNewSensorData,
                             'dateTimeOrigin': dateTimeOriginNewSensor,
                             'timeIntervalUnitsString': timeIntervalUnitsStringNewSensor,
                             'plotColumn': headerListOut[-1],
                             'headerList': headerListOut,
                             'exportHeaderList': headerListOut,
                             'unitsOfColumnsDictionary': mySensor.unitsOfColumnsDictionary
                             }

        # create modelsettings .ini file from new dictionary
        relativeFilePathOfInit = os.path.join(
            'models_settings', f'{newSensorModelName}_settings.ini')

        createInitFileFromDictionary(
            relativeFilePathOfInit, newInitDictionary)

        print(f'{"":-^36}', file=sys.stderr)
        print('Initialization complete.', file=sys.stderr)
        print(
            f"Saved settings .ini file for model {newSensorModelName} in:\n>>{os.path.join(defaultDir,relativeFilePathOfInit)}")
        print("\nIf you want to access the sensor object functions, add a breakpoint here.\nAccess then within your python shell the functions with mySensor.<>,\nSee documentation with help(mySensor)", file=sys.stderr)

        # Clear Memory
        # del(mySensor)

    # Else, process and synchronize
    elif isProcessStarted:

        print('Synchronizing data', file=sys.stderr)
        if not args.CSV:
            print('Intervals:\t\t\t', outputInterval, file=sys.stderr)
            print('Units:\t\t\t\t', outputIntervalUnits, file=sys.stderr)
        else:
            print(f'Intervals:\t\t\t <CSV Defined>: sec', file=sys.stderr)
            print(
                f'Units:\t\t\t\t <CSV Defined>: {outputInterval}', file=sys.stderr)
        print('Forward Fill:\t\t\t', isFilledForward, file=sys.stderr)
        print('Back Fill:\t\t\t', isFilledBackward, file=sys.stderr)
        print('First Forward Fill?:\t\t',
              isFilledFirstForwardThenBackward, file=sys.stderr)
        print('Format Header:\t\t\t', isOutputHeaderFormatted, file=sys.stderr)
        print(f'Export Path: \n{exportCompletePathString}')
        print(f'{"":-^10}', file=sys.stderr)

        for index, value in enumerate(sensorsToBeProcessedBooleanList):
            print(f'Sensor {index+1}:\t\t\t', value, file=sys.stderr)
        print(f'{"":-^36}', file=sys.stderr)

        # create new dataframe to merge all datas in (stack horizontally)
        dfAllEventsOfAllSensors = sensor_df.sensor_df(pd.DataFrame())
        exportHeaderListRenamed = []

        # count the sensors used, for debug purpose
        sensorsCounted = 0

        for sensor_N_isProcessed, sensorIndex_N in zip(sensorsToBeProcessedBooleanList, range(len(sensorsToBeProcessedBooleanList))):
            if sensor_N_isProcessed:
                sensorsCounted += 1
                print(f'{"":-^20}', file=sys.stderr)

                # Get Data Files and Settings
                sensorDataPathString = sensorDataPathsList[sensorIndex_N]
                sensorModelSettingsPath = sensorModelSettingsPathsList[sensorIndex_N]

                # read sensor settings
                config.read(sensorModelSettingsPath)

                modelName = eval(config['settingsModel']['modelName'])
                sensorName = modelName
                dataSeparator = eval(config['settingsModel']['dataSeparator'])
                numberOfRowsToSkip = eval(
                    config['settingsModel']['numberOfRowsToSkip'])
                timeColumnFormat = eval(
                    config['settingsModel']['timeColumnFormat'])
                timeColumnName = eval(
                    config['settingsModel']['timeColumnName'])
                plotColumn = eval(config['settingsModel']['plotColumn'])

                headerList = eval(config['settingsModel']['headerList'])
                exportHeaderList = eval(
                    config['settingsModel']['exportHeaderList'])
                unitsOfColumnsDictionary = eval(
                    config['settingsModel']['unitsOfColumnsDictionary'])

                # if Time Format is 'Origin', dateTimeOrigin and timeIntervalUnitsString must be valid inputs
                if timeColumnFormat in ['Origin']:
                    timeIntervalUnitsString = eval(
                        config['settingsModel']['timeIntervalUnitsString'])
                    dateTimeOrigin = eval(
                        config['settingsModel']['dateTimeOrigin'])
                    if dateTimeOrigin == 'creationDayOfFile':
                        dateTimeOrigin = pd.to_datetime(datetime.fromtimestamp(
                            os.path.getctime(sensorDataPathString)).strftime('%d-%m-%Y %H:%M:%S'))
                    elif dateTimeOrigin == 'modificationDayOfFile':
                        dateTimeOrigin = pd.to_datetime(datetime.fromtimestamp(
                            os.path.getmtime(sensorDataPathString)).strftime('%d-%m-%Y %H:%M:%S'))
                    else:
                        dateTimeOrigin = pd.to_datetime(dateTimeOrigin)
                else:
                    # Use default values
                    timeIntervalUnitsString = 'D'
                    dateTimeOrigin = pd.to_datetime('1900/01/01')

                print(
                    f"Reading #{sensorsCounted}: Sensor {sensorIndex_N+1}, model {modelName}.", file=sys.stderr)
                print(
                    f">> {os.path.basename(os.path.normpath(sensorDataPathString))}", file=sys.stderr)

                # create new dataframe if reading list of datasets, to append them (stack vertically)
                dfAllEventsOfOneSensor = sensor_df.sensor_df(pd.DataFrame())

                # * means all if need specific format then *.csv, or specific file start then <File Start>*
                sensorDataFilesList = glob.glob(sensorDataPathString)

                for sensorDataFile in sensorDataFilesList:
                    print(
                        f"- {os.path.basename(os.path.normpath(sensorDataFile))}", file=sys.stderr)
                    try:
                        # Crate Sensor Object with given parameters
                        sensorObject = sensor.Sensor(sensorName, modelName, sensorDataFile,
                                                     headerList=headerList, exportHeaderList=exportHeaderList,
                                                     unitsOfColumnsDictionary=unitsOfColumnsDictionary,
                                                     timeColumnName=timeColumnName, timeColumnFormat=timeColumnFormat,
                                                     dataSeparator=dataSeparator, numberOfRowsToSkip=numberOfRowsToSkip,
                                                     plotColumn=plotColumn,
                                                     timeIntervalUnitsString=timeIntervalUnitsString,
                                                     dateTimeOrigin=dateTimeOrigin)
                    except:
                        print(f'\n{"":#^30}\n', file=sys.stderr)
                        print('Something went wrong when reading. Maybe check paths?',
                              file=sys.stderr)
                        print(f'This is the current path: {sensorDataPathString}',
                              file=sys.stderr)
                        print(
                            f'And this is what glob.glob found (check if not empty): {sensorDataFilesList}',
                            file=sys.stderr)
                        print(f'\n{"":#^30}\n', file=sys.stderr)

                    sensorObject = CheckPreScripts(sensorObject)
                    # Calculate averages of export signals:
                    if args.CSV:  # if CSV file is provided
                        try:
                            dfIntervalsToExport = calculateIntervalsAsDefinedInCSVFile(
                                args.CSV, sensorObject.df1, column=sensorObject.signalsForExport)
                        except:
                            print(f'\n{"":#^30}\n', file=sys.stderr)
                            print(
                                f"Error when reading sensor data subsets according to provided CSV file.", file=sys.stderr)
                            print(f'\n{"":#^30}\n', file=sys.stderr)
                    else:  # as config.ini or arguments given
                        dfIntervalsToExport = calculateIntervals(
                            sensorObject.df1, freq=outputInterval, mode=outputIntervalUnits, column=sensorObject.signalsForExport, decimals=9)

                    # Calibrations and custom Scripts after average
                    if len(dfIntervalsToExport) > 0:
                        sensorObject.df2 = sensor_df.sensor_df(
                            dfIntervalsToExport.copy())
                        # sensorObject.df2 = CheckPostScripts(sensor_df.sensor_df(dfIntervalsToExport.copy()), modelName=modelName)
                        sensorObject = CheckPostScripts(sensorObject)

                        # # Make 1 Graph, defined per plotColumn
                        if (sensorObject.df2.df.columns.values.tolist().count(sensorObject.plotColumn) > 0):
                            yDataToPlot = sensorObject.df2.df[sensorObject.plotColumn]
                            plotTitle = f"Sensor: {modelName}"
                            if len(yDataToPlot) > 0:
                                if sensorObject.unitsOfColumnsDictionary != None:
                                    createSimplePlot(yDataToPlot, yunits=sensorObject.unitsOfColumnsDictionary.get(
                                        sensorObject.plotColumn, ''), title=plotTitle, yTitle=str(sensorObject.plotColumn))
                                else:
                                    createSimplePlot(yDataToPlot, yunits='', title=plotTitle, yTitle=str(
                                        sensorObject.plotColumn))

                        if isFilledFirstForwardThenBackward and isFilledForward:
                            sensorObject.df2.df = sensorObject.df2.df.ffill()

                        if isFilledBackward:
                            sensorObject.df2.df = sensorObject.df2.df.backfill()

                        if (not isFilledFirstForwardThenBackward) and isFilledForward:
                            sensorObject.df2.df = sensorObject.df2.df.ffill()

                        # Join Dataframes and stack vertically
                        dfAllEventsOfOneSensor = sensor_df.sensor_df(pd.concat(
                            [dfAllEventsOfOneSensor.df, sensorObject.df2.df]).sort_values('end'))

                    # # Clear Memory
                    del (dfIntervalsToExport)
                    del (sensorObject)

                # # Remove time columns with 'start' timestamps.
                dfAllEventsOfOneSensor.removeColumnFromDf('start')

                # Retrieve Header
                sensorHeaderList = dfAllEventsOfOneSensor.df.columns.values.tolist()

                # # Format Header
                new_cols_to_add = headerFormatter(
                    sensorHeaderList) if isOutputHeaderFormatted else sensorHeaderList

                for str_indx, str_value in enumerate(new_cols_to_add):
                    new_cols_to_add[str_indx] = f'{modelName}_'.replace(
                        '-', '_') + str_value
                    exportHeaderListRenamed.append(new_cols_to_add[str_indx])

                try:
                    # # Join Dataframes and stack horizontally
                    dfAllEventsOfAllSensors = sensor_df.sensor_df(dfAllEventsOfAllSensors.df.join(
                        dfAllEventsOfOneSensor.df, rsuffix=f'_{modelName}', how='outer').sort_values('end'))
                except:
                    print(f'\n{"":#^30}\n', file=sys.stderr)
                    print('Something went wrong at joining dataframes.\nMaybe check paths first?\n',
                          file=sys.stderr)
                    print(f'This is the current path: {sensorDataPathString}',
                          file=sys.stderr)
                    print(
                        f'And this is what glob.glob found: {sensorDataFilesList}',
                        file=sys.stderr)
                    print(f'{"":-^15}', file=sys.stderr)
                    print(
                        f'The left-hand side Dataframe header is:\n{dfAllEventsOfAllSensors.df.head()}',
                        file=sys.stderr)
                    print(f'{"":-^15}', file=sys.stderr)
                    print(
                        f'And the RHS Dataframe header is:\n{dfAllEventsOfOneSensor.df.head()}',
                        file=sys.stderr)
                    print(f'{"":-^15}', file=sys.stderr)
                    if args.CSV:
                        print(
                            'If you provided an .CSV file, make sure your data is within the specified start and end dates.')
                        print(args.CSV)
                    print(f'\n{"":#^30}\n', file=sys.stderr)

                # # Clear Memory of one sensor
                del (dfAllEventsOfOneSensor)

        # drop duplicate entries at the end if there are any
        dfAllEventsOfAllSensors.df = dfAllEventsOfAllSensors.df.drop_duplicates()

        if not os.path.exists(os.path.dirname(exportCompletePathString)):
            print(f'{"":#^5}')
            print(
                f'WARNING: Directory doest not exist, attempting to create {exportCompletePathString} ...')
            try:
                os.makedirs(exportCompletePathString)
            except:
                print(f'Could not create directory.')

        # # Save exports
        dfAllEventsOfAllSensors.df.to_csv(exportCompletePathString, sep=';',
                                          header=exportHeaderListRenamed,
                                          na_rep=0,
                                          quotechar='#')

        # =============================================================================
        #         # # Calculate Allan Deviation of a signal (created for ComPAS Data... need to be adjusted manually for your own data):
        #         #
        #         # if outputIntervalUnits == 'sec':
        #         #     rates = outputInterval
        #         # elif outputIntervalUnits == 'min':
        #         #     rates = outputInterval*60
        #         # else:
        #         #     rates = outputInterval*60*24
        #
        #         # data_all = dfAllEventsOfAllSensors.df['R1 [uPa]'].tolist()
        #         # (taus_out_all, ad_all, ade_all, adn_all) = allantools.oadev(data_all, rate=1.0/rates, data_type="freq", taus="all")
        #         # allan_df_all = pd.DataFrame({'Taus_min_all': taus_out_all/60, 'ad_all': ad_all, 'ad_error_all': ade_all, 'ad_number_all': adn_all})
        #         # allan_df_all.to_csv(file_export_path, sep=';', na_rep=0, quotechar='#')
        #
        # =============================================================================

        # Options exportStartDate and exportEndDate are defined:
        if exportStartDate != None and exportEndDate != None:
            # # Save time subset of export
            dfSubEventsOfAllSensors = dfAllEventsOfAllSensors.getDfSubset(
                exportStartPandaDateTime, exportEndPandaDateTime)

            dfSubEventsOfAllSensors.to_csv(os.path.join(exportBasePathString, f'{exportFileNameString}_{outputInterval}{outputIntervalUnits}__{exportStartDate}__{exportEndDate}.csv'),
                                           sep=';',
                                           header=exportHeaderListRenamed, na_rep=0, quotechar='#')

            # # Clear Memory
            del (dfSubEventsOfAllSensors)

        # Option areAdditionalFilesExportedForEachDay is True:
        if areAdditionalFilesExportedForEachDay and exportStartDate != None and exportEndDate != None:
            exportStartPandaDate = pd.to_datetime(
                exportStartDate, format='%Y-%m-%d')
            exportEndPandaDate = pd.to_datetime(
                exportEndDate, format='%Y-%m-%d')

            # Initial Values
            exportStartPandaDate_N = exportStartPandaDate
            dayCounterN = 0

            while exportStartPandaDate_N < exportEndPandaDate:
                exportStartPandaDate_N = exportStartPandaDate + \
                    timedelta(days=dayCounterN)
                exportEndPandaDate_N = exportStartPandaDate + \
                    timedelta(days=dayCounterN+1)

                exportStartDateString_N = exportStartPandaDate_N.strftime(
                    '%Y-%m-%d')
                exportEndDateString_N = exportEndPandaDate_N.strftime(
                    '%Y-%m-%d')

                # # Save Time Subset of exports
                dfSubEventsOfAllSensors = dfAllEventsOfAllSensors.getDfSubset(
                    exportStartPandaDate_N, exportEndPandaDate_N).copy()

                if len(dfSubEventsOfAllSensors) > 0:
                    dfSubEventsOfAllSensors.to_csv(os.path.join(exportBasePathString,
                                                                f'_{outputInterval}{outputIntervalUnits}__{exportStartDateString_N}__{exportEndDateString_N}.csv'), sep=';',
                                                   headerList=exportHeaderListRenamed,
                                                   na_rep=0,
                                                   quotechar='#')
                # # Clear Memory
                del (dfSubEventsOfAllSensors)
                # # Count Days
                dayCounterN += 1

        # # Clear Memory
        del (dfAllEventsOfAllSensors)

        print(f'{"":-^36}', file=sys.stderr)
        print('Synchronization complete.', file=sys.stderr)
        # print("\nAccess merged dataframe with dfAllEventsOfAllSensors.<>,\nor see documentation with help(dfAllEventsOfAllSensors)\nor clear memory with del(dfAllEventsOfAllSensors).", file=sys.stderr)

    else:
        print('Aborted.')

    dateTimeEnd = datetime.now()
    print(f'{"":-^36}', file=sys.stderr)
    print('Done. Code executed in', dateTimeEnd -
          dateTimeStart, file=sys.stderr)
    print(f'{"":-^36}', file=sys.stderr)
