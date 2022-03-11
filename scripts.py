from lib import np, pd, allantools

def Amplitude_Phase(SENSOR_Object_df,X_Column,Y_Column,R_Name,Theta_Name):    
    new_R = pd.DataFrame({R_Name: np.sqrt(SENSOR_Object_df.df[X_Column]**2+SENSOR_Object_df.df[Y_Column]**2)},index=SENSOR_Object_df.df.index)
    new_Th = pd.DataFrame({Theta_Name: np.arctan2(SENSOR_Object_df.df[Y_Column],SENSOR_Object_df.df[X_Column])*180.0/np.pi},index=SENSOR_Object_df.df.index)
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
    elif model_name == 'MSPTI_Metas_Export':
        return MSPTI_Metas_Pre_Script(SENSOR_Object)
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
    elif model_name == 'MSPTI_Metas_Export':
        return MSPTI_Metas_Post_Script(SENSOR_Object)
    elif model_name == 'miniPTI':
        return miniPTI_Post_Script(SENSOR_Object)
    else:
        return SENSOR_Object   


def Aeth33_Pre_Script(SENSOR_Object):
    # Method for value hold while Background Measurement active (via value comparison)
    Copy_df = SENSOR_Object.df1.df[['BB', 'BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6', 'BC7']].copy()
    Copy_df.loc[Copy_df['BC3']<0.0000001, Copy_df.columns] = None
    Copy_df = Copy_df.ffill()
    SENSOR_Object.addSubset(Copy_df, ['BB VH', 'BC1 VH', 'BC2 VH', 'BC3 VH', 'BC4 VH', 'BC5 VH', 'BC6 VH', 'BC7 VH'], df_index = 1)
    return SENSOR_Object

def Aeth33_Post_Script(SENSOR_Object):
    return SENSOR_Object


def Aeth31_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def Aeth31_Post_Script(SENSOR_Object):
    return SENSOR_Object


def ComPASV4_Pre_Script(SENSOR_Object):
    # Method to add BKG True for X Seconds after BKG was active:
    BKGS = SENSOR_Object.df1.df['BKG Meas. Active'].astype(bool).copy()
    for indx, val in reversed(list(enumerate(BKGS[:-1]))):
        if val:
            if BKGS[indx+1]==False:
                for indx2 in range(indx,indx+70):
                    # 60 because ComPAS data are 1 second and I want to add 70 seconds more BKG active.
                    if indx2==len(BKGS):
                        break
                    else:
                        BKGS[indx2]=True        
    SENSOR_Object.df1.df['BKG Meas. Active'] = BKGS.astype(bool)                  
                
    
    # Method for value hold while Background Measurement is active (via boolean comparison)
    Copy_df = SENSOR_Object.df1.df[['BKG Meas. Active','X1','Y1','Amplitude 1 [uPa]','Phase 1 [deg]',
                                                'X2','Y2','Amplitude 2 [uPa]','Phase 2 [deg]',
                                                'Blue A Mov. Avg [uPa]','Blue P Mov. Avg [deg]',
                                                'Green A Mov. Avg [uPa]','Green P Mov. Avg [deg]',
                                                'Red A Mov. Avg [uPa]','Red P Mov. Avg [deg]']].copy()
    Copy_df.loc[Copy_df['BKG Meas. Active']>0, Copy_df.columns] = None
    Copy_df = Copy_df.ffill()
    Copy_df.pop('BKG Meas. Active')
    SENSOR_Object.addSubset(Copy_df, ['X1 VH','Y1 VH','Amplitude 1 VH [uPa]', 'Phase 1 VH [deg]', 
                                                'X2 VH','Y2 VH','Amplitude 2 VH [uPa]','Phase 2 VH [deg]',
                                                'Blue A Mov. Avg VH [uPa]', 'Blue P Mov. Avg VH [deg]', 
                                                'Green A Mov. Avg VH [uPa]', 'Green P Mov. Avg VH [deg]', 
                                                'Red A Mov. Avg VH [uPa]', 'Red P Mov. Avg VH [deg]'],
                                                df_index = 1)
    
    return SENSOR_Object

