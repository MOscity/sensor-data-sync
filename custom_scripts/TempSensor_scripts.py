# from lib import np, pd, allantools, timedelta


def TempSensorPreScript(sensorObject):
    sensorObject.plotColumn = 'Temperature Difference [K]'
    return sensorObject


def TempSensorPostScript(sensorObject):
    return sensorObject

