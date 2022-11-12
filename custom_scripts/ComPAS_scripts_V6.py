# from lib import np, pd, allantools, timedelta
from custom_scripts import ComPAS_scripts_V5


def ComPASV6PreScript(sensorObject):
    # Same as V5
    return ComPAS_scripts_V5.ComPASV5PreScript(sensorObject)


def ComPASV6PostScript(sensorObject, Mic_Konstant = 68.07064429, Green_Amplitdue_NO2_1ppm = 1250, Green_Absorption_NO2_1ppm = 415.46):
    # Same as V5
    return ComPAS_scripts_V5.ComPASV5PostScript(sensorObject, Mic_Konstant, Green_Amplitdue_NO2_1ppm, Green_Absorption_NO2_1ppm)

