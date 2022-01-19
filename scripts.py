from lib import np, pd

def Amplitude_Phase(sensor_df,X_Column,Y_Column,R_Name,Theta_Name):    
    new_R = pd.DataFrame({R_Name: np.sqrt(sensor_df.df[X_Column]**2+sensor_df.df[Y_Column]**2)},index=sensor_df.df.index)
    new_Th = pd.DataFrame({Theta_Name: np.arctan2(sensor_df.df[Y_Column],sensor_df.df[X_Column])*180.0/np.pi},index=sensor_df.df.index)
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
    elif model_name == 'MSPTI_Export':
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
    elif model_name == 'MSPTI_Export':
        return MSPTI_Post_Script(SENSOR_Object)
    elif model_name == 'miniPTI':
        return miniPTI_Post_Script(SENSOR_Object)
    else:
        return SENSOR_Object   


def PMS_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def PMS_Post_Script(SENSOR_Object):
    # SENSOR_Object.Linear_Modify('Concentration ug/m3', 1000,0)
    # SENSOR_Object.Rename_sensor_signals('Concentration ug/m3', 'Concentration ng/m3', 'ng/m$^3$')
    return SENSOR_Object


def ComPASV4_Pre_Script(SENSOR_Object):
    # This is my custom script and it's not finished yet.
    
    # BKG_Bools_All = SENSOR_Object.df1.df['BKG Meas. Active'].astype(bool)
    # BKG_Bools_All_NOT = abs(SENSOR_Object.df1.df['BKG Meas. Active']-1.0).astype(bool)
    
    # Blue_A_Copy = pd.DataFrame(SENSOR_Object.df1.df['Blue A Mov. Avg [uPa]'],index=SENSOR_Object.df1.df.index)
    
    # SENSOR_Object.addSubset(Blue_A_Copy, 'Blue A Mov. Avg BKG [uPa]', 'uPa', df_index = 1)

    # SENSOR_Object.Linear_Modify('Blue A Mov. Avg [uPa]', BKG_Bools_All_NOT.astype(float),0, 1)
    # SENSOR_Object.Linear_Modify('Blue A Mov. Avg BKG [uPa]', BKG_Bools_All.astype(float),0, 1)
    
    return SENSOR_Object

def ComPASV4_Post_Script(SENSOR_Object):
    # This is my custom script and it's not finished yet.
        
    # Add new Columns and Calibrate  
    # Blue:
    A_Blue = 1221.5/558.0 
    # Green
    A_Green = 415.5/203.0
    # Red
    A_Red = 30.35/4.0
    
    SENSOR_Object.Linear_Modify('Blue A Mov. Avg [uPa]', A_Blue,0)
    SENSOR_Object.Rename_sensor_signals('Blue A Mov. Avg [uPa]', 'Blue 60s Mov. Avg [Mm^-1]', 'Mm$^-1$')
    
    SENSOR_Object.Linear_Modify('Green A Mov. Avg [uPa]', A_Green,0)
    SENSOR_Object.Rename_sensor_signals('Green A Mov. Avg [uPa]', 'Green 60s Mov. Avg [Mm^-1]', 'Mm$^-1$')
    
    SENSOR_Object.Linear_Modify('Red A Mov. Avg [uPa]', A_Red,0)
    SENSOR_Object.Rename_sensor_signals('Red A Mov. Avg [uPa]', 'Red 60s Mov. Avg [Mm^-1]', 'Mm$^-1$') 
          
    new_R1, new_Th1 = Amplitude_Phase(SENSOR_Object.df2, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')
    SENSOR_Object.addSubset(new_R1/214.7483648,  ['R1 [uPa]'], ['uPa'], df_index = [2,3]) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1, ['Theta1 [deg]'], ['deg'], df_index = [2,3]) # Theta in deg


    new_R2, new_Th2 = Amplitude_Phase(SENSOR_Object.df2, 'X2', 'Y2', 'R2 [uPa]', 'Theta2 [deg]')
    SENSOR_Object.addSubset(new_R2/214.7483648, ['R2 [uPa]'], ['uPa'], df_index = [2,3]) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th2, ['Theta2 [deg]'], ['deg'], df_index = [2,3]) # Theta in deg
    
    SENSOR_Object.plotkey = 'R1 [uPa]'
    
    SENSOR_Object.df2.df['BKG Meas. Active'] = SENSOR_Object.df2.df['BKG Meas. Active'].astype(bool)
    SENSOR_Object.df3.df['BKG Meas. Active'] = SENSOR_Object.df3.df['BKG Meas. Active'].astype(bool)
    
    SENSOR_Object.df2.df['BKG Meas. Active'] = SENSOR_Object.df2.df['BKG Meas. Active'].astype(float)
    SENSOR_Object.df3.df['BKG Meas. Active'] = SENSOR_Object.df3.df['BKG Meas. Active'].astype(float)
    
    # BKG_Bools = SENSOR_Object.df2.df['BKG Meas. Active']
    # Lockin_X1 = SENSOR_Object.df2.df['X1']
    # Lockin_Y1 = SENSOR_Object.df2.df['Y1']
    # Lockin_R1 = SENSOR_Object.df2.df['R1 [uPa]']
    # Lockin_T1 = SENSOR_Object.df2.df['Theta1 [deg]']
    
    # SENSOR_Object.addSubset([Lockin_R1[indx] if val else None for indx,val in enumerate(BKG_Bools)],'R1_BKG [uPa]', 'uPa', df_index = [2,3])
    # SENSOR_Object.addSubset([Lockin_T1[indx] if val else None for indx,val in enumerate(BKG_Bools)],'Theta1_BKG [deg]', 'deg', df_index = [2,3])
    
    # Ampl_Blue_60s = SENSOR_Object.df2.df['Blue A Mov. Avg [uPa]']
    # Phase_Blue_60s = SENSOR_Object.df2.df['Blue P Mov. Avg [deg]']
    # Ampl_Green_60s = SENSOR_Object.df2.df['Green A Mov. Avg [uPa]']
    # Phase_Green_60s = SENSOR_Object.df2.df['Green P Mov. Avg [deg]']
    # Ampl_Red_60s = SENSOR_Object.df2.df['Red A Mov. Avg [uPa]']
    # Phase_Red_60s = SENSOR_Object.df2.df['Red P Mov. Avg [deg]']
    
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
    SENSOR_Object.Rename_sensor_signals('60s Ernest new (V)', '60s Ernest new (arb)')
    return SENSOR_Object

def miniPTI_Post_Script(SENSOR_Object):
    return SENSOR_Object