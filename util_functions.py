from lib import rrule, timedelta, pd, register_matplotlib_converters, plt, mdates, FuncFormatter


def headerFormatter(header_list, replace_signs=['[', ']', '{', '}', '(', ')', '$', ':', ';', '.', '-', '#', '&', '/', '\\', '%', '^', '°']):
    """Formats headerList s.t. all special characters are replaced with '_'
        This dataset is easier to import and modify in 'Veusz' : ) 
        """
    export_header = header_list.copy()
    for l_indx, orig_value in enumerate(header_list):
        for r_indx, repl_value in enumerate(replace_signs):
            if repl_value == '/':
                export_header[l_indx] = export_header[l_indx].replace(
                    repl_value, ' per ')
            elif repl_value == '%':
                export_header[l_indx] = export_header[l_indx].replace(
                    repl_value, ' percent ')
            elif repl_value == '°':
                export_header[l_indx] = export_header[l_indx].replace(
                    repl_value, ' deg ')
            else:
                export_header[l_indx] = export_header[l_indx].replace(
                    repl_value, ' ')
        split_string = export_header[l_indx].split(' ')
        while split_string.count('') > 0:
            split_string.remove('')
        export_header[l_indx] = '_'.join(split_string)
    return export_header


def createInitFileFromDictionary(filepath, dictionary):
    """Creates an .ini file from an dictionary.
        filepath =      path for output file
        dictionary =    input dictionary
        """
    new_config_file = open(filepath, "w")
    new_config_file.write("[settingsModel]\n")
    for key, value in dictionary.items():
        if type(value) == list:
            new_config_file.write(key + " : [")
            if type(value[0]) == str:
                for k in range(len(value)-1):
                    new_config_file.write("'" + str(value[k]) + "',")
                new_config_file.write("'" + str(value[-1]) + "']\n\n")
            else:
                for k in range(len(value)-1):
                    new_config_file.write(str(value[k]) + ",")
                new_config_file.write(str(value[-1]) + "]\n\n")
        elif type(value) == dict:
            new_config_file.write(key + " : {\t")

            subvalues = list(value.values())
            subkeys = list(value.keys())

            if len(subkeys) > 0:
                if type(subvalues[0]) == str:
                    new_config_file.write(
                        "'" + str(subkeys[0]) + "' : '" + str(subvalues[0]) + "',\n")
                    for k in range(1, len(subvalues)-1):
                        new_config_file.write(
                            "\t\t'" + str(subkeys[k]) + "' : '" + str(subvalues[k]) + "',\n")
                    new_config_file.write(
                        "\t\t'" + str(subkeys[-1]) + "' : '" + str(subvalues[-1]) + "'\n\t}\n")
                else:
                    new_config_file.write(
                        "'" + str(subkeys[0]) + "' : " + str(subvalues[0]) + ",\n")
                    for k in range(1, len(subvalues)-1):
                        new_config_file.write(
                            "\t\t'" + str(subkeys[k]) + "' : " + str(subvalues[k]) + ",\n")
                    new_config_file.write(
                        "\t\t'" + str(subkeys[-1]) + "' : " + str(subvalues[-1]) + "\n\t}\n")
            else:
                new_config_file.write("' ' : 0 }\n")
        elif value == None:  # value == None, int or float
            new_config_file.write(key + " : None \n")
        elif type(value) == str:  # value == None, int or float
            if key == 'timeColumnFormat':
                value = value.replace('%', '%%')
            else:
                value = value
            new_config_file.write(key + " : '" + str(value) + "'\n")
        elif key == 'dateTimeOrigin':
            new_config_file.write(key + " : '" + str(value) + "'\n")
        else:  # value == int or float or bool
            new_config_file.write(key + " : " + str(value) + "\n")
    new_config_file.close()


