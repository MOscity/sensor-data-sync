import lib
from lib import sys, os, glob, configparser, argparse
from lib import pd, datetime, timedelta, allantools, np

from classes import sensor_df, Sensor
from functions import calculateIntervals, calculateIntervalsAsDefinedInCSVFile, createSimplePlot, createInitFileFromDictionary, headerFormatter
from scripts import CheckPostScripts, CheckPreScripts


def initNewSensor():
    print('New Sensor:\t\t',
          isSensorNewInitialized, file=sys.stderr)

    print('Initializing new sensor data...', file=sys.stderr)
    sensorName = 'mySensor'

    print("Reading {sensorName} data, model {sensorModelName}.".format(
        sensorName=sensorName, sensorModelName=newSensorModelName), file=sys.stderr)

    # if Time Format is 'Origin', dateTimeOrigin and timeIntervalUnitsString must be valid inputs
    if formatStyleOfTimeColumnInNewSensorData in ['Origin']:
        timeIntervalUnitsStringNewSensor = eval(
            config['settingsInit']['timeIntervalUnitsStringNewSensor'])
        dateTimeOriginNewSensor = eval(
            config['settingsInit']['dateTimeOriginNewSensor'])

        if dateTimeOriginNewSensor == 'creationDayOfFile':
            dateTimeOriginNewSensor = pd.to_datetime(datetime.fromtimestamp(
                os.path.getctime(newSensorDataCompletePathString)).strftime('%d-%m-%Y %H:%M:%S'))
        elif dateTimeOriginNewSensor == 'modificationDayOfFile':
            dateTimeOriginNewSensor = pd.to_datetime(datetime.fromtimestamp(
                os.path.getmtime(newSensorDataCompletePathString)).strftime('%d-%m-%Y %H:%M:%S'))
        else:
            dateTimeOriginNewSensor = pd.to_datetime(
                dateTimeOriginNewSensor)
    else:
        # Use default values
        timeIntervalUnitsStringNewSensor = 'D'
        dateTimeOriginNewSensor = pd.to_datetime('1900/01/01')

    # Create sensor object and read data
    mySensor = Sensor(sensorName,
                      newSensorModelName,
                      newSensorDataCompletePathString,
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
    relativeFilePathOfInit = "models_settings/{NewModel}_settings.ini".format(
        NewModel=newSensorModelName)
    createInitFileFromDictionary(
        relativeFilePathOfInit, newInitDictionary)

    print('------', file=sys.stderr)
    print('Initialization complete.', file=sys.stderr)
    print('------', file=sys.stderr)
    print("Saved settings .ini file for model {sensorModelName} in:\n>>{fpath}".format(
        sensorModelName=newSensorModelName, fpath=defaultDirectoryOfThisScript+'/ \n'+relativeFilePathOfInit), file=sys.stderr)
    print("\nAccess sensor object functions with mySensor.<>,\nor see documentation with help(mySensor)\nor clear memory with del(mySensor).", file=sys.stderr)

    # Clear Memory
    # del(mySensor)


def exportData():
    # drop duplicate entries at the end
    dfAllEventsOfAllSensors.df = dfAllEventsOfAllSensors.df.drop_duplicates()

    # # Save exports
    dfAllEventsOfAllSensors.df.to_csv(exportCompletePathString, sep=';',
                                      header=exportHeaderListRenamed, na_rep=0, quotechar='#')

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
    #         # allan_df_all.to_csv(exportDirectoryPathString+'/'+exportFileNameString+'_{freq}{mode}__AllanDeviation_All.csv'.format(freq=outputInterval,mode=outputIntervalUnits), sep=';', na_rep=0, quotechar='#')
    #
    # =============================================================================

    # Options exportStartDate and exportEndDate are defined:
    if exportStartDate != None and exportEndDate != None:
        # # Save time subset of export
        dfSubEventsOfAllSensors = dfAllEventsOfAllSensors.getDfSubset(
            exportStartPandaDateTime, exportEndPandaDateTime)
        dfSubEventsOfAllSensors.to_csv(exportDailyCompletePathString, sep=';',
                                       header=exportHeaderListRenamed, na_rep=0, quotechar='#')

        # # Clear Memory
        del (dfSubEventsOfAllSensors)

    # Option areAdditionalFilesExportedForEachDay is True:
    if areAdditionalFilesExportedForEachDay and exportStartDate != None and exportEndDate != None:
        exportStartPandaDate = pd.to_datetime(
            exportStartDate, format='%Y-%m-%d')
        exportEndPandaDate = pd.to_datetime(
            exportEndDate, format='%Y-%m-%d')
        exportStartPandaDateN = exportStartPandaDate

        dayCounterN = 0
        while exportStartPandaDateN < exportEndPandaDate:
            exportStartPandaDateN = exportStartPandaDate + \
                timedelta(days=dayCounterN)
            exportEndPandaDate_N = exportStartPandaDate + \
                timedelta(days=dayCounterN+1)

            exportStartDateStringN = exportStartPandaDateN.strftime(
                '%Y-%m-%d')
            exportEndDateStringN = exportEndPandaDate_N.strftime(
                '%Y-%m-%d')

            exportDayNCompletePathString = exportBasePathString + '_{freq}{mode}__{start}__{end}.csv'.format(
                freq=outputInterval, mode=outputIntervalUnits, start=exportStartDateStringN, end=exportEndDateStringN)

            # # Save Time Subset of exports
            dfSubEventsOfAllSensors = dfAllEventsOfAllSensors.getDfSubset(
                exportStartPandaDateN, exportEndPandaDate_N)
            if len(dfSubEventsOfAllSensors) > 0:
                dfSubEventsOfAllSensors.to_csv(exportDayNCompletePathString, sep=';',
                                               headerList=exportHeaderListRenamed, na_rep=0, quotechar='#')

            # # Clear Memory
            del (dfSubEventsOfAllSensors)

            # # Count Days
            dayCounterN += 1

    # # Clear Memory
    # del(dfAllEventsOfAllSensors)


# MAIN
if __name__ == "__main__":
    # Time Performance Check
    dateTimeStart = datetime.now()

    # Default directory of the script
    defaultDirectoryOfThisScript = os.path.abspath(
        os.path.abspath(os.path.dirname(sys.argv[0]))) + "/"

    # Default path to config.ini file
    configFilePath = defaultDirectoryOfThisScript + \
        "config_9_ComPAS_CPC_Partektor.ini"

    # Arguments
    parser = argparse.ArgumentParser(description='Sensors utilities')
    parser.add_argument('--inifile', required=False, dest='INI', default=configFilePath,
                        help="Path to configuration(.ini) file ({} if omitted)".format(configFilePath))

    parser.add_argument('--intervals', required=False, dest='CSV', type=argparse.FileType('r'),
                        help='csv file with start and end timestamps columns. '
                        'First row must be the column names (i.e. "start" and "end"). '
                        'Uses intervals as defined in config.ini if this argument is '
                        'not provided. Uses 10 minute intervals if this argument is '
                        'missing and config.ini is missing too.')

    args = parser.parse_args()

    # Check which configuration file was provided
    configFilePath = args.INI

    # maybe there is a better name for this variable...
    listOfSensorUsageBools = []
    sensorDataPathsList = []
    sensorModelSettingsPathsList = []

    # Change numberOfMaxSensors if you need more then 10 sensors, and then add accordingly new lines for
    # data paths, settings path, use_sensor_i, etc. in config.ini (see pattern of the first 10 sensors).
    numberOfMaxSensors = 10

    config = configparser.ConfigParser()

    if os.path.exists(configFilePath):
        config.read(configFilePath)

        # settingsInit
        isSensorNewInitialized = eval(
            config['settingsInit']['isSensorNewInitialized'])
        newSensorModelName = eval(config['settingsInit']['newSensorModelName'])

        newSensorDataCompletePathString = eval(config['settingsInit']['newSensorDataDirectoryPathString']) + '/' + eval(
            config['settingsInit']['newSensorDataFileNameString'])
        numberOfRowsToSkipInNewSensorData = eval(
            config['settingsInit']['numberOfRowsToSkipInNewSensorData'])
        nameOfTimeColumnInNewSensorData = eval(
            config['settingsInit']['nameOfTimeColumnInNewSensorData'])
        formatStyleOfTimeColumnInNewSensorData = eval(
            config['settingsInit']['formatStyleOfTimeColumnInNewSensorData'])
        dataSeparatorInNewSensorData = eval(
            config['settingsInit']['dataSeparatorInNewSensorData'])

        # settingsOutput
        outputInterval = eval(config['settingsOutput']['outputInterval'])
        outputIntervalUnits = eval(
            config['settingsOutput']['outputIntervalUnits'])

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

        exportDirectoryPathString = eval(
            config['settingsOutput']['exportDirectoryPathString'])
        exportFileNameString = eval(
            config['settingsOutput']['exportFileNameString'])
        exportBasePathString = exportDirectoryPathString + '/' + exportFileNameString

        exportCompletePathString = exportBasePathString + \
            '_{freq}{mode}.csv'.format(
                freq=outputInterval, mode=outputIntervalUnits)
        if exportStartDate != None and exportEndDate != None:
            exportStartPandaDateTime = pd.to_datetime(
                exportStartDate, format='%d.%m.%Y')
            exportEndPandaDateTime = pd.to_datetime(
                exportEndDate, format='%d.%m.%Y')
            exportStartDate = exportStartPandaDateTime.strftime('%Y-%m-%d')
            exportEndDate = exportEndPandaDateTime.strftime('%Y-%m-%d')
            exportDailyCompletePathString = exportBasePathString + '_{freq}{mode}__{start}__{end}.csv'.format(
                freq=outputInterval, mode=outputIntervalUnits, start=exportStartDate, end=exportEndDate)

        # settingsGeneral and settingsOutput
        for k in range(1, numberOfMaxSensors+1):
            listOfSensorUsageBools.append(
                eval(config['settingsOutput']['isSensorProcessed_'+str(k)]))
            sensorDataPathsList.append(eval(config['settingsGeneral']['sensorDataDirectoryPathString_'+str(
                k)]) + '/' + eval(config['settingsGeneral']['sensorDataFileExtensionString_'+str(k)]))
            sensorModelSettingsPathsList.append(defaultDirectoryOfThisScript + eval(
                config['settingsGeneral']['sensorModelSettingsRelativePathString_'+str(k)]))

    else:  # Assume default values
        print('Could not find the configuration file {0}'.format(
            configFilePath), file=sys.stderr)

        # settingsInit
        isSensorNewInitialized = False

        # settingsOutput
        outputInterval = 10
        outputIntervalUnits = 'min'

        isFilledForward = True
        isFilledBackward = True
        isFilledFirstForwardThenBackward = True

        isOutputHeaderFormatted = True

        exportStartDate = None
        exportEndDate = None
        areAdditionalFilesExportedForEachDay = False

        exportCompletePathString = defaultDirectoryOfThisScript + \
            'output/Sample_Average_out_{freq}{mode}.csv'.format(
                freq=outputInterval, mode=outputIntervalUnits)

        # settingsGeneral and settingsOutput
        sensorDataPathAETH = defaultDirectoryOfThisScript + 'sample_datas/AE33_sample.dat'
        sensorDataPathPMS = defaultDirectoryOfThisScript + 'sample_datas/PMS1_sample.csv'
        sensorDataPathComPAS = defaultDirectoryOfThisScript + \
            'sample_datas/ComPASV4_sample.txt'
        sensorDataPathSMPS = defaultDirectoryOfThisScript + \
            'sample_datas/SMPS3080_Export_sample.csv'
        sensorDataPathMSPTI = defaultDirectoryOfThisScript + \
            'sample_datas/MSPTI_Metas_Export_sample.csv'
        sensorDataPathMiniPTI = defaultDirectoryOfThisScript + \
            'sample_datas/miniPTI_Export_sample.csv'

        sensorModelSettingsPathAETH = defaultDirectoryOfThisScript + \
            'models_settings/AE33_settings.ini'
        sensorModelSettingsPathPMS = defaultDirectoryOfThisScript + \
            'models_settings/PMSChinaSensor_settings.ini'
        sensorModelSettingsPathComPAS = defaultDirectoryOfThisScript + \
            'models_settings/ComPAS-V4_settings.ini'
        sensorModelSettingsPathSMPS = defaultDirectoryOfThisScript + \
            'models_settings/SMPS3080_Export_Settings.ini'
        sensorModelSettingsPathMSPTI = defaultDirectoryOfThisScript + \
            'models_settings/MSPTI_Metas_settings.ini'
        sensorModelSettingsPathMINIPTI = defaultDirectoryOfThisScript + \
            'models_settings/miniPTI_settings.ini'

        listOfSensorUsageBools = [True, True, True, True, True, True]
        sensorDataPathsList = [sensorDataPathAETH, sensorDataPathPMS, sensorDataPathComPAS,
                               sensorDataPathSMPS, sensorDataPathMSPTI, sensorDataPathMiniPTI]
        sensorModelSettingsPathsList = [sensorModelSettingsPathAETH, sensorModelSettingsPathPMS, sensorModelSettingsPathComPAS,
                                        sensorModelSettingsPathSMPS, sensorModelSettingsPathMSPTI, sensorModelSettingsPathMINIPTI]

        for k in range(7, numberOfMaxSensors+1):
            listOfSensorUsageBools.append(False)
            sensorDataPathsList.append(
                defaultDirectoryOfThisScript + 'model_settings/no_data.csv')
            sensorModelSettingsPathsList.append(
                defaultDirectoryOfThisScript + 'model_settings/no_settings.ini')

    # Initializiation Complete
    print('---------------------------------', file=sys.stderr)

    # if isSensorNewInitialized is true, skip averaging process etc.
    if isSensorNewInitialized:
        initNewSensor()

    # Else, process and synchronize
    else:
        print('Synchronizing data', file=sys.stderr)
        print('Units:\t\t\t\t', outputIntervalUnits, file=sys.stderr)
        print('Intervals:\t\t\t', outputInterval, file=sys.stderr)
        print('Forward Fill:\t\t', isFilledForward, file=sys.stderr)
        print('Back Fill:\t\t\t', isFilledBackward, file=sys.stderr)
        print('First Forward Fill?:',
              isFilledFirstForwardThenBackward, file=sys.stderr)
        print('Format Header:\t\t', isOutputHeaderFormatted, file=sys.stderr)
        print('---------------------------------', file=sys.stderr)

        for index, value in enumerate(listOfSensorUsageBools):
            print('Sensor {ind}:\t\t\t'.format(
                ind=index+1), value, file=sys.stderr)

        # create new dataframe to merge all datas in (stack horizontally)
        dfAllEventsOfAllSensors = sensor_df(pd.DataFrame())
        exportHeaderListRenamed = []

        # count the sensors used, for debug purpose
        sensorsCounted = 0

        for sensorNIsUsed, sensorIndexN in zip(listOfSensorUsageBools, range(len(listOfSensorUsageBools))):
            if sensorNIsUsed:
                sensorsCounted += 1
                print('------------------------', file=sys.stderr)

                # Get Data Files and Settings
                sensorDataPathString = sensorDataPathsList[sensorIndexN]
                sensorModelSettingsPath = sensorModelSettingsPathsList[sensorIndexN]

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

                print("Reading #{sensorsCounted}: Sensor {sensorIndexN}, model {sensorModelName}.".format(
                    sensorsCounted=sensorsCounted, sensorIndexN=sensorIndexN+1, sensorModelName=modelName), file=sys.stderr)
                indexOfSlash = len(sensorDataPathString) - \
                    sensorDataPathString[::-1].find('/')
                print(">> {dataPath}".format(
                    dataPath=sensorDataPathString[:indexOfSlash]), file=sys.stderr)

                # create new dataframe if reading list of datasets, to append them (stack vertically)
                dfAllEventsOfOneSensor = sensor_df(pd.DataFrame())

                # * means all if need specific format then *.csv, or specific file start then <File Start>*
                sensorDataFilesList = glob.glob(sensorDataPathString)

                for sensorDataFileIndex in range(len(sensorDataFilesList)):
                    # get final data file path, if sensorDataPathString was a list
                    sensorDataFile = sensorDataFilesList[sensorDataFileIndex]
                    indexOfSlash = len(sensorDataFile) - \
                        sensorDataFile[::-1].find('/')
                    print(
                        "- {data} ".format(data=sensorDataFile[indexOfSlash:]), file=sys.stderr)

                    # Crate Sensor Object with given parameters
                    sensorObject = Sensor(sensorName, modelName, sensorDataFile,
                                          headerList=headerList, exportHeaderList=exportHeaderList,
                                          unitsOfColumnsDictionary=unitsOfColumnsDictionary,
                                          timeColumnName=timeColumnName, timeColumnFormat=timeColumnFormat,
                                          dataSeparator=dataSeparator, numberOfRowsToSkip=numberOfRowsToSkip,
                                          plotColumn=plotColumn,
                                          timeIntervalUnitsString=timeIntervalUnitsString,
                                          dateTimeOrigin=dateTimeOrigin)

                    sensorObject = CheckPreScripts(sensorObject)
                    # Calculate averages of export signals:
                    if args.CSV:  # if CSV file is provided
                        dfIntervalsToExport = calculateIntervalsAsDefinedInCSVFile(
                            args.CSV, sensorObject.df1, column=sensorObject.signalsForExport)
                    else:  # as config.ini or arguments given
                        dfIntervalsToExport = calculateIntervals(
                            sensorObject.df1, freq=outputInterval, mode=outputIntervalUnits, column=sensorObject.signalsForExport, decimals=9)

                    # Calibrations and custom Scripts after average
                    if len(dfIntervalsToExport) > 0:
                        sensorObject.df2 = sensor_df(
                            dfIntervalsToExport.copy())
                        # sensorObject.df2 = CheckPostScripts(sensor_df(dfIntervalsToExport.copy()), modelName=modelName)
                        sensorObject = CheckPostScripts(sensorObject)

                        # # Make 1 Graph, defined per plotColumn
                        if (sensorObject.df2.df.columns.values.tolist().count(sensorObject.plotColumn) > 0):
                            yDataToPlot = sensorObject.df2.df[sensorObject.plotColumn]
                            plotTitle = "Sensor: {sensorModelName}".format(
                                sensorModelName=modelName)
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
                        dfAllEventsOfOneSensor = sensor_df(pd.concat(
                            [dfAllEventsOfOneSensor.df, sensorObject.df2.df]).sort_values('end'))

                    # # Clear Memory

                    del (dfIntervalsToExport)
                    del (sensorObject)

                # # Remove time columns with 'start' timestamps.
                dfAllEventsOfOneSensor.removeColumnFromDf('start')
                dfAllEventsOfAllSensors.removeColumnFromDf('start')

                # # Format Header
                if isOutputHeaderFormatted:
                    new_cols_to_add = headerFormatter(
                        dfAllEventsOfOneSensor.df.columns.values.tolist())
                else:
                    new_cols_to_add = dfAllEventsOfOneSensor.df.columns.values.tolist()

                for str_indx, str_value in enumerate(new_cols_to_add):
                    new_cols_to_add[str_indx] = '{}_'.format(
                        modelName).replace('-', '_') + str_value
                    exportHeaderListRenamed.append(new_cols_to_add[str_indx])

                # # Join Dataframes and stack horizontally
                dfAllEventsOfAllSensors = sensor_df(dfAllEventsOfAllSensors.df.join(
                    dfAllEventsOfOneSensor.df, rsuffix='_{}'.format(modelName), how='outer').sort_values('end'))

                # # If even more misssing data should be filled, uncomment this:
                # total_df = total_df.backfill()
                # total_df = total_df.ffill()

                # # Clear Memory
                del (dfAllEventsOfOneSensor)

        exportData()

        print('------', file=sys.stderr)
        print('Synchronization complete.', file=sys.stderr)
        print('------', file=sys.stderr)
        print("\nAccess merged dataframe with dfAllEventsOfAllSensors.<>,\nor see documentation with help(dfAllEventsOfAllSensors)\nor clear memory with del(dfAllEventsOfAllSensors).", file=sys.stderr)

    dateTimeEnd = datetime.now()
    print('------------------------', file=sys.stderr)
    print('Done. Code executed in', dateTimeEnd -
          dateTimeStart, file=sys.stderr)
