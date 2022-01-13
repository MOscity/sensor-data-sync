# import configparser, argparse # for argument parsing
# from dateutil.parser import parse
# import sys, time, os, glob

from dateutil import rrule
from datetime import datetime, timedelta

import pandas as pd
from pandas.plotting import register_matplotlib_converters

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter


def my_date_formater(ax, delta):
    if delta.days < 3:
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
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
     x = mdates.num2date(x)
     if pos == 0:
         fmt = '%b %d\n%Y'
     else:
         fmt = '%b %-d'
     label = x.strftime(fmt)
     return label

# def LabView_to_DateTime(tlab):
#     return datetime.fromtimestamp(tlab - 2082844800)

# def ExcelTime_to_Datetime(texc):
#     return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + texc - 2)



def interval_rounder(t_mode,interval):
    interval_half = interval/2.0
    t_new = (t_mode//interval)*interval
    if (t_mode//interval_half)%2: t_new += interval
    return int(t_new)

         
def time_rounder(t,interval=1,mode='min'): # modes = 'sec', 'min' or 'hour'
    
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
        
    else: # mode == 'hour':
        t_new_sec = 0
        t_new_min = 0
        t_new_hour = interval_rounder(t_new_hour,interval)
        if (t_new_hour>=24):
            t_new_hour = t_new_hour-24
            t_add = timedelta(hours=1)
    
    return t.replace(second=t_new_sec, microsecond=0, minute=t_new_min, hour=t_new_hour)+t_add


def create_plot(y, x=None, yunits='##', title="mySensor", ytitle='eBC'):
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

def calculate_intervals_csv(intervalfile, df_origin, decimals = 0 ,column=0):
    if column == 0:
        column = df_origin.columns
    df = pd.read_csv(intervalfile,
                     index_col = False,
                     parse_dates=['start','end'])
    for index, row in df.iterrows():
        subset = df_origin.df.getSubset_df(row['start'], row['end'], column)
        for key, value in subset.mean().iteritems():
            df.loc[index, key] = round(value,decimals)
    df = df.set_index('end')
    return df


def calculate_intervals(dataframe, freq = 1, mode = 'min', decimals = 0, column=0, fill_nonempty=True ): 
    # Frequency is averaging interval in units of 'sec', 'min' or 'hours'
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
        column = dataframe.df.columns.values
        
    tmin = time_rounder((dataframe.df.first_valid_index()),freq,mode)
    tmax = time_rounder((dataframe.df.last_valid_index()),freq,mode) - dt_0
    
    for dt in rrule.rrule(ruler, interval = freq, dtstart=tmin, until=tmax):
        start = dt
        end = dt+dt_0
        subset = dataframe.getSubset_df(start, end, column)
        
        if fill_nonempty: # if subset is empty roll back in time to get last non-zero subset
            k = 0
            while len(subset)==0: 
                subset = dataframe.getSubset_df(start-timedelta(minutes=k),end, column)
                k+=1
                if k > 10000: # stop if k is too large
                    continue
        
        index = len(df)
        df.loc[index, 'start'] = start
        df.loc[index, 'end'] = end

        columns_dict = dict(subset.mean(numeric_only=True))
        for key, value in columns_dict.items():
            df.loc[index, key] = round(value,decimals)
    df = df.set_index('end')
    return df