def intervalRounder(t_mode, interval):
    """Rounds a number to nearest multiple of interval.
        t_mode =    input number (float/int)
        interval =  number to build multiples of (float/int)
        returns int
        """
    interval_half = interval/2.0
    t_new = (t_mode//interval)*interval
    if (t_mode//interval_half) % 2:
        t_new += interval
    return int(t_new)


# modes = 'sec', 'min' or 'hour'
def daytimeRoundToNearestInterval(t, interval=10, mode='min'):
    """Rounds a given daytime to the nearest multiple of the given interval.
        t =         time of a day, type: datetime
        interval =  time interval (Default = 10)
        mode =      time units ('sec', 'min' (default) or 'hours')
        returns datetime
        """
    t_new_sec = t.second
    t_new_min = t.minute
    t_new_hour = t.hour
    t_add = timedelta()

    if mode == 'sec':
        t_new_sec = intervalRounder(t_new_sec, interval)
        if (t_new_sec >= 60):
            t_new_sec = t_new_sec-60
            t_add = timedelta(minutes=1)

    elif mode == 'min':
        t_new_sec = 0
        t_new_min = intervalRounder(t_new_min, interval)
        if (t_new_min >= 60):
            t_new_min = t_new_min-60
            t_add = timedelta(hours=1)

    else:  # mode == 'hours':
        t_new_sec = 0
        t_new_min = 0
        t_new_hour = intervalRounder(t_new_hour, interval)
        if (t_new_hour >= 24):
            t_new_hour = t_new_hour-24
            t_add = timedelta(hours=1)

    return t.replace(second=t_new_sec, microsecond=0, minute=t_new_min, hour=t_new_hour)+t_add


def calculateIntervalsAsDefinedInCSVFile(intervalfile, dataframe, decimals=9, column=0, avgMode=True, numerics_only=True, TimeColumnFormatOut='Format = %Y-%m-%d %H:%M'):
    """Averages a dataframe and returns new dataframe with time intervals as defined in intervalfile.
        intervalfile =  file with interval., First row must be the column names (i.e. "start" and "end").
        dataframe =     sensor dataframe to average (sensor_df(pd.DataFrame))
        decimals =      decimal points to round mean/median value
        column =        columns to export as subset from dataframe
                        if column = 0, all columns are exported
        avgMode =      if True: uses .mean() (Default),
                        if False: uses .median()
        numerics_only = if True: uses only non-empty entries (Default),
                        if False: ignores non-empty entries.
        returns pd.DataFrame
        """
    if column == 0:
        column = dataframe.df.columns.values.tolist().copy()
    df = pd.readCSV(intervalfile,
                    index_col=False,
                    parse_dates=['start', 'end'])
    for index, row in df.iterrows():
        subset = dataframe.getDfSubset(row['start'], row['end'], column)

        if avgMode:
            columnsDict = dict(subset.mean(numeric_only=numerics_only))
        else:
            columnsDict = dict(subset.median(numeric_only=numerics_only))

        for key, value in columnsDict.items():
            df.loc[index, key] = round(value, decimals)
    df = df.set_index('end')
    return df


def calculateIntervals(dataframe, freq=1, mode='min', decimals=9, column=0, avgMode=True, numerics_only=True):
    """Averages a dataframe and returns new dataframe with equidistant time intervals of <freq> <mode>.
        dataframe =     sensor dataframe to average (sensor_df(pd.DataFrame))
        freq =          interval distance (int)
        mode =          interval units ('sec', 'min' or 'hours')
        decimals =      decimal points to round mean/median value
        column =        columns to export as subset from dataframe
                        if column = 0, all columns are exported
        fill_nonempty = uses last non-empty value  of a selected subset is empty.
                        iterates maximally 1500 minutes back in 1min steps.
        avgMode =      if True: uses .mean() (Default), 
                        if False: uses .median()
        numerics_only = if True: uses only non-empty entries (Default),
                        if False: ignores non-empty entries.
        returns pd.DataFrame
        """
    freq = int(freq)
    df = pd.DataFrame(columns=['start', 'end'])

    if mode == 'sec':
        dt_0 = timedelta(seconds=freq)
        ruler = rrule.SECONDLY
    elif mode == 'min':
        dt_0 = timedelta(minutes=freq)
        ruler = rrule.MINUTELY
    else:  # mode == 'hours'
        dt_0 = timedelta(hours=freq)
        ruler = rrule.HOURLY

    if column == 0:
        column = dataframe.df.columns.values.tolist().copy()

    tmin = daytimeRoundToNearestInterval(
        (dataframe.df.first_valid_index()), freq, mode)
    tmax = daytimeRoundToNearestInterval(
        (dataframe.df.last_valid_index()), freq, mode) - dt_0

    inv_counter = 0

    for dt in rrule.rrule(ruler, interval=freq, dtstart=tmin, until=tmax):
        start = dt
        end = dt+dt_0

        #start_shifted = (start not in dataframe.df.index)
        #end_shifted = (end not in dataframe.df.index)
        start_value = start
        end_value = end

        # print('------------')
        while (start_value not in dataframe.df.index):
            start_value -= timedelta(seconds=1)
            #print('Shifting Start Time...', start_value)
            if start_value <= tmin:
                break

        while (end_value not in dataframe.df.index):
            end_value += timedelta(seconds=1)
            #print('Shifting End Time...', end_value)
            if end_value >= tmax:
                break

        while (start not in dataframe.df.index):
            start_value += timedelta(seconds=1)
            #print('Shifting Start Time forward...', start_value)
            if start_value >= end_value:
                break

        # if start_shifted:
        #     print('Shifted Start Time from', start, 'to', start_value)
        # if end_shifted:
        #     print('Shifted End Time from', end, 'to', end_value)

        subset = dataframe.getDfSubset(start_value, end_value, column)

        # print('my Subset', subset)
        # Uff this is dangerous...
        if len(subset) == 0:
            print('Warning! Empty Subset')
            subset = dataframe.getDfSubset(
                start_value-2*dt_0, end_value, column)

        index = len(df)
        df.loc[index, 'start'] = start
        df.loc[index, 'end'] = end
        #print('start:', start)
        #print('end:', end)
        # print(subset)

        if avgMode:
            columnsDict = dict(subset.mean(numeric_only=numerics_only))
        else:
            columnsDict = dict(subset.median(numeric_only=numerics_only))

        for key, value in columnsDict.items():
            df.loc[index, key] = round(value, decimals)

        inv_counter += 1

    df = df.set_index('end')

    return df
