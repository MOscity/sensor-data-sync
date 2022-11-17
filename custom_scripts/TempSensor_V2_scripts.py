# from lib import np, pd, allantools, timedelta


def TempSensorV2PreScript(sensorObject):
    sensorObject.plotColumn = 'Temperature Difference [K]'

    return sensorObject


def TempSensorV2PostScript(sensorObject):
    return sensorObject
