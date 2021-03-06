from lib import np, pd, allantools, timedelta

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
    elif model_name == 'PAX':
        return PAX_Pre_Script(SENSOR_Object)
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
    elif model_name == 'PAX':
        return PAX_Post_Script(SENSOR_Object)
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
    # Adjust Winter to Summer time
    timelist = SENSOR_Object.df1.df.index.tolist()
    for timeindex in range(len(timelist)):
        timelist[timeindex] += timedelta(hours=1)
    SENSOR_Object.df1.df.index = timelist
    
    # Resample in 10 Seconds interval if needed
    Time_Intervals = '10S' # 10 Seconds
    SENSOR_Object.df1.df = SENSOR_Object.df1.df.resample(Time_Intervals).interpolate()
    
    # Method for value hold while Background Measurement active (via value comparison)
    # Copy_df = SENSOR_Object.df1.df[['BB', 'BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6', 'BC7']].copy()
    # Copy_df.loc[Copy_df['BC3']<0.0000001, Copy_df.columns] = None
    # Copy_df = Copy_df.ffill()
    # SENSOR_Object.addSubset(Copy_df, ['BB VH', 'BC1 VH', 'BC2 VH', 'BC3 VH', 'BC4 VH', 'BC5 VH', 'BC6 VH', 'BC7 VH'], df_index = 1)
    return SENSOR_Object

