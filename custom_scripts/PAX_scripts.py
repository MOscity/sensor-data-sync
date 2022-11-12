# from lib import np, pd, allantools, timedelta


def PAXPreScript(sensorObject):
    timeIntervals = '10S'  # 10 Seconds
    sensorObject.df1.df = sensorObject.df1.df.resample(
        timeIntervals).interpolate()
    # PAX is not recording data when in BKG/Filter modus, therefore resampling is needed and values are interpolated (linear).
    return sensorObject


def PAXPostScript(sensorObject):
    return sensorObject
