from lib import rrule, timedelta, pd


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


def calculateIntervalsAsDefinedInCSVFile(intervalfile, dataframe, decimals=9, column=0, avgMode=True, numerics_only=True):
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
    df_out = pd.read_csv(intervalfile,
                         index_col=False,
                         parse_dates=['start', 'end'])

    for index, row in df_out.iterrows():
        subset = dataframe.getDfSubset(row['start'], row['end'], column)

        if avgMode:
            columnsDict = dict(subset.mean(numeric_only=numerics_only))
        else:
            columnsDict = dict(subset.median(numeric_only=numerics_only))

        for key, value in columnsDict.items():
            df_out.loc[index, key] = round(value, decimals)
    df_out = df_out.set_index('end')
    return df_out


def calculateIntervals(dataframe, freq=1, mode='min', decimals=9, column=0, avgMode=True, numerics_only=True):
    """Averages a dataframe and returns new dataframe with equidistant time intervals of <freq> <mode>.
        dataframe =     sensor dataframe to average (sensor_df(pd.DataFrame))
        freq =          interval distance (int)
        mode =          interval units ('sec', 'min', 'hours' or 'days').
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
    df_out = pd.DataFrame(columns=['start', 'end'])

    if mode == 'sec':
        dt_0 = timedelta(seconds=freq)
        ruler = rrule.SECONDLY
        mode_code = 'S'
        # Note: 'L' is milliseconds.
    elif mode == 'min':
        dt_0 = timedelta(minutes=freq)
        ruler = rrule.MINUTELY
        mode_code = 'T'
    elif mode == 'hours':
        dt_0 = timedelta(hours=freq)
        ruler = rrule.HOURLY
        mode_code = 'H'
    else:  # mode == 'days':
        dt_0 = timedelta(days=freq)
        ruler = rrule.DAILY
        mode_code = 'd'

    if column == 0:
        column = dataframe.df.columns.values.tolist().copy()

    # Get first and last time index
    tmin = dataframe.df.first_valid_index()
    tmax = dataframe.df.last_valid_index()-dt_0/2.0

    # Round to nearest timestamp with the given interval and units.
    tmin = tmin.round(f'{freq}{mode_code}')
    tmax = tmax.round(f'{freq}{mode_code}')

    for dt in rrule.rrule(ruler, interval=freq, dtstart=tmin, until=tmax):
        start = dt
        end = dt+dt_0

        start_new = start
        end_new = end

        if (start not in dataframe.df.index):
            iloc_idx = dataframe.df.index.searchsorted(dt-dt_0)
            if iloc_idx > 0:
                iloc_idx -= 1
            loc_idx = dataframe.df.index[iloc_idx]
            start_new = loc_idx

        if (end not in dataframe.df.index):
            iloc_idx = dataframe.df.index.searchsorted(dt+dt_0)
            if iloc_idx >= len(dataframe.df)-1:
                iloc_idx = -1
            loc_idx = dataframe.df.index[iloc_idx]
            end_new = loc_idx

        # if end_new-start_new > 2*dt_0:
        #     print(f'{"":#^5}')
        #     print(
        #         f'WARNING: Time gap in subset is larger than usual.\n - Start Time: {start}\n - End Time: {end}\n - Columns: {column}')

        # get the original subset, but write the rounded time
        subset = dataframe.getDfSubset(start_new, end_new, column)

        if len(subset) == 0:
            print(f'{"":#^5}')
            print(
                f'WARNING: Empty Subset.\n - Start Time: {start}\n - End Time: {end}\n - Columns: {column}')

        else:
            index = len(df_out)
            # write the rounded time
            df_out.loc[index, 'start'] = start
            df_out.loc[index, 'end'] = end

        if avgMode:
            columnsDict = dict(subset.mean(numeric_only=numerics_only))
        else:
            columnsDict = dict(subset.median(numeric_only=numerics_only))

        for key, value in columnsDict.items():
            df_out.loc[index, key] = round(value, decimals)

    df_out = df_out.set_index('end')

    return df_out