def Aeth33_Post_Script(SENSOR_Object):
    BC1_Abs = pd.DataFrame({'BC1_Abs': SENSOR_Object.df2.df['BC1'].copy()/1000*1.39/2.7*18.47},index=SENSOR_Object.df2.df.index)
    BC2_Abs = pd.DataFrame({'BC2_Abs': SENSOR_Object.df2.df['BC2'].copy()/1000*1.39/2.7*14.54},index=SENSOR_Object.df2.df.index)
    BC3_Abs = pd.DataFrame({'BC3_Abs': SENSOR_Object.df2.df['BC3'].copy()/1000*1.39/2.7*13.14},index=SENSOR_Object.df2.df.index)
    BC4_Abs = pd.DataFrame({'BC4_Abs': SENSOR_Object.df2.df['BC4'].copy()/1000*1.39/2.7*11.58},index=SENSOR_Object.df2.df.index)
    BC5_Abs = pd.DataFrame({'BC5_Abs': SENSOR_Object.df2.df['BC5'].copy()/1000*1.39/2.7*10.35},index=SENSOR_Object.df2.df.index)
    BC6_Abs = pd.DataFrame({'BC6_Abs': SENSOR_Object.df2.df['BC6'].copy()/1000*1.39/2.7*7.77},index=SENSOR_Object.df2.df.index)
    BC7_Abs = pd.DataFrame({'BC7_Abs': SENSOR_Object.df2.df['BC7'].copy()/1000*1.39/2.7*7.19},index=SENSOR_Object.df2.df.index)
    
    
    SENSOR_Object.addSubset(BC1_Abs, ['BC1 Abs [1/Mm]'],new_units=['1/Mm'],df_index=2) 
    SENSOR_Object.addSubset(BC2_Abs, ['BC2 Abs [1/Mm]'],new_units=['1/Mm'],df_index=2) 
    SENSOR_Object.addSubset(BC3_Abs, ['BC3 Abs [1/Mm]'],new_units=['1/Mm'],df_index=2) 
    SENSOR_Object.addSubset(BC4_Abs, ['BC4 Abs [1/Mm]'],new_units=['1/Mm'],df_index=2) 
    SENSOR_Object.addSubset(BC5_Abs, ['BC5 Abs [1/Mm]'],new_units=['1/Mm'],df_index=2) 
    SENSOR_Object.addSubset(BC6_Abs, ['BC6 Abs [1/Mm]'],new_units=['1/Mm'],df_index=2) 
    SENSOR_Object.addSubset(BC7_Abs, ['BC7 Abs [1/Mm]'],new_units=['1/Mm'],df_index=2) 
    
    SENSOR_Object.plotkey = 'BC3 Abs [1/Mm]'
    
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
    # # Resample to 1s, as it should be at ComPAS
    # Time_Intervals = '1S' # 1 Second
    # SENSOR_Object.df1.df = SENSOR_Object.df1.df.resample(Time_Intervals).interpolate()
    
    
    # Background
    BKGS = SENSOR_Object.df1.df['BKG Meas. Active'].astype(bool).copy()
    BKG_Values_X = SENSOR_Object.df1.df['X1'].copy()
    BKG_Values_Y = SENSOR_Object.df1.df['Y1'].copy()
    
    for indx, val in reversed(list(enumerate(BKGS[:-1]))):
        if indx>=5:
            if not val:
                # All Values where BKG was not active are set to None
                BKG_Values_X[indx] = None
                BKG_Values_Y[indx] = None
            else:
                if BKGS[indx-1] == False:
                    # BKG just started
                    # Watch out units! 1 index is here 1 second.
                    BKG_Values_X[indx-5:indx+120] = None
                    BKG_Values_Y[indx-5:indx+120] = None
                if BKGS[indx+1] == False:
                    # BKG just finished
                    BKG_Values_X[indx-5:indx+5] = None
                    BKG_Values_Y[indx-5:indx+5] = None
        else:
            BKG_Values_X[indx] = None
            BKG_Values_Y[indx] = None
    

    # Not sure wheter rolling mean is smart here...
    BKG_Values_X_df = pd.DataFrame({'X1 BKG': BKG_Values_X},index=SENSOR_Object.df1.df.index).rolling(30).mean().interpolate(method='nearest').ffill().bfill()
    BKG_Values_Y_df = pd.DataFrame({'Y1 BKG': BKG_Values_Y},index=SENSOR_Object.df1.df.index).rolling(30).mean().interpolate(method='nearest').ffill().bfill()
    
    SENSOR_Object.addSubset(BKG_Values_X_df, ['X1 BKG'],new_units=[''],df_index=1)
    SENSOR_Object.addSubset(BKG_Values_Y_df, ['Y1 BKG'],new_units=[''],df_index=1)
    
    SENSOR_Object.signals.append('X1 BKG')
    SENSOR_Object.signals.append('Y1 BKG')
    SENSOR_Object.signals_export.append('X1 BKG')
    SENSOR_Object.signals_export.append('Y1 BKG')
    
    # Subtract Interpolated Datasets
    # Subtracted_Signal_X = SENSOR_Object.df1.df['X1'].copy().ffill().bfill() - SENSOR_Object.df1.df['X1 BKG'].copy().rolling(10).mean().ffill().bfill()
    # Subtracted_Signal_Y = SENSOR_Object.df1.df['Y1'].copy().ffill().bfill() - SENSOR_Object.df1.df['Y1 BKG'].copy().rolling(10).mean().ffill().bfill()

    Subtracted_Signal_X = SENSOR_Object.df1.df['X1'].copy().interpolate().ffill().bfill() - SENSOR_Object.df1.df['X1 BKG'].copy()
    Subtracted_Signal_Y = SENSOR_Object.df1.df['Y1'].copy().interpolate().ffill().bfill() - SENSOR_Object.df1.df['Y1 BKG'].copy()
    
    X1_Sub = pd.DataFrame({'X1 Subtracted': Subtracted_Signal_X},index=SENSOR_Object.df1.df.index)
    Y1_Sub = pd.DataFrame({'Y1 Subtracted': Subtracted_Signal_Y},index=SENSOR_Object.df1.df.index)

    SENSOR_Object.addSubset(X1_Sub, ['X1 Subtracted'],new_units=[''],df_index=1)
    SENSOR_Object.addSubset(Y1_Sub, ['Y1 Subtracted'],new_units=[''],df_index=1)
    
    SENSOR_Object.signals.append('X1 BKG')
    SENSOR_Object.signals.append('Y1 BKG')
    SENSOR_Object.signals_export.append('X1 BKG')
    SENSOR_Object.signals_export.append('Y1 BKG')
    SENSOR_Object.signals.append('X1 Subtracted')
    SENSOR_Object.signals.append('Y1 Subtracted')
    SENSOR_Object.signals_export.append('X1 Subtracted')
    SENSOR_Object.signals_export.append('Y1 Subtracted')
    
    # Method to add BKG True for X Seconds after BKG was active:
    BKGS = SENSOR_Object.df1.df['BKG Meas. Active'].astype(bool).copy()
    for indx, val in reversed(list(enumerate(BKGS[:-1]))):
        if val:
            if BKGS[indx+1]==False:
                for indx2 in range(indx,indx+10):
                    # 60 because ComPAS data are 1 second and I want to add 70 seconds more BKG active.
                    if indx2==len(BKGS):
                        break
                    else:
                        BKGS[indx2]=True 
    SENSOR_Object.df1.df['BKG Meas. Active'] = BKGS.astype(bool)             
    
    
        

    return SENSOR_Object

