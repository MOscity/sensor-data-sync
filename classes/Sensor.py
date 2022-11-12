from lib import pd
from classes import sensor_df


def renameKeyInDict(oldDict, oldName, newColumnName):
    """Replaces a key in a dictionary and returns a new dictionary.
        The value of the key is not changed.
        oldDict = input dictionary
        oldName = name of old key
        newColumnName = new name for old keys
            returns new dictionary"""
    newDict = {}
    for key, value in oldDict.items():
        newKey = (key if key != oldName else newColumnName)
        newDict[newKey] = oldDict[key]
    return newDict


class Sensor(object):
    _dfMaxNumber = 3

    def __init__(self,
                 sensorName,
                 modelName,
                 dataFilePath,
                 headerList=None,
                 exportHeaderList=None,
                 unitsOfColumnsDictionary={},
                 timeColumnName=None,
                 timeColumnFormat=None,
                 quotechar='"',
                 dataSeparator=None,
                 numberOfRowsToSkip=0,
                 plotColumn='',
                 dateTimeOrigin=pd.to_datetime('1900/01/01'),
                 timeIntervalUnitsString='s'
                 ):
        """Initialize sensor object.

        # =============================================================================
        Attributes:
        # =============================================================================
            self.sensorName :             sensor name (str)

            self.modelName :                modelName (str), see "model"_settings.ini files
            self.dataPath :                 path to datafiles (str), see config.ini file
            self.df1,                       panda dataframe for all datas and all columns
            self.df2,                       panda dataframe for averaged datas and export columns
            self.df3 :                      empty dataframe
            self.signals :                  headerList list (overrides found headerList in file if provided)
            self.signalsForExport :            signals to export (from self.signals) (optional)
            self.unitsOfColumnsDictionary:  signal units dictionary for any/all elements of self.signals (optional)
            self.plotColumn :               signal to plot (one of self.signals) (optional)
        # =============================================================================  
        Inputs:
        # =============================================================================
            sensorName :                    Any name for your sensor (str)

            modelName :                     Model name of your sensor (str).
                                            Currently Fully Implemented: AE33, AE31, SMPS3080_Export, 
                                            ComPAS-V4, PMS1, MSPTI, miniPTI.
                                            Any other name can be used for initializing new datasets.

            dataFilePath :                  valid data path (str)

            headerList = [] :               Override headerList row with another list (length must match with columns). 
                                            If headerList is None, first row will be used as column names.

            exportHeaderList = [] :         list for signals to export.
                                            if exportHeaderList is None, exportHeaderList = headerList

            unitsOfColumnsDictionary = {}:  dictionary for units of signals.
                                            if unitsOfColumnsDictionary is None, a basic dictionary 
                                            from the headerList list is created with all units empty ''.

            timeColumnName = '' :           columnName with date time entries (str)
                                            if timeColumnFormat is set to 'DateTime_2Column', provide 2 column names 
                                            for date and time as a list, e.g. timeColumnName = ['Date','Time'].

            timeColumnFormat = '' :         'Excel', 'DateTime_1Column', 'DateTime_2Column', 'Origin' or
                                            'Format = <custom format>'. See below for examples.

            dataSeparator = '' :            separator in datafile, e.g ',', '\t', ';' 
                                            or None (=interpret file structure with python, default)

            numberOfRowsToSkip = 0 :        skip first N rows of datafile.

            plotColumn = '' :               ColumnName to plot. Default is last column.

            dateTimeOrigin = 0 :            If timeColumnFormat is set to 'Origin' define dateTimeOrigin and timeIntervalUnitsString:
                                            dateTimeOrigin: Define the reference date. The numeric values would be 
                                            parsed as number of units (defined by unit) since this reference date.
                                            If ‘unix’ (or POSIX) time; dateTimeOrigin is set to 1970-01-01.
                                            If ‘julian’, unit must be ‘D’, and dateTimeOrigin is set to beginning of 
                                            Julian Calendar. Julian day number 0 is assigned to the day starting 
                                            at noon on January 1, 4713 BC.
                                            If Timestamp convertible, dateTimeOrigin is set to Timestamp identified by dateTimeOrigin.   

            timeIntervalUnitsString = 's'   timeIntervalUnitsString: The unit of the arg (D,s,ms,us,ns) denote the unit, which 
                                            is an integer or float number. This will be based off the dateTimeOrigin. 
                                            Example, with unit=’ms’ and dateTimeOrigin=’unix’ (the default), this would 
                                            calculate the number of milliseconds to the unix epoch start.

            # Allowed Time Formats:
            # timeColumnFormat:             Examples:
            #
            # 'Excel'                       44543.44961
            #                               number representing days past since...
            #
            # 'DateTime_1Column'            16-12-2021 10:11:43, or 14.12.2021 10:05:28
            #                               Datetime will be infered from 1 column.
            #
            # 'DateTime_2Column'            2021/12/29 +{separator}+ 00:09:00
            #                               Datetime will be infered from 2 columns.
            #
            #
            # 'Format = ... '               for custom time format
            #                               e.g. %%d.%%m.%%Y %%H:%%M:%%S for 28.12.2021 15:44:02
            #                               Note: Use %% instead % in the .ini file.  
            #                               'Format = %%d.%%m.%%Y %%H:%%M:%%S' = 14.12.2021 10:05:28
            #                               'Format = %%d-%%m-%%Y %%H:%%M:%%S' = 16-12-2021 10:11:43
            #                               See also: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
            #                               https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
            #                        
            # 'dateTimeOrigin'              provide custom dateTimeOrigin with pandas datetime, 
            #                               e.g. pd.datetime('1900/01/01')
            #                               --> and also provide timeIntervalUnitsString in this case: 'D', 's'
            #                       
       # =============================================================================   
        """

        self.sensorName = sensorName
        self.modelName = modelName
        self.dataPath = dataFilePath

        headerListOut = headerList
        separatorOut = dataSeparator
        skiprowsOut = numberOfRowsToSkip

        # if headerList is not provided, first row will be used as headerList
        # else skip one more row
        if headerListOut != None:
            skiprowsOut += 1

        #headerExportListOut = exportHeaderList
        unitsOfColumnsDictionaryOut = unitsOfColumnsDictionary
        plotColumnOut = plotColumn

        # Init main sensor dataframe
        self.df1 = sensor_df.sensor_df(pd.read_csv(
            dataFilePath,                   # relative python path to subdirectory
            index_col=False,
            names=headerListOut,         # use names=None to infer column names
            sep=separatorOut,        # Space-separated value file.
            # quotechar = quotechar_out,  # double quote allowed as quote character
            skiprows=skiprowsOut,    # Skip the first X row of the file
            engine='python'           # allows to use sep=None to find separator
        ))

        # # Remove empty columns ... maybe dangerous to do...
        self.df1.removeEmptyColumnsInDf()
        self.df1.removeColumnFromDf(' ')
        self.df1.removeColumnFromDf('  ')
        self.df1.removeColumnFromDf('   ')

        # Init more sensor dataframes
        self.df2 = sensor_df.sensor_df(pd.DataFrame())
        self.df3 = sensor_df.sensor_df(pd.DataFrame())

        # If no headerList is provided, use first row as headerList
        if headerListOut == None:
            headerListOut = self.df1.df.columns.to_list().copy()

        # If a headerList is provided, check if type is list and if length matches with number of columns
        elif type(headerListOut) == list:
            currentHeaderLength = len(self.df1.df.columns.to_list().copy())
            if len(headerListOut) == currentHeaderLength:
                headerListOut = headerList
            else:
                raise Exception(
                    "Number of items in headerList list does not match with number of columns in dataframe.")
        else:
            raise Exception("Type of headerList has to be None or a list.")

        # If no export headerList is provided, use all columns
        if exportHeaderList == None:
            headerExportListOut = headerListOut.copy()
        elif type(headerListOut) == list:
            headerExportListOut = exportHeaderList
        else:
            raise Exception("Type of exportHeaderList has to be None or list.")

        # If no signal units are provided, create a dictionary with headerList as keys and empty values
        if unitsOfColumnsDictionary == None:
            unitsOfColumnsDictionaryOut = dict.fromkeys(headerListOut, '')
        # if dict is not None but empty ({}) we can access .items():
        elif len(unitsOfColumnsDictionaryOut.items()) == 0:
            unitsOfColumnsDictionaryOut = dict.fromkeys(headerListOut, '')

        # If no plotColumn is provided, use last column for plots

        if plotColumn == '':  # or headerListOut.count(plotColumn)==0:
            plotColumnOut = headerListOut[-1]
        # or if plotColumn is None
        elif plotColumn == None:
            plotColumnOut = headerListOut[-1]
        # or if plotColumn is not in signals list, use last column for plots
        elif headerListOut.count(plotColumn) == 0:
            print('There is no column named {plotKey}'.format(
                plotKey=plotColumn))
            plotColumnOut = headerListOut[-1]

        # If timeColumnName is None, use first column for timestamp.
        if timeColumnName == None:
            timeColumnNameOut = headerListOut[0]
            DateColumnNameOut = headerListOut[0]
        # elif timeColumnName is a list, check if has exactly 2 entries for 'Date' and 'Time'
        elif type(timeColumnName) == list:
            if len(timeColumnName) == 2:
                TimeColumnFormatOut = 'DateTime_2Column'
                DateColumnNameOut = timeColumnName[0]
                timeColumnNameOut = timeColumnName[1]
            else:
                raise Exception(
                    "Provide a list with 2 string entries for Date and Time, e.g. timeColumnName = ['Date','Time']")
        # elif timeColumnName is a string, just use it
        elif type(timeColumnName) == str:
            timeColumnNameOut = timeColumnName
            DateColumnNameOut = timeColumnName
        else:
            raise Exception(
                "Type of timeColumnName has to be None, list, or string.")

        # if timeColumnFormat is None, infer date time (see below)
        if timeColumnFormat == None:
            TimeColumnFormatOut = None
        # elif timeColumnFormat is a string, use it and check if it is 'DateTime_2Column'
        elif type(timeColumnFormat) == str:
            TimeColumnFormatOut = timeColumnFormat
            if timeColumnFormat == 'DateTime_2Column':
                # in this case, if type(timeColumnName)==str -> invalid input.
                if type(timeColumnName) == str:
                    raise Exception(
                        "If timeColumnFormat is set to {}, leave timeColumnName=None or provide a list with 2 entries for Date and Time, e.g. timeColumnName = ['Date','Time'] ".format(timeColumnFormat))
                # elif timeColumnName is None, assume first 2 columns are 'Date' and 'Time'
                elif timeColumnName == None:
                    DateColumnNameOut = headerListOut[0]
                    timeColumnNameOut = headerListOut[1]
                # elif timeColumnName is list with 2 entries, this case is already done.
        else:
            raise Exception(
                "Type of timeColumnFormat has to be None or string.")

        # Safety check if there is a row containing strings (i.e. header names) again:
        isCorrupted = self.df1.checkForBadWordsInDf(
            timeColumnNameOut, timeColumnNameOut, startIndexOffset=1)
        if isCorrupted:
            for key in headerListOut:
                if (key != timeColumnNameOut) or (key != DateColumnNameOut):
                    self.df1.df[key] = self.df1.df[key].astype(float)

        if TimeColumnFormatOut == None:  # if timeColumnFormat = None,: infer date time
            self.df1.df['Datetime'] = pd.to_datetime(
                self.df1.df[timeColumnNameOut], infer_datetime_format=True, utc=False)
        elif TimeColumnFormatOut in ['Excel']:
            # Datetime format is given from excel (example 44544.42951 is 2021-Dec-14. 10:18:29.664)
            self.df1.df['Datetime'] = pd.to_datetime(
                self.df1.df[timeColumnNameOut], unit='D', dateTimeOrigin=pd.to_datetime('1899/12/31'), utc=False)
            # self.df1.df['Datetime'] = pd.to_datetime(self.df1.df['Datetime'], utc=True) - pd.to_timedelta(2, unit='D') # subtract 2 additional days
        elif TimeColumnFormatOut[:24] in ['DateTime_CustomFormat = ']:
            self.df1.df['Datetime'] = pd.to_datetime(
                self.df1.df[timeColumnNameOut], infer_datetime_format=False, format=TimeColumnFormatOut[24:], utc=False)
        elif TimeColumnFormatOut in ['DateTime_2Column']:
            self.df1.df['Datetime'] = pd.to_datetime(
                self.df1.df[DateColumnNameOut] + " " + self.df1.df[timeColumnNameOut], infer_datetime_format=True, utc=False)
        elif TimeColumnFormatOut[:32] in ['DateTime_2Column_CustomFormat = ']:
            self.df1.df['Datetime'] = pd.to_datetime(
                self.df1.df[DateColumnNameOut] + " " + self.df1.df[timeColumnNameOut], infer_datetime_format=False, format=TimeColumnFormatOut[32:], utc=False)
        elif TimeColumnFormatOut in ['Origin']:
            self.df1.df['Datetime'] = pd.to_datetime(
                self.df1.df[timeColumnNameOut], unit=timeIntervalUnitsString, origin=dateTimeOrigin, utc=False)
        elif TimeColumnFormatOut[:9] == 'Format = ':
            self.df1.df['Datetime'] = pd.to_datetime(
                self.df1.df[timeColumnNameOut], infer_datetime_format=False, format=TimeColumnFormatOut[9:], utc=False)
        else:  # if 'DateTime_1Column' : infer date time
            self.df1.df['Datetime'] = pd.to_datetime(
                self.df1.df[timeColumnNameOut], infer_datetime_format=True, utc=False)

        self.df1.df = self.df1.df.set_index('Datetime')

        self.signals = headerListOut
        self.signalsForExport = headerExportListOut
        self.unitsOfColumnsDictionary = unitsOfColumnsDictionaryOut
        self.plotColumn = plotColumnOut

    def getDf(self, dfIndex=1):
        """returns the sensor_df of the selected dataframe.
            dfIndex = 1(=default), 2 or 3"""
        if dfIndex == 1:
            return self.df1
        elif dfIndex == 2:
            return self.df2
        elif dfIndex == 3:
            return self.df3
        else:
            return self.df1

    def getSubset(self, pandaDateTimeStart, pandaDateTimeEnd, columnNameString, dfIndex=1):
        """returns the sensor_df subset of the given columns and selected dataframes.
            pandaDateTimeStart = start datetime (pd.datetime)
            pandaDateTimeEnd = end datetime (pd.datetime)
            columnNameString = column to export (str)
            dfIndex = 1(=default), 2 or 3"""
        return self.getDf(dfIndex).getDfSubset(pandaDateTimeStart, pandaDateTimeEnd, columnNameString)

    def renameColumnInSensorDf(self, oldColumnNameString, newColumnNameString, newUnits=None, dfIndex=-1):
        """Rename a column/signal and all related attributes of a sensor_object.
            oldName = column/signal to modify (str)
            newColumnName = new name (str)
            newUnits = units of new column/signal (str)
            dfIndex = 1,2,3, or -1(=all, default)"""

        if dfIndex == -1:
            for i in range(self._dfMaxNumber):
                self.getDf(i+1).renameColumnInDf(oldColumnNameString,
                                                 newColumnNameString)
        elif type(dfIndex) == list:
            for index in dfIndex:
                self.getDf(index).renameColumnInDf(
                    oldColumnNameString, newColumnNameString)
        else:
            self.getDf(dfIndex).renameColumnInDf(
                oldColumnNameString, newColumnNameString)

        # Check in signals:
        newSignals = self.signals.copy()
        if newSignals.count(oldColumnNameString) > 0:
            indexOfOldSignal = newSignals.index(oldColumnNameString)
            newSignals[indexOfOldSignal] = newColumnNameString
        self.signals = newSignals

        # Check in signalsExport:
        newSignalsForExport = self.signalsForExport.copy()
        if newSignalsForExport.count(oldColumnNameString) > 0:
            indexOfOldSignalForExport = newSignalsForExport.index(
                oldColumnNameString)
            newSignalsForExport[indexOfOldSignalForExport] = newColumnNameString
        self.signalsForExport = newSignalsForExport

        # Check in unitsOfColumnsDictionary:
        newSignalsDictionary = self.unitsOfColumnsDictionary.copy()
        signalUnitNamesInDictionaryList = list(newSignalsDictionary.keys())
        if signalUnitNamesInDictionaryList.count(oldColumnNameString) > 0:
            if newUnits != None:
                newSignalsDictionary[oldColumnNameString] = newUnits
            self.unitsOfColumnsDictionary = renameKeyInDict(
                newSignalsDictionary, oldColumnNameString, newColumnNameString)

        # Check in plotColumn
        if self.plotColumn == oldColumnNameString:
            self.plotColumn = newColumnNameString

    def addSubset(self, otherDf, newColumnNames=None, newUnits=None, dfIndex=-1):
        """Adds a dataframe (to the right) to one/all sensor dataframes.
            otherDf = dataframe to join (panda dataframe)
            newColumnNames = new column names (list or string)
            newUnits = new units for sensor object
            dfIndex = 1,2,3, or -1(=all, default)
            """
        if newColumnNames == None:
            newColumnNames = otherDf.columns.values.tolist().copy()
        else:
            otherDf.columns = newColumnNames

        if newUnits == None:
            newUnits = ['' for k in range(len(newColumnNames))]

        if dfIndex == -1:
            for i in range(self._dfMaxNumber):
                self.getDf(i+1).df = self.getDf(i+1).df.join(otherDf)
        elif type(dfIndex) == list:
            for index in dfIndex:
                self.getDf(index).df = self.getDf(index).df.join(otherDf)
        else:
            self.getDf(dfIndex).df = self.getDf(dfIndex).df.join(otherDf)

        signalNames = self.signals.copy()
        exportSignalNames = self.signalsForExport.copy()
        unitsDictionary = self.unitsOfColumnsDictionary.copy()

        for index, otherDfColumnName in enumerate(otherDf.columns.values):
            signalNames.append(otherDfColumnName)
            exportSignalNames.append(otherDfColumnName)
            unitsDictionary.update({otherDfColumnName: newUnits[index]})

            self.unitsOfColumnsDictionary = unitsDictionary
            self.signals = signalNames
            self.signalsForExport = exportSignalNames

    def removeSubset(self, nameOfColumnToRemove, dfIndex=-1):
        """Removes the given column from one/all sensor dataframes.
            nameOfColumnToRemove = column name (string)
            dfIndex = 1,2,3, or -1(=all, default)"""

        newSignals = self.signals.copy()
        if newSignals.count(nameOfColumnToRemove) > 0:
            newSignals.remove(nameOfColumnToRemove)
        self.signals = newSignals

        newExportSignals = self.signalsForExport.copy()
        if newExportSignals.count(nameOfColumnToRemove) > 0:
            newExportSignals.remove(nameOfColumnToRemove)
        self.signalsForExport = newExportSignals

        newSignalsDictionary = self.unitsOfColumnsDictionary.copy()
        if len(newSignalsDictionary) > 0:
            if len(newSignalsDictionary.get(nameOfColumnToRemove, [])) > 0:
                newSignalsDictionary.pop(nameOfColumnToRemove)
        self.unitsOfColumnsDictionary = newSignalsDictionary

        if dfIndex == -1:
            for i in range(self._dfMaxNumber):
                self.getDf(i+1).removeColumnFromDf(nameOfColumnToRemove)
        elif type(dfIndex) == list:
            for ind in dfIndex:
                self.getDf(ind).removeColumnFromDf(nameOfColumnToRemove)
        else:
            self.getDf(dfIndex).removeColumnFromDf(nameOfColumnToRemove)

        # Check in plotColumn
        if self.plotColumn == nameOfColumnToRemove:
            self.plotColumn = self.signals[-1]

    def dropDuplicates(self, columnName, dfIndex=-1):
        """Drops duplicate entries in the given column in one/all sensor dataframes.
            column = column to check for duplicates
            dfIndex = 1,2,3, or -1(=all, default)"""
        if dfIndex == -1:
            for i in range(self._dfMaxNumber):
                self.getDf(i+1).dropDuplicatesInDf(columnName)
        elif type(dfIndex) == list:
            for ind in dfIndex:
                self.getDf(ind).dropDuplicatesInDf(columnName)
        else:
            self.getDf(dfIndex).dropDuplicatesInDf(columnName)

    def LinearModify(self, columnName, A, B, dfIndex=-1):
        """Linear modification of the given column in one/all sensor dataframes.
            columnName = column to modify (str)
                --> newColumn[i] = A*col[i]+B
            dfIndex = 1,2,3, or -1(=all, default)"""

        if dfIndex == -1:
            for i in range(self._dfMaxNumber):
                self.getDf(i+1).linearModifyDf(columnName, A, B)
        elif type(dfIndex) == list:
            for ind in dfIndex:
                self.getDf(ind).linearModifyDf(columnName, A, B)
        else:
            self.getDf(dfIndex).linearModifyDf(columnName, A, B)

    def NPolynomialModify(self, columnName, coefficientsList=[0, 1], dfIndex=-1):
        """N-polynomial modification of the given column in one/all sensor dataframes.
            columnName = column to modify (str)
            coefficientsList = list of coefficients in ascending order; 
            or simply = a_n for n = 0, 1, 2, ...
                    e.g. coefficientsList=[0,1] for Linear Modification 1*x+0
            newColumn[i] = a[n]*col[i]**n + a[n-1]*col[i]**(n-1) + ... 
            ... + a[1]*col[i] + a[0]
            dfIndex = 1,2,3, or -1(=all, default)"""

        if dfIndex == -1:
            for i in range(self._dfMaxNumber):
                self.getDf(i+1).NPolynomialModifyDf(columnName,
                                                    coefficientsList)
        elif type(dfIndex) == list:
            for ind in dfIndex:
                self.getDf(ind).NPolynomialModifyDf(
                    columnName, coefficientsList)
        else:
            self.getDf(dfIndex).NPolynomialModifyDf(
                columnName, coefficientsList)