def ComPASV4_Post_Script(SENSOR_Object):
    A_Blue = 1221.5/558.0 
    A_Green = 415.5/203.0
    A_Red = 30.35/4.0
    
    SENSOR_Object.Linear_Modify('Blue A Mov. Avg [uPa]', A_Blue,0,df_index=[1,2])
    SENSOR_Object.Rename_sensor_signal('Blue A Mov. Avg [uPa]', 'Blue A 60s Mov. Avg [Mm^-1]', new_units='Mm^-1',df_index=[1,2])
    
    SENSOR_Object.Linear_Modify('Green A Mov. Avg [uPa]', A_Green,0,df_index=[1,2])
    SENSOR_Object.Rename_sensor_signal('Green A Mov. Avg [uPa]', 'Green A 60s Mov. Avg [Mm^-1]', new_units='Mm^-1',df_index=[1,2])
    
    SENSOR_Object.Linear_Modify('Red A Mov. Avg [uPa]', A_Red,0,df_index=[1,2])
    SENSOR_Object.Rename_sensor_signal('Red A Mov. Avg [uPa]', 'Red A 60s Mov. Avg [Mm^-1]', new_units='Mm^-1',df_index=[1,2]) 
    
    new_R1, new_Th1 = Amplitude_Phase(SENSOR_Object.df2, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')
    SENSOR_Object.addSubset(new_R1/214.7483648, ['R1 [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1, ['Theta1 [deg]'],new_units=['deg'],df_index=2) # Theta in deg

    new_R2, new_Th2 = Amplitude_Phase(SENSOR_Object.df2, 'X2', 'Y2', 'R2 [uPa]', 'Theta2 [deg]')
    SENSOR_Object.addSubset(new_R2/214.7483648, ['R2 [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th2, ['Theta2 [deg]'],new_units=['deg'],df_index=2) # Theta in deg
    
    new_R1_VH, new_Th1_VH = Amplitude_Phase(SENSOR_Object.df2, 'X1 VH', 'Y1 VH', 'R1 VH [uPa]', 'Theta1 VH [deg]')
    SENSOR_Object.addSubset(new_R1_VH/214.7483648, ['R1 VH [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1_VH, ['Theta1 VH [deg]'],new_units=['deg'],df_index=2) # Theta in deg

    new_R2_VH, new_Th2_VH = Amplitude_Phase(SENSOR_Object.df2, 'X2 VH', 'Y2 VH', 'R2 VH [uPa]', 'Theta2 VH [deg]')
    SENSOR_Object.addSubset(new_R2_VH/214.7483648, ['R2 VH [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th2_VH, ['Theta2 VH [deg]'],new_units=['deg'],df_index=2) # Theta in deg
    
    SENSOR_Object.df2.df['BKG Meas. Active'] = SENSOR_Object.df2.df['BKG Meas. Active'].astype(bool)
    SENSOR_Object.df2.df['BKG Meas. Active'] = SENSOR_Object.df2.df['BKG Meas. Active'].astype(float)

    SENSOR_Object.plotkey = 'R1 VH [uPa]'
    
    return SENSOR_Object


def ComPASV5_Pre_Script(SENSOR_Object):  
    return SENSOR_Object

def ComPASV5_Post_Script(SENSOR_Object):
    new_R1, new_Th1 = Amplitude_Phase(SENSOR_Object.df2, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')
    SENSOR_Object.addSubset(new_R1/214.7483648, ['R1 [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1, ['Theta1 [deg]'],new_units=['deg'],df_index=2) # Theta in deg

    new_R2, new_Th2 = Amplitude_Phase(SENSOR_Object.df2, 'X2', 'Y2', 'R2 [uPa]', 'Theta2 [deg]')
    SENSOR_Object.addSubset(new_R2/214.7483648, ['R2 [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th2, ['Theta2 [deg]'],new_units=['deg'],df_index=2) # Theta in deg

    
    # SENSOR_Object.df2.df['BKG Meas. Active'] = SENSOR_Object.df2.df['BKG Meas. Active'].astype(bool)
    # SENSOR_Object.df2.df['BKG Meas. Active'] = SENSOR_Object.df2.df['BKG Meas. Active'].astype(float)

    SENSOR_Object.plotkey = 'R1 [uPa]'

    return SENSOR_Object
    

def PMS_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def PMS_Post_Script(SENSOR_Object):
    return SENSOR_Object


def SMPS3080_Exp_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def SMPS3080_Exp_Post_Script(SENSOR_Object):
    return SENSOR_Object


def SMPS3080_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def SMPS3080_Post_Script(SENSOR_Object):
    return SENSOR_Object


def MSPTI_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def MSPTI_Post_Script(SENSOR_Object):
    return SENSOR_Object

def MSPTI_Metas_Pre_Script(SENSOR_Object):
    SENSOR_Object.df1.df.index = SENSOR_Object.df1.df.index.tz_localize(None)
    return SENSOR_Object

def MSPTI_Metas_Post_Script(SENSOR_Object):
    return SENSOR_Object


def miniPTI_Pre_Script(SENSOR_Object):
    SENSOR_Object.Rename_sensor_signal('60s Norm dphi2 R Vect (V)', '60s Norm dphi2 R Vect (arb)', new_units='')
    SENSOR_Object.Rename_sensor_signal('60s Ernest new (V)', '60s Ernest new (arb)', new_units='')
    return SENSOR_Object

def miniPTI_Post_Script(SENSOR_Object):
    return SENSOR_Object