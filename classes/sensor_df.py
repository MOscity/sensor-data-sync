from lib import pd


class sensor_df(object):
    def __init__(self, df=pd.DataFrame()):
        """Initialize sensor dataframe object.

        # =============================================================================
        Attributes:
        # =============================================================================
            self.df :               panda dataframe with extended functions

        # =============================================================================
        Inputs:
        # =============================================================================
            df :                    Any panda dataframe (pd.DataFrame(...))
       # =============================================================================   
        """
        self.df = df

    def getDfSubset(self, start, end, columnsToExport=-1):
        """returns the panda dataframe subset of the given columns.
            start = start datetime (pd.to_datetime)
            end = end datetime (pd.to_datetime)
            columnsToExport = columns to export (list of str)
                        -1 = all columns (default)"""
        if columnsToExport == -1:
            existingColumnNamesList = self.df.columns.values.tolist().copy()
        elif columnsToExport == None:
            existingColumnNamesList = self.df.columns.values.tolist().copy()
        else:
            existingColumnNamesList = []
            for index, value in enumerate(self.df.columns.values):
                if columnsToExport.count(value) > 0:
                    existingColumnNamesList.append(value)
            # [f(x) if condition else g(x) for x in sequence]

        # startTime = pd.to_datetime(start)
        # endTime = pd.to_datetime(end)
        # indexStart  = self.df.index[self.df.index.get_loc(startTime, method='nearest')]
        # indexEnd  = self.df.index[self.df.index.get_loc(endTime, method='nearest')]
        # # Produces Error: InvalidIndexError: Reindexing only valid with uniquely valued Index objects
        # print(indexStart,indexEnd)

        return self.df.loc[pd.to_datetime(start):pd.to_datetime(end), existingColumnNamesList]

    def dropDuplicatesInDf(self, nameOfColumnToCheck):
        """Drops duplicate entries in the given column in this dataframe.
            nameOfColumnToCheck = name of column to check for duplicates"""
        self.df = self.df.drop_duplicates(nameOfColumnToCheck)

    def linearModifyDf(self, columnName, A, B):
        """Linear modification of the given column in this dataframe.
            columnName = column to modify (str)
            newColumn[i] = A*col[i]+B"""
        columnNamesList = self.df.columns.values.tolist().copy()
        if columnNamesList.count(columnName) > 0:
            self.df[columnName] = A*self.df[columnName].astype(float)+B
        else:
            raise Exception(
                "There is no column named {col}".format(col=columnName))
        del (columnNamesList)

    def NPolynomialModifyDf(self, columnName, coefficientsList=[0, 1]):
        """Polynomial modification of the given column in this dataframe.
            columnName = column to modify (str)
            coefficientsList = list of coefficients in ascending order; 
            or simply = a_n for n = 0, 1, 2, ...
                    e.g. coefficientsList=[0,1] for Linear Modification 1*x+0
            newColumn[i] = a[n]*col[i]**n + a[n-1]*col[i]**(n-1) + ... 
            ... + a[1]*col[i] + a[0]"""
        columnNamesList = self.df.columns.values.tolist().copy()
        if columnNamesList.count(columnName) > 0:
            self.df['NPolynomialColumnTemporary'] = coefficientsList[0]
            for power, coefficient in enumerate(coefficientsList):
                self.df['NPolynomialColumnTemporary'] += coefficient * \
                    self.df[columnName].astype(float)**power
            self.df[columnName] = self.df['NPolynomialColumnTemporary']
            self.df.pop('NPolynomialColumnTemporary')
        else:
            raise Exception(
                "There is no column named {col}".format(col=columnName))
        del (columnNamesList)

    def addSubsetToDf(self, otherDf, newColumnNameList=None):
        """Adds a dataframe (to the right) to this dataframe.
            otherDf = dataframe to join (panda dataframe)
            newColumnNameList = new column name (list of str)"""
        if newColumnNameList != None:
            otherDf.columns = newColumnNameList

        self.df = self.df.join(otherDf)

    def renameColumnInDf(self, oldColumnName, newColumnName):
        """Rename a column of this dataframe, if present.
            oldColumnName = column/signal to modify (str)
            newColumnName = new name (str)"""
        columnNamesList = self.df.columns.values.tolist().copy()
        if columnNamesList.count(oldColumnName) > 0:
            indexOfOldColumnInDf = columnNamesList.index(oldColumnName)
            columnNamesList[indexOfOldColumnInDf] = newColumnName
        self.df.columns = columnNamesList

    def removeColumnFromDf(self, columnNameToRemoveListOrString):
        """Removes the given column in this dataframe, if present.
            columnNameToRemoveListOrString = column name (str or list of str)"""
        if len(self.df) > 0:
            if type(columnNameToRemoveListOrString) == list:
                for index, value in enumerate(columnNameToRemoveListOrString):
                    if len(self.df.get(value, [])) > 0:
                        self.df.pop(value)
            elif len(self.df.get(columnNameToRemoveListOrString, [])) > 0:
                self.df.pop(columnNameToRemoveListOrString)

    def checkForBadWordsInDf(self, badWord, columnName, startIndexOffset=0, endIndexOffset=0):
        """Removes all rows which contain 'badWord' from this dataframe by checking all elements of column.
            badWord = word to search in column
            columnName = column name (string)
            startIndexOffset = start row index (optional)
            endIndexOffset = end row index (optional)"""
        hasOccured = False
        for k in range(startIndexOffset, len(self.df[columnName])-endIndexOffset):
            if type(self.df[columnName][k]) == str:
                # .find('') returns -1 if not found.
                if self.df[columnName][k].find(badWord) >= 0:
                    print(
                        'Warning: Removed row {rowK} due to corrupt data'.format(rowK=k))
                    hasOccured = True
                    self.df.drop(labels=k, axis=0, inplace=True)
        return hasOccured

    def removeEmptyColumnsInDf(self):
        """Removes all columns with only NaN-values from this dataframe.
            """
        columnNamesList = self.df.columns.values.tolist().copy()
        for index, columnName in enumerate(columnNamesList):
            if self.df[columnName].isnull().all() == True:
                print(
                    'Warning: Removed empty column "{column}"'.format(column=columnName))
                self.removeColumnFromDf(columnName)
