# from lib import np, pd, allantools, timedelta


def SMPS3080_ExpPreScript(sensorObject):
    # Use this script if data were already processed by Ernest's excel sheet 'script'.
    timeIntervals = '60S'  # 10 Second
    sensorObject.df1.df = sensorObject.df1.df.resample(
        timeIntervals).ffill().bfill().interpolate()
    return sensorObject


def SMPS3080_ExpPostScript(sensorObject):
    return sensorObject


def SMPS3080PreScript(sensorObject):
    return sensorObject


def SMPS3080PostScript(sensorObject):
    return sensorObject
