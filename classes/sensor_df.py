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
        Methods:
        # =============================================================================
            getDfSubset
            linearModifyDf    
            NPolynomialModifyDf  
            addSubsetToDf      
            renameColumnInDf
            removeColumnFromDf
            checkForBadWordsInDf
            removeEmptyColumnsInDf

        # =============================================================================   
        """
        self.df = df

    def getDfSubset(self, start, end, columnsToExport=-1):
        """returns the panda dataframe subset of the given columns.
            start = start datetime (pd.to_datetime)
            end = end datetime (pd.to_datetime)
            columnsToExport = columns to export (list of str)
                        -1 = all columns (default)"""
        if (columnsToExport == -1) or (columnsToExport == None):
            # No header given: copying current header
            existingColumnNamesList = self.df.columns.values.tolist().copy()
        else:
            # Check if names exist in the self.df Dataframe
            existingColumnNamesList = [value for index, value in enumerate(
                self.df.columns) if (columnsToExport.count(value) > 0)]

        return self.df.loc[pd.to_datetime(start):pd.to_datetime(end), existingColumnNamesList]

    def linearModifyDf(self, columnName, A, B):
        """Linear modification of the given column in this dataframe.
            columnName = column to modify (str)
            newColumn[i] = A*col[i]+B"""
        self.df[columnName] = self.df[columnName].transform(lambda x: A*x + B)

    def NPolynomialModifyDf(self, columnName, coefficientsList=[0, 1]):
        """Polynomial modification of the given column in this dataframe.
            columnName = column to modify (str)
            coefficientsList = list of coefficients in ascending order; 
            or simply = a_n for n = 0, 1, 2, ...
                    e.g. coefficientsList=[0,1] for Linear Modification 1*x+0
            newColumn[i] = a[n]*col[i]**n + a[n-1]*col[i]**(n-1) + ... 
            ... + a[1]*col[i] + a[0]"""
        def polyfunc(x):
            result = 0
            for power, coefficient in enumerate(coefficientsList):
                result += coefficient * x**power
            return result

        self.df[columnName] = self.df[columnName].transform(polyfunc)

    def addSubsetToDf(self, otherDf, newColumnNameList=None):
        """Adds a dataframe (to the right) to this dataframe.
            otherDf = dataframe to join (panda dataframe)
            newColumnNameList = new column name (list of str)"""
        if newColumnNameList != None:
            otherDf.columns = newColumnNameList

        self.df = self.df.join(otherDf)

    def renameColumnInDf(self, oldColumnNames, newColumnNames, raise_errors=True):
        """Rename a column of this dataframe, if present.
            oldColumnNames = columns/signals to modify (str or list)
            newColumnNames = new names (str or list)"""
        if type(oldColumnNames) == str:
            oldColumnNames = [oldColumnNames]
        if type(newColumnNames) == str:
            newColumnNames = [newColumnNames]
        namesDict = dict(zip(oldColumnNames, newColumnNames))

        self.df.rename(columns=namesDict, inplace=True,
                       errors='raise' if raise_errors else 'ignore')

    def removeColumnFromDf(self, columnNameToRemoveListOrString, raise_errors=True):
        """Removes the given column in this dataframe, if present.
            columnNameToRemoveListOrString = column name (str or list of str)"""
        self.df.drop(columnNameToRemoveListOrString,
                     inplace=True, axis=1, errors='raise' if raise_errors else 'ignore')

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
                    print(f'Warning: Removed row {k} due to corrupt data')
                    hasOccured = True
                    self.df.drop(labels=k, axis=0, inplace=True)
        return hasOccured

    def removeEmptyColumnsInDf(self):
        """Removes all columns with only NaN-values from this dataframe.
            """
        columnNamesList = self.df.columns.values.tolist().copy()
        for index, columnName in enumerate(columnNamesList):
            if self.df[columnName].isnull().all() == True:
                print(f'Warning: Removed empty column "{columnName}"')
                self.removeColumnFromDf(columnName)
