from lib import rrule, timedelta, pd, register_matplotlib_converters, plt, mdates, FuncFormatter

def my_header_formatter(header_list, replace_signs= ['[',']','{','}','(',')','$',':',';','.','-','#','&','/','\\','%','^','°']):
    """Formats header s.t. all special characters are replaced with '_'
        This dataset is easier to import and modify in 'Veusz' : ) 
        """
    export_header = header_list.copy()
    for l_indx,orig_value in enumerate(header_list):
        for r_indx,repl_value in enumerate(replace_signs):
            if repl_value == '/':
                export_header[l_indx] = export_header[l_indx].replace(repl_value, ' per ')
            elif repl_value == '%':
                export_header[l_indx] = export_header[l_indx].replace(repl_value, ' percent ')
            elif repl_value == '°':
                export_header[l_indx] = export_header[l_indx].replace(repl_value, ' deg ')
            else:
                export_header[l_indx] = export_header[l_indx].replace(repl_value, ' ')
        split_string = export_header[l_indx].split(' ')
        while split_string.count('')>0:
            split_string.remove('')
        export_header[l_indx] = '_'.join(split_string)
    return export_header

def my_date_formater(ax, delta):
    """Formats matplotlib axes 
        """
    if delta.days < 3:
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%a, %d-%b-%Y'))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.grid(True, which='minor')
        ax.tick_params(axis="x", which="major", pad=15)
        if delta.days < 0.75:
            ax.xaxis.set_minor_locator(mdates.HourLocator())
        if delta.days < 1:
            ax.xaxis.set_minor_locator(mdates.HourLocator((0,3,6,9,12,15,18,21,)))
        else:
            ax.xaxis.set_minor_locator(mdates.HourLocator((0,6,12,18,)))
    elif delta.days < 8:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%a %d'))
        ax.xaxis.grid(True, which='minor')
        ax.tick_params(axis="x", which="major", pad=15)
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.set(xlabel='date')
    else:
        xtick_locator = mdates.AutoDateLocator()
        xtick_formatter = mdates.AutoDateFormatter(xtick_locator)
        xtick_formatter.scaled[30.] = FuncFormatter(my_days_format_function)
        xtick_formatter.scaled[1.] = FuncFormatter(my_days_format_function)
        ax.xaxis.set_major_locator(xtick_locator)
        ax.xaxis.set_major_formatter(xtick_formatter)
        ax.set(xlabel='date')

def my_days_format_function(x, pos=None):
    """Formats matplotlib dates in daytime.
        """
    x = mdates.num2date(x)
    if pos == 0:
        fmt = '%d. %b\n%Y'
    else:
        fmt = '%d.%m '
    label = x.strftime(fmt)
    return label



def create_ini_file_from_dict(filepath,dictionary):
    """Creates an .ini file from an dictionary.
        filepath =      path for output file
        dictionary =    input dictionary
        """
    new_config_file = open(filepath, "w")
    new_config_file.write("[GENERAL_SETTINGS]\n")
    for key,value in dictionary.items():
        if type(value) == list:
            new_config_file.write(key + " : [" )
            if type(value[0])==str:
                for k in range(len(value)-1):
                    new_config_file.write("'" + str(value[k]) + "',")
                new_config_file.write("'" + str(value[-1]) + "']\n\n")
            else:
                for k in range(len(value)-1):
                    new_config_file.write(str(value[k]) + ",")
                new_config_file.write(str(value[-1]) + "]\n\n")                              
        elif type(value) == dict:
            new_config_file.write(key + " : {\t" )
            
            subvalues = list(value.values())
            subkeys = list(value.keys())
            
            if len(subkeys)>0:
                if type(subvalues[0])==str:
                    new_config_file.write("'" + str(subkeys[0]) + "' : '" + str(subvalues[0]) + "',\n")
                    for k in range(1,len(subvalues)-1):
                        new_config_file.write("\t\t'" + str(subkeys[k]) + "' : '" + str(subvalues[k]) + "',\n")
                    new_config_file.write("\t\t'" + str(subkeys[-1]) + "' : '" + str(subvalues[-1]) + "'\n\t}\n")
                else:
                    new_config_file.write("'" + str(subkeys[0]) + "' : " + str(subvalues[0]) + ",\n")
                    for k in range(1,len(subvalues)-1):
                        new_config_file.write("\t\t'" + str(subkeys[k]) + "' : " + str(subvalues[k]) + ",\n")
                    new_config_file.write("\t\t'" + str(subkeys[-1]) + "' : " + str(subvalues[-1]) + "\n\t}\n")
            else:
                new_config_file.write("' ' : 0 }\n")
        elif value == None: # value == None, int or float
            new_config_file.write(key + " : None \n")
        elif type(value) == str: # value == None, int or float
            new_config_file.write(key + " : '" + str(value) + "'\n")
        else: # value == int or float or bool
            new_config_file.write(key + " : " + str(value) + "\n")
    new_config_file.close()                 
 


