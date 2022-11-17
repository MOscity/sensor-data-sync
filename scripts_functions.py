from custom_scripts import miniPTI_scripts, MSPTI_scripts, PAX_scripts, PMS_scripts, SMPS_3080_scripts, TempSensor_scripts, TempSensor_V2_scripts
from custom_scripts import AE31_and_AE33_scripts, ComPAS_scripts_V4, ComPAS_scripts_V5, ComPAS_scripts_V6


def CheckPreScripts(sensorObject):
    modelName = sensorObject.modelName
    if modelName == 'AE33':
        return AE31_and_AE33_scripts.Aeth33PreScript(sensorObject)
    elif modelName == 'AE31':
        return AE31_and_AE33_scripts.Aeth31PreScript(sensorObject)
    elif modelName == 'PMS1':
        return PMS_scripts.PMSPreScript(sensorObject)
    elif modelName == 'ComPAS-V4':
        return ComPAS_scripts_V4.ComPASV4PreScript(sensorObject)
    elif modelName == 'ComPAS-V5':
        return ComPAS_scripts_V5.ComPASV5PreScript(sensorObject)
    elif modelName == 'ComPAS-V6':
        return ComPAS_scripts_V6.ComPASV6PreScript(sensorObject)
    elif modelName == 'PAX':
        return PAX_scripts.PAXPreScript(sensorObject)
    elif modelName == 'SMPS3080_Export':
        return SMPS_3080_scripts.SMPS3080_ExpPreScript(sensorObject)
    elif modelName == 'SMPS3080':
        return SMPS_3080_scripts.SMPS3080PreScript(sensorObject)
    elif modelName == 'MSPTI_Export':
        return MSPTI_scripts.MSPTIPreScript(sensorObject)
    elif modelName == 'MSPTI_Metas_Export':
        return MSPTI_scripts.MSPTI_MetasPreScript(sensorObject)
    elif modelName == 'miniPTI':
        return miniPTI_scripts.miniPTIPreScript(sensorObject)
    elif modelName == 'TempSensor':
        return TempSensor_scripts.TempSensorPreScript(sensorObject)
    elif modelName == 'TempSensor_V2':
        return TempSensor_V2_scripts.TempSensorV2PreScript(sensorObject)
    else:
        return sensorObject


def CheckPostScripts(sensorObject):
    modelName = sensorObject.modelName
    if modelName == 'AE33':
        return AE31_and_AE33_scripts.Aeth33PostScript(sensorObject)
    elif modelName == 'AE31':
        return AE31_and_AE33_scripts.Aeth31PostScript(sensorObject)
    elif modelName == 'PMS1':
        return PMS_scripts.PMSPostScript(sensorObject)
    elif modelName == 'ComPAS-V4':
        return ComPAS_scripts_V4.ComPASV4PostScript(sensorObject)
    elif modelName == 'ComPAS-V5':
        return ComPAS_scripts_V5.ComPASV5PostScript(sensorObject)
    elif modelName == 'ComPAS-V6':
        return ComPAS_scripts_V6.ComPASV6PostScript(sensorObject)
    elif modelName == 'PAX':
        return PAX_scripts.PAXPostScript(sensorObject)
    elif modelName == 'SMPS3080_Export':
        return SMPS_3080_scripts.SMPS3080_ExpPostScript(sensorObject)
    elif modelName == 'SMPS3080':
        return SMPS_3080_scripts.SMPS3080PostScript(sensorObject)
    elif modelName == 'MSPTI_Export':
        return MSPTI_scripts.MSPTIPostScript(sensorObject)
    elif modelName == 'MSPTI_Metas_Export':
        return MSPTI_scripts.MSPTI_MetasPostScript(sensorObject)
    elif modelName == 'miniPTI':
        return miniPTI_scripts.miniPTIPostScript(sensorObject)
    elif modelName == 'TempSensor':
        return TempSensor_scripts.TempSensorPostScript(sensorObject)
    elif modelName == 'TempSensor_V2':
        return TempSensor_V2_scripts.TempSensorV2PostScript(sensorObject)
    else:
        return sensorObject