def ComPASV5_Post_Script(SENSOR_Object):
    # Special Constants
    #Mic_Konstant = 214.7483648
    #Mic_Konstant = 215.2582778
    Mic_Konstant = 68.07064429
    
        
    # Green Channel Absorption Calibration
    Green_Amplitdue_NO2_1ppm = 1550 # uPa
    Green_Absorption_NO2_1ppm = 415.46 # 1/Mm
    
    # Cast Booleans
    BKGS = SENSOR_Object.df2.df['BKG Meas. Active'].astype(bool).copy()
    SENSOR_Object.df2.df['BKG Meas. Active'] = BKGS.tolist()
    
    # Calculate BKG Amplitude and Phase after Average
    new_R1_BKG, new_Th1_BKG = Amplitude_Phase(SENSOR_Object.df2, 'X1 BKG', 'Y1 BKG', 'R1 BKG [uPa]', 'Theta1 BKG [deg]')
    new_R1_BKG = new_R1_BKG/Mic_Konstant
    SENSOR_Object.addSubset(new_R1_BKG, ['R1 BKG [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1_BKG, ['Theta1 BKG [deg]'],new_units=['deg'],df_index=2) # Theta in deg

    # Calculate Signal Amplitude and Phase after Average
    new_R1, new_Th1 = Amplitude_Phase(SENSOR_Object.df2, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')
    new_R1 = new_R1/Mic_Konstant
    SENSOR_Object.addSubset(new_R1, ['R1 [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    # SENSOR_Object.addSubset(new_R1*Green_Absorption_NO2_1ppm/Green_Amplitdue_NO2_1ppm, ['R1 [1/Mm]'],new_units=['1/Mm'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1, ['Theta1 [deg]'],new_units=['deg'],df_index=2) # Theta in deg

    new_R2, new_Th2 = Amplitude_Phase(SENSOR_Object.df2, 'X2', 'Y2', 'R2 [uPa]', 'Theta2 [deg]')
    new_R2 = new_R2/Mic_Konstant
    SENSOR_Object.addSubset(new_R2, ['R2 [uPa]'],new_units=['uPa'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th2, ['Theta2 [deg]'],new_units=['deg'],df_index=2) # Theta in deg

    # Remove Signal Datas during BKG and fill them with linear interpolation
    R1_uPa_Copy = SENSOR_Object.df2.df['R1 [uPa]'].copy()
    # R1_Mm_Copy = SENSOR_Object.df2.df['R1 [1/Mm]'].copy()
    Theta1_Copy = SENSOR_Object.df2.df['Theta1 [deg]'].copy()
    
    for indx,val in enumerate(BKGS):
        if val:
            R1_uPa_Copy[indx] = None
            # R1_Mm_Copy[indx] = None
            Theta1_Copy[indx] = None  
            
    SENSOR_Object.df2.df['R1 [uPa]'] = R1_uPa_Copy
    # SENSOR_Object.df2.df['R1 [1/Mm]'] = R1_Mm_Copy
    SENSOR_Object.df2.df['Theta1 [deg]'] = Theta1_Copy
    
    SENSOR_Object.df2.df['R1 [uPa]'] = SENSOR_Object.df2.df['R1 [uPa]'].interpolate().ffill().bfill()
    # SENSOR_Object.df2.df['R1 [1/Mm]'] = SENSOR_Object.df2.df['R1 [1/Mm]'].interpolate().ffill().bfill()
    SENSOR_Object.df2.df['Theta1 [deg]'] = SENSOR_Object.df2.df['Theta1 [deg]'].interpolate().ffill().bfill()
    
    
    # Calculate Signals after Average: Already subtracted X and Y BKGs in Pre-Script
    Subtracted_Signal_X = SENSOR_Object.df2.df['X1 Subtracted']
    Subtracted_Signal_Y = SENSOR_Object.df2.df['Y1 Subtracted']
    
    Calc_R = pd.DataFrame({'R1 BKG Subtracted [1/Mm]': np.sqrt(Subtracted_Signal_X**2+Subtracted_Signal_Y**2)},index=SENSOR_Object.df2.df.index)
    Calc_Theta = pd.DataFrame({'Theta1 BKG Subtracted [deg]': np.arctan2(Subtracted_Signal_Y,Subtracted_Signal_X)*180.0/np.pi},index=SENSOR_Object.df2.df.index)
    Calc_R = Calc_R/Mic_Konstant*Green_Absorption_NO2_1ppm/Green_Amplitdue_NO2_1ppm
    
    # Remove Signal Datas during BKG and fill them with linear interpolation
    for indx,val in enumerate(BKGS):
        if val:
            Calc_R['R1 BKG Subtracted [1/Mm]'][indx] = None
            Calc_Theta['Theta1 BKG Subtracted [deg]'][indx] = None
    
    Calc_R = Calc_R.interpolate().ffill().bfill()
    Calc_Theta = Calc_Theta.interpolate().ffill().bfill()
    
    SENSOR_Object.addSubset(Calc_R, ['R1 BKG Subtracted [1/Mm]'],new_units=['1/Mm'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(Calc_Theta, ['Theta1 BKG Subtracted [deg]'],new_units=['deg'],df_index=2) # Theta in deg


    # Calculate Signal with given Datasets in ComPAS (after average). X(or Y) Green/Blue/red are already background subtracted within LabView.
    new_R1_Green, new_Th1_Green = Amplitude_Phase(SENSOR_Object.df2, 'X Green [a.u.]', 'Y Green [a.u.]', 'R1_Green [1/Mm]', 'Theta1_Green [deg]')
    new_R1_Green = new_R1_Green/Mic_Konstant*Green_Absorption_NO2_1ppm/Green_Amplitdue_NO2_1ppm
    SENSOR_Object.addSubset(new_R1_Green, ['R1_Green [1/Mm]'],new_units=['1/Mm'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1_Green, ['Theta1_Green [deg]'],new_units=['deg'],df_index=2) # Theta in deg

    new_R1_BKG_Green, new_Th1_BKG_Green = Amplitude_Phase(SENSOR_Object.df2, 'X BKG Green [a.u.]', 'Y BKG Green [a.u.]', 'R1_BKG_Green [1/Mm]', 'Theta1_BKG_Green [deg]')
    new_R1_BKG_Green/Mic_Konstant*Green_Absorption_NO2_1ppm/Green_Amplitdue_NO2_1ppm
    SENSOR_Object.addSubset(new_R1_BKG_Green, ['R1_BKG_Green [1/Mm]'],new_units=['1/Mm'],df_index=2) # Scale R to uPa
    SENSOR_Object.addSubset(new_Th1_BKG_Green, ['Theta1_BKG_Green [deg]'],new_units=['deg'],df_index=2) # Theta in deg
    
    # Cast Booleans
    BKGS = SENSOR_Object.df2.df['BKG Meas. Active'].astype(int).copy()
    SENSOR_Object.df2.df['BKG Meas. Active'] = BKGS.tolist()    
    
    # Other Stuff 
    # SENSOR_Object.df2.df['BKG Meas. Active'] = SENSOR_Object.df2.df['BKG Meas. Active'].astype(bool)
    # SENSOR_Object.df2.df['BKG Meas. Active'] = SENSOR_Object.df2.df['BKG Meas. Active'].astype(float)

    # SENSOR_Object.plotkey = 'R1 [1/Mm]'
    SENSOR_Object.plotkey ='R1 BKG Subtracted [1/Mm]'

    return SENSOR_Object

def PAX_Pre_Script(SENSOR_Object):
    Time_Intervals = '10S' # 10 Seconds
    SENSOR_Object.df1.df = SENSOR_Object.df1.df.resample(Time_Intervals).interpolate()
    # PAX is not recording data when in BKG/Filter modus, therefore resampling is needed and values are interpolated (linear).
    return SENSOR_Object

def PAX_Post_Script(SENSOR_Object):
    return SENSOR_Object


def PMS_Pre_Script(SENSOR_Object):
    return SENSOR_Object

def PMS_Post_Script(SENSOR_Object):
    return SENSOR_Object


def SMPS3080_Exp_Pre_Script(SENSOR_Object):
    Time_Intervals = '60S' # 10 Second
    SENSOR_Object.df1.df = SENSOR_Object.df1.df.resample(Time_Intervals).pad().interpolate().ffill().bfill()
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