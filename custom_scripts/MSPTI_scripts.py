# from lib import np, pd, allantools, timedelta


def MSPTIPreScript(sensorObject):
    return sensorObject


def MSPTIPostScript(sensorObject):
    return sensorObject


def MSPTI_MetasPreScript(sensorObject):
    sensorObject.df1.df.index = sensorObject.df1.df.index.tz_localize(None)
    return sensorObject


def MSPTI_MetasPostScript(sensorObject):
    return sensorObject
