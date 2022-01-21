from lib import np, pd

def Amplitude_Phase(sensor_df,X_Column,Y_Column,R_Name,Theta_Name):    
    new_R = pd.DataFrame({R_Name: np.sqrt(sensor_df.df[X_Column]**2+sensor_df.df[Y_Column]**2)},index=sensor_df.df.index)
    new_Th = pd.DataFrame({Theta_Name: np.arctan2(sensor_df.df[Y_Column],sensor_df.df[X_Column])*180.0/np.pi},index=sensor_df.df.index)
    return new_R, new_Th

def Check_Pre_Scripts(SENSOR_Object_df, model_name):
    # model_name = SENSOR_Object.modelname
    if model_name == 'AE33':
        return Aeth33_Pre_Script(SENSOR_Object_df)
    elif model_name == 'AE31':
        return Aeth31_Pre_Script(SENSOR_Object_df)
    elif model_name == 'PMS1':
        return PMS_Pre_Script(SENSOR_Object_df)
    elif model_name == 'ComPAS-V4':
        return ComPASV4_Pre_Script(SENSOR_Object_df)
    elif model_name == 'ComPAS-V5':
        return ComPASV5_Pre_Script(SENSOR_Object_df)
    elif model_name == 'SMPS3080_Export':
        return SMPS3080_Exp_Pre_Script(SENSOR_Object_df)
    elif model_name == 'SMPS3080':
        return SMPS3080_Pre_Script(SENSOR_Object_df)
    elif model_name == 'MSPTI_Export':
        return MSPTI_Pre_Script(SENSOR_Object_df)
    elif model_name == 'miniPTI':
        return miniPTI_Pre_Script(SENSOR_Object_df)
    else:
        return SENSOR_Object_df

def Check_Post_Scripts(SENSOR_Object_df, model_name):
    #model_name = SENSOR_Object.modelname
    if model_name == 'AE33':
        return Aeth33_Post_Script(SENSOR_Object_df)
    elif model_name == 'AE31':
        return Aeth31_Post_Script(SENSOR_Object_df)
    elif model_name == 'PMS1':
        return PMS_Post_Script(SENSOR_Object_df)
    elif model_name == 'ComPAS-V4':
        return ComPASV4_Post_Script(SENSOR_Object_df)
    elif model_name == 'ComPAS-V5':
        return ComPASV5_Post_Script(SENSOR_Object_df)
    elif model_name == 'SMPS3080_Export':
        return SMPS3080_Exp_Post_Script(SENSOR_Object_df)
    elif model_name == 'SMPS3080':
        return SMPS3080_Post_Script(SENSOR_Object_df)
    elif model_name == 'MSPTI_Export':
        return MSPTI_Post_Script(SENSOR_Object_df)
    elif model_name == 'miniPTI':
        return miniPTI_Post_Script(SENSOR_Object_df)
    else:
        return SENSOR_Object_df   


def PMS_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def PMS_Post_Script(SENSOR_Object_df):
    return SENSOR_Object_df


def ComPASV4_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def ComPASV4_Post_Script(SENSOR_Object_df):
    # This is my custom script and it's not finished yet.
        
    # Add new Columns and Calibrate  
    # Blue:
    A_Blue = 1221.5/558.0 
    # Green
    A_Green = 415.5/203.0
    # Red
    A_Red = 30.35/4.0
    
    SENSOR_Object_df.Linear_Modify_df('Blue A Mov. Avg [uPa]', A_Blue,0)
    SENSOR_Object_df.Rename_df_Column('Blue A Mov. Avg [uPa]', 'Blue 60s Mov. Avg [Mm^-1]')
    
    SENSOR_Object_df.Linear_Modify_df('Green A Mov. Avg [uPa]', A_Green,0)
    SENSOR_Object_df.Rename_df_Column('Green A Mov. Avg [uPa]', 'Green 60s Mov. Avg [Mm^-1]')
    
    SENSOR_Object_df.Linear_Modify_df('Red A Mov. Avg [uPa]', A_Red,0)
    SENSOR_Object_df.Rename_df_Column('Red A Mov. Avg [uPa]', 'Red 60s Mov. Avg [Mm^-1]') 
          
    new_R1, new_Th1 = Amplitude_Phase(SENSOR_Object_df, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')
    SENSOR_Object_df.addSubset_to_df(new_R1/214.7483648,  'R1 [uPa]') # Scale R to uPa
    SENSOR_Object_df.addSubset_to_df(new_Th1, 'Theta1 [deg]') # Theta in deg

    new_R2, new_Th2 = Amplitude_Phase(SENSOR_Object_df, 'X2', 'Y2', 'R2 [uPa]', 'Theta2 [deg]')
    SENSOR_Object_df.addSubset_to_df(new_R2/214.7483648, 'R2 [uPa]') # Scale R to uPa
    SENSOR_Object_df.addSubset_to_df(new_Th2, 'Theta2 [deg]') # Theta in deg
    
    SENSOR_Object_df.df['BKG Meas. Active'] = SENSOR_Object_df.df['BKG Meas. Active'].astype(bool)
    SENSOR_Object_df.df['BKG Meas. Active'] = SENSOR_Object_df.df['BKG Meas. Active'].astype(float)

    return SENSOR_Object_df

def ComPASV5_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def ComPASV5_Post_Script(SENSOR_Object_df):
    return SENSOR_Object_df
    
def SMPS3080_Exp_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def SMPS3080_Exp_Post_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def SMPS3080_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def SMPS3080_Post_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def Aeth33_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def Aeth33_Post_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def Aeth31_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def Aeth31_Post_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def MSPTI_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def MSPTI_Post_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def miniPTI_Pre_Script(SENSOR_Object_df):
    return SENSOR_Object_df

def miniPTI_Post_Script(SENSOR_Object_df):
    return SENSOR_Object_df