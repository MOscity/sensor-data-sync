# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:35:43 2022

@author: Groovekeeper
"""

# Testbench
# Testbench
import configparser, argparse # for argument parsing
from dateutil.parser import parse
import sys, time, os, glob
from dateutil import rrule
from datetime import datetime, timedelta

import pandas as pd
from pandas.plotting import register_matplotlib_converters

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

from functions import *
from classes import *

from Aethalometer_settings import *
from PMSChinaSensor_settings import *
from ComPAS_settings import *
from SMPS3080_Exported_Settings import *
    
# Averaging intervals for synchonrizing datasets
FREQ = 10
MODE = 'min'  

# Define which sensors were used:
AETH_Bool = True
PMS_Bool = True
ComPAS_Bool = True
SMPS_Bool = True

# File Paths:
# File Paths must be valid for all used sensors (i.e. if set TRUE above)    
DATA_PATH_AETH = 'S:/HT/A1874_ISE/A1874_Projekte/2018_Light_Absorption/Messkampagne Dec 2021/AE33/2021/'
FILE_EXT_AETH = 'AE33_AE33-S02-00176_20211221.dat'

DATA_PATH_PMS = 'S:/HT/A1874_ISE/A1874_Projekte/2018_Light_Absorption/Messkampagne Dec 2021/ChinaSensor/'
FILE_EXT_PMS = 'China-Sensor-2021-12-14.csv'

DATA_PATH_ComPAS = 'S:/HT/A1874_ISE/A1874_Projekte/2018_Light_Absorption/Messkampagne Dec 2021/ComPAS Data/'
FILE_EXT_ComPAS = 'ComPAS_AllDatas_18-12-2021.txt'

DATA_PATH_SMPS = 'S:/HT/A1874_ISE/A1874_Projekte/2018_Light_Absorption/Messkampagne Dec 2021/SMPS/'
FILE_EXT_SMPS = '211214_Export.csv'

AETH_File = DATA_PATH_AETH+FILE_EXT_AETH
PMS_File = DATA_PATH_PMS+FILE_EXT_PMS
ComPAS_File = DATA_PATH_ComPAS+FILE_EXT_ComPAS
SMPS_File = DATA_PATH_SMPS+FILE_EXT_SMPS

myD = New_Sensor('myDevice','Unknown', ComPAS_File, TimeFormat='DateTime_1Column', skiprows=0)