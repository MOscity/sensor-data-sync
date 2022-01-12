
import pandas as pd
import numpy as np

def Amplitude_Phase(sensor_df,X_Column,Y_Column):    
    new_R = pd.DataFrame({"R": np.sqrt(sensor_df.df[X_Column]**2+sensor_df.df[Y_Column]**2)},index=sensor_df.df.index)
    new_Th = pd.DataFrame({"Theta": np.arctan2(sensor_df.df[Y_Column],sensor_df.df[X_Column])*180.0/np.pi},index=sensor_df.df.index)
    return new_R, new_Th


def Check_Pre_Scripts(SENSOR_Object):
    model_name = SENSOR_Object.modelname
    if model_name == 'AE33':
        return Aeth33_Pre_Script(SENSOR_Object)
    elif model_name == 'AE31':
        return Aeth31_Pre_Script(SENSOR_Object)
    elif model_name == 'PMS1':
        return PMS_Pre_Script(SENSOR_Object)
    elif model_name == 'ComPAS-V4':
        return ComPASV4_Pre_Script(SENSOR_Object)
    elif model_name == 'ComPAS-V5':
        return ComPASV5_Pre_Script(SENSOR_Object)
    elif model_name == 'SMPS3080_Export':
        return SMPS3080_Exp_Pre_Script(SENSOR_Object)
    elif model_name == 'SMPS3080':
        return SMPS3080_Pre_Script(SENSOR_Object)
    elif model_name == 'MSPTI':
        return MSPTI_Pre_Script(SENSOR_Object)
    elif model_name == 'miniPTI':
        return miniPTI_Pre_Script(SENSOR_Object)
    else:
        return SENSOR_Object

def Check_Post_Scripts(SENSOR_Object):
    model_name = SENSOR_Object.modelname
    if model_name == 'AE33':
        return Aeth33_Post_Script(SENSOR_Object)
    elif model_name == 'AE31':
        return Aeth31_Post_Script(SENSOR_Object)
    elif model_name == 'PMS1':
        return PMS_Post_Script(SENSOR_Object)
    elif model_name == 'ComPAS-V4':
        return ComPASV4_Post_Script(SENSOR_Object)
    elif model_name == 'ComPAS-V5':
        return ComPASV5_Post_Script(SENSOR_Object)
    elif model_name == 'SMPS3080_Export':
        return SMPS3080_Exp_Post_Script(SENSOR_Object)
    elif model_name == 'SMPS3080':
        return SMPS3080_Post_Script(SENSOR_Object)
    elif model_name == 'MSPTI':
        return MSPTI_Post_Script(SENSOR_Object)
    elif model_name == 'miniPTI':
        return miniPTI_Post_Script(SENSOR_Object)
    else:
        return SENSOR_Object   


def PMS_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def PMS_Post_Script(SENSOR_Object):
    SENSOR_Object.Linear_Modify('Concentration ug/m3', 1000,0)
    SENSOR_Object.Rename_sensor_signals('Concentration ug/m3', 'Concentration ng/m3', 'ng/m$^3$')
    return SENSOR_Object



def ComPASV4_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def ComPASV4_Post_Script(SENSOR_Object):
    # Add new Columns and Calibrate
    # Blue:
    A_Blue = 1221.5/558.0 
    # Green
    A_Green = 415.5/203.0
    # Red
    A_Red = 30.35/4.0
    
    SENSOR_Object.Linear_Modify('Blue A Mov. Avg [uPa]', A_Blue,0)
    SENSOR_Object.Rename_sensor_signals('Blue A Mov. Avg [uPa]', 'Blue A Mov. Avg [Mm^-1]', 'Mm$^-1$')
    
    SENSOR_Object.Linear_Modify('Green A Mov. Avg [uPa]', A_Green,0)
    SENSOR_Object.Rename_sensor_signals('Green A Mov. Avg [uPa]', 'Green A Mov. Avg [Mm^-1]', 'Mm$^-1$')
    
    SENSOR_Object.Linear_Modify('Red A Mov. Avg [uPa]', A_Red,0)
    SENSOR_Object.Rename_sensor_signals('Red A Mov. Avg [uPa]', 'Red A Mov. Avg [Mm^-1]', 'Mm$^-1$') 
          
    new_R1, new_Th1 = Amplitude_Phase(SENSOR_Object.df1, 'X1', 'Y1')
    SENSOR_Object.addSubset(new_R1/214.7483648, 'R1', 'uPa') # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1, 'Theta1', 'deg') # Theta in deg

    new_R2, new_Th2 = Amplitude_Phase(SENSOR_Object.df1, 'X2', 'Y2')
    SENSOR_Object.addSubset(new_R2/214.7483648, 'R2', 'uPa') # Scale R to uPa
    SENSOR_Object.addSubset(new_Th2, 'Theta2', 'deg') # Theta in deg
    
    SENSOR_Object.plotkey = 'Blue A Mov. Avg [Mm^-1]'
    
    return SENSOR_Object

def ComPASV5_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def ComPASV5_Post_Script(SENSOR_Object):
    return SENSOR_Object
    
def SMPS3080_Exp_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def SMPS3080_Exp_Post_Script(SENSOR_Object):
    return SENSOR_Object

def SMPS3080_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def SMPS3080_Post_Script(SENSOR_Object):
    return SENSOR_Object

def Aeth33_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def Aeth33_Post_Script(SENSOR_Object):
    return SENSOR_Object

def Aeth31_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def Aeth31_Post_Script(SENSOR_Object):
    return SENSOR_Object

def MSPTI_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def MSPTI_Post_Script(SENSOR_Object):
    return SENSOR_Object

def miniPTI_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def miniPTI_Post_Script(SENSOR_Object):
    return SENSOR_Object