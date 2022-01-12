
import pandas as pd
# from functions import rename_key_in_dict

def rename_key_in_dict(old_dict,old_name,new_name):
    """Replaces a key in a dictionary and returns a new dictionary.
        The value of the key is not changed.
        old_dict = input dictionary
        old_name = name of old key
        new_name = new name for old key
            returns new dictionary"""
    new_dict = {}
    for key,value in old_dict.items():
        new_key = (key if key != old_name else new_name)
        new_dict[new_key] = old_dict[key]
    return new_dict


class sensor_df(object):
    def __init__(self, df=pd.DataFrame()):
        """Initialize sensor object.
        
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
        
    def getSubset_df(self, start, end, columns):
        """returns the panda dataframe subset of the given columns.
            start = start datetime (pd.datetime)
            end = end datetime (pd.datetime)
            columns = columns to export (str)"""
        return self.df.loc[pd.to_datetime(start):pd.to_datetime(end), columns]
   
    def dropDuplicates_in_df(self, column_to_check):  
        """Drops duplicate entries in the given column in this dataframe.
            column_to_check = column to check for duplicates"""
        self.df = self.df.drop_duplicates(column_to_check)
    
    def Linear_Modify_df(self, Column, A,B):# returns A*col[i]+B
        """Linear modification of the given column in this dataframe.
            Column = column to modify (str)
            col_new[i] = A*col[i]+B"""
        self.df[Column] = A*self.df[Column]+B
        
    def NPoly_Modify_df(self, Column, a_n=[0,1]): # returns a[n]*col[i]**n + a[n-1]*col[i]**(n-1) + ... + a[1]*col[i] + a[0]
        """Polynomial modification of the given column in this dataframe.
            Column = column to modify (str)
            a_n = list of coefficients in ascending order
                    e.g. a_n = a_n=[0,1] for Linear Modification
            col_new[i] = a[n]*col[i]**n + a[n-1]*col[i]**(n-1) + ... 
            ... + a[1]*col[i] + a[0]"""
        for k in range(len(a_n)):
            self.df[Column] = a_n[k]*self.df[Column]**k
        
    # def Exp_Modify_df(self, Column, A,B): # returns exp(a*col[i]+b)
    #     self.df[Column] = np.exp(A*self.df[Column]+B)   

    # def Amplitude_Phase(sensor_df,X_Column,Y_Column):    
    #     new_R = pd.DataFrame({"R": np.sqrt(sensor_df.df[X_Column]**2+sensor_df.df[Y_Column]**2)},index=sensor_df.df.index)
    #     new_Th = pd.DataFrame({"Theta": np.arctan2(sensor_df.df[Y_Column],sensor_df.df[X_Column])*180.0/np.pi},index=sensor_df.df.index)
    #     return new_R, new_Th
        
    def Rename_df_Column(self, old_name, new_name):
        """Rename a column of this dataframe, if present.
            old_name = column/signal to modify (str)
            new_name = new name (str)"""
        column_names = self.df.columns.values.tolist()
        if column_names.count(old_name)>0:
            pos_df = column_names.index(old_name)
            column_names[pos_df] = new_name     
        self.df.columns = column_names
            
    def addSubset_to_df(self, df_other, new_name = 'New List'):
        """Adds a dataframe (to the right) to this dataframe.
            df_other = dataframe to join (panda dataframe)
            new_name = new column name (string)"""
        given_name = df_other.columns[-1]       
        self.df.join(df_other)
        self.Rename_df_Column(given_name, new_name)
        
    def removeColumn_from_df(self,column):
        """Removes the given column in this dataframe, if present.
            column = column name (string)"""
        if len(self.df)>0:
            if len(self.df.get(column,[]))>0:
                self.df.pop(column)   

class Sensor(object):
    def __init__(self, sensorname, model, datafile, header=[], header_export=[], signal_units_dict={}, other_dict={},TimeColumn='',TimeFormat= '',append_text= '',quotechar = '"', separator='',skiprows=0,plotkey='',origin=0, date_units='s'):
        """Initialize sensor object.
        
        # =============================================================================
        Attributes:
        # =============================================================================
            self.name :             sensor name (str)
            
            self.modelname :        model (str), see "model"_settings.ini files
            self.datapath :         path to datafiles (str), see config.ini file
            self.new_model :        False if found in model list, else True
            self.df1, 
            self.df2, 
            self.df3 :              3 panda dataframes with extended functions
            self.signals :          header list (overrides found header in file if provided)
            self.mainsignals :      signals to export (from self.signals)
            self.signal_units_dict: signal units dictionary for any/all elements of self.signals
            self.other_dict :       other dictionary for any/all elements 
                                    of self.signals (e.g. wavelengths dictionary)
            self.plotkey :          signal to plot (one of self.signals)
        # =============================================================================  
        Inputs:
        # =============================================================================
            sensorname :            Any name for your sensor (str)
            model :                 Model name of your sensor (str).
                                    Currently Supported: AE33, AE31, SMPS3080_Export, ComPAS-V4, PMS1
                                    Any other name will be registered as 'new model'.
            datafile :              data path (str)
            header = [] :           Override header row, length must match with columns. 
                                    If not provided, first row will be used as column names.
                         
            header_export = [] :    list for signals to export.
            signal_units_dict = {}: dictionary for units of signals.
            other_dict = {} :       other dictionary.
            TimeColumn = '' :       Column with date time entries (str)
                                    if TimeFormat is set to 'DateTime_2Column', provide 2 column names 
                                    for date and time as a list, e.g. TimeColumn = ['Date','Time'].
            TimeFormat = '' :       'Excel', 'DateTime_1Column', 'DateTime_2Column' or 'origin'.
            # 
            # TimeFormat:           Devices, Comments:
            # 'Excel'               --> SMPS
            # 'DateTime_1Column'    --> ComPAS, PMS ChinaSensor
            # 'DateTime_2Column'    --> Aethalometer
            # 'origin'              --> provide custom origin with pandas datetime, 
            #                           e.g. pd.datetime('1900/01/01')
            #                          
            # TimeFormat:           Examples:  
            # 'Excel'               44543.44961
            # 'DateTime_2Column'    2021/12/29 +{separator}+ 00:09:00
            # 'DateTime_1Column'    16-12-2021 10:11:43
            # 'DateTime_1Column'    14.12.2021 10:05:28

            append_text = '' :      unknown feature - ask alejandro
            
            quotechar = '"' :       Char for quotations in datafile.
            separator = '' :        separator in datafile, e.g ',' , '\t', ';' 
                                    or None (=interpret file structure with python, default)
            skiprows = 0 :          skip first N rows of datafile.
            plotkey = '' :          Column to plot. Default is last column.
            origin = 0 :            if TimeFormat is set to 'origin' define origin and date_units:
                                    origin: Define the reference date. The numeric values would be 
                                    parsed as number of units (defined by unit) since this reference date.
                                    If ‘unix’ (or POSIX) time; origin is set to 1970-01-01.
                                    If ‘julian’, unit must be ‘D’, and origin is set to beginning of 
                                    Julian Calendar. Julian day number 0 is assigned to the day starting 
                                    at noon on January 1, 4713 BC.
                                    If Timestamp convertible, origin is set to Timestamp identified by origin.                     
            date_units = 's'        date_units: The unit of the arg (D,s,ms,us,ns) denote the unit, which 
                                    is an integer or float number. This will be based off the origin. 
                                    Example, with unit=’ms’ and origin=’unix’ (the default), this would 
                                    calculate the number of milliseconds to the unix epoch start.
       # =============================================================================   
        """
        
        self.name = sensorname
        self.modelname = model
        self.datapath = datafile
        
        self.new_model = False
        
        if model in ['AE33','AE31','SMPS3080_Export','ComPAS-V4','PMS1']:
            self.new_model = False
        else:
            self.new_model = True
            
        if self.new_model:
            header_out = None
            separator_out = None
            skiprows_out = 0
            # Commented lines will be read from file below
            # header_export_out
            # signal_units_dict_out
            other_dict_out = {'':0}
            # TimeColumn_out
            TimeFormat_out = None
            append_text_out = ""
            quotechar_out= '"'
            # plotkey_out
        else:
            header_out = header
            separator_out = separator
            skiprows_out = skiprows
            
            header_export_out = header_export
            signal_units_dict_out = signal_units_dict
            other_dict_out = other_dict
            TimeColumn_out = TimeColumn
            TimeFormat_out = TimeFormat
            append_text_out = append_text
            quotechar_out = quotechar
            plotkey_out = plotkey
        
        if len(header)>0:               # Override header before read file
            header_out = header
        
        if len(separator)>0:            # Override separator before read file
            separator_out = separator
         
        if skiprows>0:                  # Override skiprows before read file
            skiprows_out = skiprows
          
        self.df1 = sensor_df(pd.read_csv(
            datafile,                   # relative python path to subdirectory
            index_col = False,
            names = header_out,         # use names=None to infer column names
            sep = separator_out,        # Space-separated value file.
            quotechar = quotechar_out,  # double quote allowed as quote character
            skiprows = skiprows_out,    # Skip the first X row of the file
            engine = 'python'           # allows to use sep=None to find separator
            ))
        
        self.df2 = sensor_df(pd.DataFrame())
        self.df3 = sensor_df(pd.DataFrame())
        
        if self.new_model:
            header_out = self.df1.df.columns.to_list()
            header_export_out = header_out
            signal_units_dict_out = dict.fromkeys(header_out,'')
            TimeColumn_out = header_out[0]
            plotkey_out = header_out[-1]
        
        if len(header_export)>0:
            header_export_out = header_export
            
        if len(signal_units_dict.items())>0:
            signal_units_dict_out = signal_units_dict         
        
        if len(other_dict.items())>0:
            other_dict_out = other_dict
          
        if len(TimeColumn)>0:
            TimeColumn_out = TimeColumn
            if type(TimeColumn)==list:
                if len(TimeColumn)!=2:
                    raise Exception("Provide a list with 2 string entries for Date and Time, e.g. TimeColumn = ['Date','Time']") 
                TimeFormat_out = 'DateTime_2Column'
                DateColumn_out = TimeColumn[0]
                TimeColumn_out = TimeColumn[1]   
            
        if len(TimeFormat)>0:
            TimeFormat_out = TimeFormat
            if TimeFormat == 'DateTime_2Column':
                if type(TimeColumn)==list:
                    if len(TimeColumn)!=2:
                        raise Exception("Provide a list with 2 string entries for Date and Time, e.g. TimeColumn = ['Date','Time']") 
                    DateColumn_out = TimeColumn[0]
                    TimeColumn_out = TimeColumn[1]
                elif type(TimeColumn)==str and len(TimeColumn)>0: 
                    raise Exception("If TimeFormat is set to {}, leave TimeColumn empty or provide a list with 2 entries for Date and Time, e.g. TimeColumn = ['Date','Time'] ".format(TimeFormat)) 
                else: # Assume first 2 columns are 'Date' and 'Time'
                    DateColumn_out = header_out[0]
                    TimeColumn_out = header_out[1]
                    
        if len(plotkey)>0:
            plotkey_out = plotkey
        
        if TimeFormat_out in ['Excel']:
            # Datetime format is given from excel (example 44544.42951 is 2021-Dec-14. 10:18:29.664)
            self.df1.df['Datetime'] = pd.to_datetime(self.df1.df[TimeColumn_out], unit='D', origin=pd.to_datetime('1900/01/01'))
            self.df1.df['Datetime'] = pd.to_datetime(self.df1.df['Datetime']) - pd.to_timedelta(2, unit='D') # subtract 2 additional days 
        elif TimeFormat_out in ['DateTime_2Column']:
            #self.df['Datetime'] = pd.to_datetime(self.df['Date']) + pd.to_timedelta(self.df['Time'])
            self.df1.df['Datetime'] = pd.to_datetime(self.df1.df[DateColumn_out] + " " + self.df1.df[TimeColumn_out], infer_datetime_format=True)
        elif TimeFormat_out in ['DateTime_1Column']:
            self.df1.df['Datetime'] = pd.to_datetime(self.df1.df[TimeColumn_out], infer_datetime_format=True)
        elif TimeFormat_out in ['origin']:
            self.df1.df['Datetime'] = pd.to_datetime(self.df1.df[TimeColumn_out], unit=date_units, origin=origin)   
        else: # if TimeFormat = None : infer date time
            self.df1.df['Datetime'] = pd.to_datetime(self.df1.df[TimeColumn_out], infer_datetime_format=True)
        
        self.df1.df = self.df1.df.set_index('Datetime')
        
        
        self.signals = header_out
        self.mainsignals = header_export_out
        self.signal_units_dict = signal_units_dict_out
        self.other_dict = other_dict_out
        self.plotkey = plotkey_out    
              
            
    def getSubset(self, start, end, columns, df_index = 1):
        """returns the sensor_df subset of the given columns and selected dataframes.
            start = start datetime (pd.datetime)
            end = end datetime (pd.datetime)
            columns = columns to export (str)
            df_index = 1(=default), 2 or 3"""
        if df_index == 2:
            return self.df2.getSubset_df(start, end, columns)
        elif df_index==3:
            return self.df3.getSubset_df(start, end, columns)
        else:
            return self.df3.getSubset_df(start, end, columns)
        
    def Rename_sensor_signals(self, old_name, new_name, new_units=False, df_index=-1):
        """Rename a column/signal and all related attributes of a sensor_object.
            old_name = column/signal to modify (str)
            new_name = new name (str)
            new_units = units of new column/signal (str)
            df_index = 1,2,3, or -1(=all, default)"""
        # Check in df:
        column1_names = self.df1.df.columns.values.tolist()
        column2_names = self.df2.df.columns.values.tolist()
        column3_names = self.df3.df.columns.values.tolist()
        
        if df_index not in [2,3]:
            if column1_names.count(old_name)>0:
                pos_df1 = column1_names.index(old_name)
                column1_names[pos_df1] = new_name     
            self.df1.df.columns = column1_names
        if df_index not in [1,3]:
            if column2_names.count(old_name)>0:
                pos_df2 = column2_names.index(old_name)
                column2_names[pos_df2] = new_name     
            self.df2.df.columns = column2_names
            
        if df_index not in [1,2]:
            if column3_names.count(old_name)>0:
                pos_df3 = column3_names.index(old_name)
                column3_names[pos_df3] = new_name     
            self.df3.df.columns = column3_names
        
        # Check in signals:
        if self.signals.count(old_name)>0:
            pos_signals = self.signals.index(old_name)
            self.signals[pos_signals] = new_name
            
        # Check in mainsignals:
        if self.mainsignals.count(old_name)>0:
            pos_mainsignals = self.mainsignals.index(old_name)
            self.mainsignals[pos_mainsignals] = new_name   

        # Check in signal_units_dict:
        units_keys = list(self.signal_units_dict.keys())
        if units_keys.count(old_name)>0: 
            if new_units!=False:
                self.signal_units_dict[old_name] = new_units
            self.signal_units_dict = rename_key_in_dict(self.signal_units_dict,old_name,new_name)    
            
        # Check in other_dict:
        other_keys = list(self.other_dict.keys())
        if other_keys.count(old_name)>0: 
            self.other_dict[old_name] = new_units
            self.other_dict = rename_key_in_dict(self.other_dict,old_name,new_name)  
            
        # Check in plotkey
        if self.plotkey == old_name:
            self.plotkey = new_name
    
    
    def addSubset(self, df_other, new_name = 'New List', new_units=' ', df_index = -1):
        """Adds a dataframe (to the right) to one/all sensor dataframes.
            df_other = dataframe to join (panda dataframe)
            new_name = new column name (string)
            new_units = new units for sensor object
            df_index = 1,2,3, or -1(=all, default)"""
        given_name = df_other.columns[-1]       
        self.signals.append(given_name)
        self.mainsignals.append(given_name)
        self.signal_units_dict.update({given_name: new_units})
        
        if df_index == 1:
            self.df1.df = self.df1.df.join(df_other)
        elif df_index == 2:
            self.df2.df = self.df2.df.join(df_other)
        elif df_index == 3:
            self.df3.df = self.df3.df.join(df_other)
        else:
            self.df1.df = self.df1.df.join(df_other)
            self.df2.df = self.df2.df.join(df_other)
            self.df3.df = self.df3.df.join(df_other)
            
        self.Rename_sensor_signals(given_name, new_name, new_units)

    def removeSubset(self, column, df_index = -1):
        """Removes the given column from one/all sensor dataframes.
            column = column name (string)
            df_index = 1,2,3, or -1(=all, default)"""
        if self.signals.count(column)>0:
            self.signals.remove(column)
            
        if self.mainsignals.count(column)>0:
            self.mainsignals.remove(column)
            
        if len(self.signal_units_dict)>0:
            if len(self.signal_units_dict.get(column,[]))>0:
                self.signal_units_dict.pop(column)
                
        if len(self.other_dict)>0:
            if len(self.other_dict.get(column,[]))>0:
                self.other_dict.pop(column)                 
        if df_index == 1:
            self.df1.removeColumn_from_df(column)
        elif df_index == 2:
            self.df2.removeColumn_from_df(column)
        elif df_index == 3:
            self.df3.removeColumn_from_df(column)
        else:
            self.df1.removeColumn_from_df(column)
            self.df2.removeColumn_from_df(column)
            self.df3.removeColumn_from_df(column)
            
        # Check in plotkey
        if self.plotkey == column:
            self.plotkey = self.signals[-1]
            
            
    def dropDuplicates(self, column_to_check, df_index = -1):
        """Drops duplicate entries in the given column in one/all sensor dataframes.
            column_to_check = column to check for duplicates
            df_index = 1,2,3, or -1(=all, default)"""
        if df_index == 1:
            self.df1 = self.df1.drop_duplicates(column_to_check)
        elif df_index == 2:
            self.df2 = self.df2.drop_duplicates(column_to_check)
        elif df_index == 3:
            self.df3 = self.df3.drop_duplicates(column_to_check)
        else:
            self.df1 = self.df1.drop_duplicates(column_to_check)
            self.df2 = self.df2.drop_duplicates(column_to_check)
            self.df3 = self.df3.drop_duplicates(column_to_check)          
            
    
    def Linear_Modify(self, Column, A,B, df_index=-1):
        """Linear modification of the given column in one/all sensor dataframes.
            Column = column to modify (str)
                --> col_new[i] = A*col[i]+B
            df_index = 1,2,3, or -1(=all, default)"""
        if df_index == 1:
            self.df1.Linear_Modify_df(Column, A, B)
        elif df_index == 2:
            self.df2.Linear_Modify_df(Column, A, B)
        elif df_index == 3:
            self.df3.Linear_Modify_df(Column, A, B)
        else:
            self.df1.Linear_Modify_df(Column, A, B)
            self.df2.Linear_Modify_df(Column, A, B)
            self.df3.Linear_Modify_df(Column, A, B)

    def NPoly_Modify(self, Column, a_n = [0,1], df_index=-1):
        """N-polynomial modification of the given column in one/all sensor dataframes.
            Column = column to modify (str)
            a_n = list of coefficients in ascending order
                    e.g. a_n = a_n=[0,1] for Linear Modification
            col_new[i] = a[n]*col[i]**n + a[n-1]*col[i]**(n-1) + ... 
            ... + a[1]*col[i] + a[0]
            df_index = 1,2,3, or -1(=all, default)"""
        if df_index == 1:
            self.df1.NPoly_Modify_df(Column, a_n=[0])
        elif df_index == 2:
            self.df2.NPoly_Modify_df(Column, a_n=[0])
        elif df_index == 3:
            self.df3.NPoly_Modify_df(Column, a_n=[0])
        else:
            self.df1.NPoly_Modify_df(Column, a_n=[0])
            self.df2.NPoly_Modify_df(Column, a_n=[0])
            self.df3.NPoly_Modify_df(Column, a_n=[0])