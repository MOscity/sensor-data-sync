# from lib import np, pd, allantools, timedelta


def miniPTIPreScript(sensorObject):
    sensorObject.renameColumnInSensorDf(
        '60s Norm dphi2 R Vect (V)', '60s Norm dphi2 R Vect (arb)', newUnits='')
    sensorObject.renameColumnInSensorDf(
        '60s Ernest new (V)', '60s Ernest new (arb)', newUnits='')
    return sensorObject


def miniPTIPostScript(sensorObject):
    return sensorObject