def interval_rounder(t_mode,interval):
    """Rounds a number to nearest multiple of interval.
        t_mode =    input number (float/int)
        interval =  number to build multiples of (float/int)
        returns int
        """
    interval_half = interval/2.0
    t_new = (t_mode//interval)*interval
    if (t_mode//interval_half)%2: t_new += interval
    return int(t_new)

         
def time_rounder(t,interval=10,mode='min'): # modes = 'sec', 'min' or 'hour'
    """Rounds a given daytime to the nearest multiple of interval.
        t =         time of a day, type: datetime
        interval =  time interval (Default = 10)
        mode =      time units ('sec', 'min' (default) or 'hours')
        returns datetime
        """
    t_new_sec = t.second
    t_new_min = t.minute
    t_new_hour = t.hour
    t_add = timedelta()
        
    if mode=='sec':
        t_new_sec = interval_rounder(t_new_sec,interval)
        if (t_new_sec>=60):
            t_new_sec = t_new_sec-60
            t_add = timedelta(minutes=1)
        
    elif mode == 'min':
        t_new_sec = 0
        t_new_min = interval_rounder(t_new_min,interval)
        if (t_new_min>=60):
            t_new_min = t_new_min-60
            t_add = timedelta(hours=1)
        
    else: # mode == 'hours':
        t_new_sec = 0
        t_new_min = 0
        t_new_hour = interval_rounder(t_new_hour,interval)
        if (t_new_hour>=24):
            t_new_hour = t_new_hour-24
            t_add = timedelta(hours=1)
    
    return t.replace(second=t_new_sec, microsecond=0, minute=t_new_min, hour=t_new_hour)+t_add

def create_allan_plot(y, x=None, yunits='##', title="mySensor", ytitle='eBC'):
    """Creates a plot from y including labels and units. Written by Alejandro Keller.
        """
    plt.style.use('ggplot')
    register_matplotlib_converters()
    
    # definitions for the axes
    left, width = 0.1, 0.7
    bottom, height = 0.15, 0.75
    spacing = 0.005
    box_width = 1 - (1.5*left + width + spacing)

    rect_scatter = [left, bottom, width, height]
    rect_box = [left + width + spacing, bottom, box_width, height]

    # start with a rectangular Figure
    box = plt.figure("boxplot", figsize=(12, 6))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    ax_box = plt.axes(rect_box)
    ax_box.tick_params(direction='in', labelleft=False, labelbottom=False)

    # the scatter plot:
    if x==None:
        ax_scatter.plot(y) # change plot type to scatter to have markers
        tdelta = y.index.max() - y.index.min()
    else:
        ax_scatter.plot(x, y) # change plot type to scatter to have markers
        tdelta = x.max() - x.min()
    ax_scatter.set(xlabel='date', ylabel=ytitle + ' (' + yunits + ')', title=title)
    my_date_formater(ax_scatter, tdelta)

    # now determine nice limits by hand:
    # binwidth = 0.25
    lim0 = y.min()
    lim1 = y.max()
    if x==None:
        tlim0 = y.index.min()
        tlim1 = y.index.max()
    else:
        tlim0 = x.min()
        tlim1 = x.max()
    extra_space = (lim1 - lim0)/10
    extra_t = (tlim1 - tlim0)/10
    ax_scatter.set_xlim((tlim0-extra_t, tlim1+extra_t))
    ax_scatter.set_ylim((lim0-extra_space, lim1+extra_space))

    meanpointprops = dict(marker='D')
    ax_box.boxplot(y.dropna(), showmeans=True, meanprops=meanpointprops)
    ax_box.set_ylim(ax_scatter.get_ylim())
    mu = y.mean()
    sigma = y.std()
    text = r'$\mu={0:.2f},\ \sigma={1:.3f}$'.format(mu, sigma)
    ax_box.text(1, lim1 + extra_space/2, text, horizontalalignment="center", verticalalignment="center")
    
    plt.show()
    plt.close()
    del(box)
    
def create_plot(y, x=None, yunits='##', title="mySensor", ytitle='eBC'):
    """Creates a plot from y including labels and units. Written by Alejandro Keller.
        """
    plt.style.use('ggplot')
    register_matplotlib_converters()
    
    # definitions for the axes
    left, width = 0.1, 0.7
    bottom, height = 0.15, 0.75
    spacing = 0.005
    box_width = 1 - (1.5*left + width + spacing)

    rect_scatter = [left, bottom, width, height]
    rect_box = [left + width + spacing, bottom, box_width, height]

    # start with a rectangular Figure
    box = plt.figure("boxplot", figsize=(12, 6))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    ax_box = plt.axes(rect_box)
    ax_box.tick_params(direction='in', labelleft=False, labelbottom=False)

    # the scatter plot:
    if x==None:
        ax_scatter.plot(y) # change plot type to scatter to have markers
        tdelta = y.index.max() - y.index.min()
    else:
        ax_scatter.plot(x, y) # change plot type to scatter to have markers
        tdelta = x.max() - x.min()
    ax_scatter.set(xlabel='date', ylabel=ytitle + ' (' + yunits + ')', title=title)
    my_date_formater(ax_scatter, tdelta)

    # now determine nice limits by hand:
    # binwidth = 0.25
    lim0 = y.min()
    lim1 = y.max()
    if x==None:
        tlim0 = y.index.min()
        tlim1 = y.index.max()
    else:
        tlim0 = x.min()
        tlim1 = x.max()
    extra_space = (lim1 - lim0)/10
    extra_t = (tlim1 - tlim0)/10
    ax_scatter.set_xlim((tlim0-extra_t, tlim1+extra_t))
    ax_scatter.set_ylim((lim0-extra_space, lim1+extra_space))

    meanpointprops = dict(marker='D')
    ax_box.boxplot(y.dropna(), showmeans=True, meanprops=meanpointprops)
    ax_box.set_ylim(ax_scatter.get_ylim())
    mu = y.mean()
    sigma = y.std()
    text = r'$\mu={0:.2f},\ \sigma={1:.3f}$'.format(mu, sigma)
    ax_box.text(1, lim1 + extra_space/2, text, horizontalalignment="center", verticalalignment="center")
    
    plt.show()
    plt.close()
    del(box)

def calculate_intervals_csv(intervalfile, dataframe, decimals = 0 ,column=0, avg_mode=True, numerics_only=True):
    """Averages a dataframe and returns new dataframe with time intervals as defined in intervalfile.
        intervalfile =  file with interval., First row must be the column names (i.e. "start" and "end").
        dataframe =     sensor dataframe to average (sensor_df(pd.DataFrame))
        decimals =      decimal points to round mean/median value
        column =        columns to export as subset from dataframe
                        if column = 0, all columns are exported
        avg_mode =      if True: uses .mean() (Default),
                        if False: uses .median()
        numerics_only = if True: uses only non-empty entries (Default),
                        if False: ignores non-empty entries.
        returns pd.DataFrame
        """
    if column == 0:
        column = dataframe.df.columns.values.tolist().copy()
    df = pd.read_csv(intervalfile,
                     index_col = False,
                     parse_dates=['start','end'])
    for index, row in df.iterrows():
        subset = dataframe.getSubset_df(row['start'], row['end'], column)
        
        if avg_mode:
            columns_dict = dict(subset.mean(numeric_only=numerics_only))
        else:
            columns_dict = dict(subset.median(numeric_only=numerics_only))
            
        for key, value in columns_dict.items():
            df.loc[index, key] = round(value,decimals)
    df = df.set_index('end')
    return df


def calculate_intervals(dataframe, freq = 1, mode = 'min', decimals = 0, column=0, avg_mode=True, numerics_only=True): 
    """Averages a dataframe and returns new dataframe with equidistant time intervals of <freq> <mode>.
        dataframe =     sensor dataframe to average (sensor_df(pd.DataFrame))
        freq =          interval distance (int)
        mode =          interval units ('sec', 'min' or 'hours')
        decimals =      decimal points to round mean/median value
        column =        columns to export as subset from dataframe
                        if column = 0, all columns are exported
        fill_nonempty = uses last non-empty value  of a selected subset is empty.
                        iterates maximally 1500 minutes back in 1min steps.
        avg_mode =      if True: uses .mean() (Default), 
                        if False: uses .median()
        numerics_only = if True: uses only non-empty entries (Default),
                        if False: ignores non-empty entries.
        returns pd.DataFrame
        """
    freq = int(freq)
    df = pd.DataFrame(columns=['start','end'])
    
    if mode == 'sec':
        dt_0 = timedelta(seconds=freq)
        ruler = rrule.SECONDLY
    elif mode == 'min':
        dt_0 = timedelta(minutes=freq)
        ruler = rrule.MINUTELY
    else: #mode == 'hours'
        dt_0 = timedelta(hours=freq)
        ruler = rrule.HOURLY
        
    if column == 0:
        column = dataframe.df.columns.values.tolist().copy()
        
    tmin = time_rounder((dataframe.df.first_valid_index()),freq,mode)
    tmax = time_rounder((dataframe.df.last_valid_index()),freq,mode) - dt_0
    for dt in rrule.rrule(ruler, interval = freq, dtstart=tmin, until=tmax):
        start = dt
        end = dt+dt_0
        subset = dataframe.getSubset_df(start, end, column)
        
        index = len(df)
        df.loc[index, 'start'] = start
        df.loc[index, 'end'] = end

        if avg_mode:
            columns_dict = dict(subset.mean(numeric_only=numerics_only))
        else:
            columns_dict = dict(subset.median(numeric_only=numerics_only))
            
        for key, value in columns_dict.items():
            df.loc[index, key] = round(value,decimals)
    df = df.set_index('end')
    return df
