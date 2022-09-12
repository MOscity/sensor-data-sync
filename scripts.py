from lib import np, pd, allantools, timedelta


def Amplitude_Phase(sensorObjectDf, X_Column, Y_Column, R_Name, Theta_Name):
    new_R = pd.DataFrame({R_Name: np.sqrt(
        sensorObjectDf.df[X_Column]**2+sensorObjectDf.df[Y_Column]**2)}, index=sensorObjectDf.df.index)
    new_Th = pd.DataFrame({Theta_Name: np.arctan2(
        sensorObjectDf.df[Y_Column], sensorObjectDf.df[X_Column])*180.0/np.pi}, index=sensorObjectDf.df.index)
    return new_R, new_Th


def CheckPreScripts(sensorObject):
    modelName = sensorObject.modelName
    if modelName == 'AE33':
        return Aeth33PreScript(sensorObject)
    elif modelName == 'AE31':
        return Aeth31PreScript(sensorObject)
    elif modelName == 'PMS1':
        return PMSPreScript(sensorObject)
    elif modelName == 'ComPAS-V4':
        return ComPASV4PreScript(sensorObject)
    elif modelName == 'ComPAS-V5':
        return ComPASV5PreScript(sensorObject)
    elif modelName == 'PAX':
        return PAXPreScript(sensorObject)
    elif modelName == 'SMPS3080_Export':
        return SMPS3080_ExpPreScript(sensorObject)
    elif modelName == 'SMPS3080':
        return SMPS3080PreScript(sensorObject)
    elif modelName == 'MSPTI_Export':
        return MSPTIPreScript(sensorObject)
    elif modelName == 'MSPTI_Metas_Export':
        return MSPTI_MetasPreScript(sensorObject)
    elif modelName == 'miniPTI':
        return miniPTIPreScript(sensorObject)
    elif modelName == 'TempSensor':
        return TempSensorPreScript(sensorObject)
    else:
        return sensorObject


def CheckPostScripts(sensorObject):
    modelName = sensorObject.modelName
    if modelName == 'AE33':
        return Aeth33PostScript(sensorObject)
    elif modelName == 'AE31':
        return Aeth31PostScript(sensorObject)
    elif modelName == 'PMS1':
        return PMSPostScript(sensorObject)
    elif modelName == 'ComPAS-V4':
        return ComPASV4PostScript(sensorObject)
    elif modelName == 'ComPAS-V5':
        return ComPASV5PostScript(sensorObject)
    elif modelName == 'PAX':
        return PAXPostScript(sensorObject)
    elif modelName == 'SMPS3080_Export':
        return SMPS3080_ExpPostScript(sensorObject)
    elif modelName == 'SMPS3080':
        return SMPS3080PostScript(sensorObject)
    elif modelName == 'MSPTI_Export':
        return MSPTIPostScript(sensorObject)
    elif modelName == 'MSPTI_Metas_Export':
        return MSPTI_MetasPostScript(sensorObject)
    elif modelName == 'miniPTI':
        return miniPTIPostScript(sensorObject)
    elif modelName == 'TempSensor':
        return TempSensorPostScript(sensorObject)
    else:
        return sensorObject


def Aeth33PreScript(sensorObject):
    # Adjust Winter to Summer time
    timelist = sensorObject.df1.df.index.tolist()
    for timeindex in range(len(timelist)):
        timelist[timeindex] += timedelta(hours=1)
    sensorObject.df1.df.index = timelist

    # Resample in 10 Seconds interval if needed
    timeIntervals = '10S'  # 10 Seconds
    sensorObject.df1.df = sensorObject.df1.df.resample(
        timeIntervals).interpolate()

    # Method for value hold while Background Measurement active (via value comparison)
    # Copy_df = sensorObject.df1.df[['BB', 'BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6', 'BC7']].copy()
    # Copy_df.loc[Copy_df['BC3']<0.0000001, Copy_df.columns] = None
    # Copy_df = Copy_df.ffill()
    # sensorObject.addSubset(Copy_df, ['BB VH', 'BC1 VH', 'BC2 VH', 'BC3 VH', 'BC4 VH', 'BC5 VH', 'BC6 VH', 'BC7 VH'], dfIndex = 1)
    return sensorObject


def Aeth33PostScript(sensorObject):
    BC1_Abs = pd.DataFrame({'BC1_Abs': sensorObject.df2.df['BC1'].copy(
    )/1000*1.39/2.7*18.47}, index=sensorObject.df2.df.index)
    BC2_Abs = pd.DataFrame({'BC2_Abs': sensorObject.df2.df['BC2'].copy(
    )/1000*1.39/2.7*14.54}, index=sensorObject.df2.df.index)
    BC3_Abs = pd.DataFrame({'BC3_Abs': sensorObject.df2.df['BC3'].copy(
    )/1000*1.39/2.7*13.14}, index=sensorObject.df2.df.index)
    BC4_Abs = pd.DataFrame({'BC4_Abs': sensorObject.df2.df['BC4'].copy(
    )/1000*1.39/2.7*11.58}, index=sensorObject.df2.df.index)
    BC5_Abs = pd.DataFrame({'BC5_Abs': sensorObject.df2.df['BC5'].copy(
    )/1000*1.39/2.7*10.35}, index=sensorObject.df2.df.index)
    BC6_Abs = pd.DataFrame({'BC6_Abs': sensorObject.df2.df['BC6'].copy(
    )/1000*1.39/2.7*7.77}, index=sensorObject.df2.df.index)
    BC7_Abs = pd.DataFrame({'BC7_Abs': sensorObject.df2.df['BC7'].copy(
    )/1000*1.39/2.7*7.19}, index=sensorObject.df2.df.index)

    sensorObject.addSubset(
        BC1_Abs, ['BC1 Abs [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)
    sensorObject.addSubset(
        BC2_Abs, ['BC2 Abs [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)
    sensorObject.addSubset(
        BC3_Abs, ['BC3 Abs [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)
    sensorObject.addSubset(
        BC4_Abs, ['BC4 Abs [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)
    sensorObject.addSubset(
        BC5_Abs, ['BC5 Abs [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)
    sensorObject.addSubset(
        BC6_Abs, ['BC6 Abs [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)
    sensorObject.addSubset(
        BC7_Abs, ['BC7 Abs [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)

    sensorObject.plotColumn = 'BC3 Abs [1/Mm]'

    return sensorObject


def Aeth31PreScript(sensorObject):
    return sensorObject


def Aeth31PostScript(sensorObject):
    return sensorObject


def TempSensorPreScript(sensorObject):
    sensorObject.plotColumn = 'Temperature Difference [K]'
    return sensorObject


def TempSensorPostScript(sensorObject):
    return sensorObject


def ComPASV4PreScript(sensorObject):

    # Method to add BKG True for X Seconds after BKG was active:
    BKGS = sensorObject.df1.df['BKG Meas. Active'].astype(bool).copy()
    for index, value in reversed(list(enumerate(BKGS[:-1]))):
        if value:
            if BKGS[index+1] == False:
                for indx2 in range(index, index+70):
                    # 60 because ComPAS data are 1 second and I want to add 70 seconds more BKG active.
                    if indx2 == len(BKGS):
                        break
                    else:
                        BKGS[indx2] = True
    sensorObject.df1.df['BKG Meas. Active'] = BKGS.astype(bool)

    # Method for value hold while Background Measurement is active (via boolean comparison)
    Copy_df = sensorObject.df1.df[['BKG Meas. Active', 'X1', 'Y1', 'Amplitude 1 [uPa]', 'Phase 1 [deg]',
                                   'X2', 'Y2', 'Amplitude 2 [uPa]', 'Phase 2 [deg]',
                                   'Blue A Mov. Avg [uPa]', 'Blue P Mov. Avg [deg]',
                                   'Green A Mov. Avg [uPa]', 'Green P Mov. Avg [deg]',
                                   'Red A Mov. Avg [uPa]', 'Red P Mov. Avg [deg]']].copy()
    Copy_df.loc[Copy_df['BKG Meas. Active'] > 0, Copy_df.columns] = None
    Copy_df = Copy_df.ffill()
    Copy_df.pop('BKG Meas. Active')
    sensorObject.addSubset(Copy_df, ['X1 VH', 'Y1 VH', 'Amplitude 1 VH [uPa]', 'Phase 1 VH [deg]',
                                     'X2 VH', 'Y2 VH', 'Amplitude 2 VH [uPa]', 'Phase 2 VH [deg]',
                                     'Blue A Mov. Avg VH [uPa]', 'Blue P Mov. Avg VH [deg]',
                                     'Green A Mov. Avg VH [uPa]', 'Green P Mov. Avg VH [deg]',
                                     'Red A Mov. Avg VH [uPa]', 'Red P Mov. Avg VH [deg]'],
                           dfIndex=1)

    return sensorObject


def ComPASV4PostScript(sensorObject):
    A_Blue = 1221.5/558.0
    A_Green = 415.5/203.0
    A_Red = 30.35/4.0

    sensorObject.LinearModify(
        'Blue A Mov. Avg [uPa]', A_Blue, 0, dfIndex=[1, 2])
    sensorObject.renameColumnInSensorDf(
        'Blue A Mov. Avg [uPa]', 'Blue A 60s Mov. Avg [Mm^-1]', newUnits='Mm^-1', dfIndex=[1, 2])

    sensorObject.LinearModify(
        'Green A Mov. Avg [uPa]', A_Green, 0, dfIndex=[1, 2])
    sensorObject.renameColumnInSensorDf(
        'Green A Mov. Avg [uPa]', 'Green A 60s Mov. Avg [Mm^-1]', newUnits='Mm^-1', dfIndex=[1, 2])

    sensorObject.LinearModify(
        'Red A Mov. Avg [uPa]', A_Red, 0, dfIndex=[1, 2])
    sensorObject.renameColumnInSensorDf(
        'Red A Mov. Avg [uPa]', 'Red A 60s Mov. Avg [Mm^-1]', newUnits='Mm^-1', dfIndex=[1, 2])

    new_R1, new_Th1 = Amplitude_Phase(
        sensorObject.df2, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')
    sensorObject.addSubset(
        new_R1/214.7483648, ['R1 [uPa]'], newUnits=['uPa'], dfIndex=2)  # Scale R to uPa
    sensorObject.addSubset(new_Th1, ['Theta1 [deg]'], newUnits=[
        'deg'], dfIndex=2)  # Theta in deg

    new_R2, new_Th2 = Amplitude_Phase(
        sensorObject.df2, 'X2', 'Y2', 'R2 [uPa]', 'Theta2 [deg]')
    sensorObject.addSubset(
        new_R2/214.7483648, ['R2 [uPa]'], newUnits=['uPa'], dfIndex=2)  # Scale R to uPa
    sensorObject.addSubset(new_Th2, ['Theta2 [deg]'], newUnits=[
        'deg'], dfIndex=2)  # Theta in deg

    new_R1_VH, new_Th1_VH = Amplitude_Phase(
        sensorObject.df2, 'X1 VH', 'Y1 VH', 'R1 VH [uPa]', 'Theta1 VH [deg]')
    sensorObject.addSubset(
        new_R1_VH/214.7483648, ['R1 VH [uPa]'], newUnits=['uPa'], dfIndex=2)  # Scale R to uPa
    sensorObject.addSubset(new_Th1_VH, ['Theta1 VH [deg]'], newUnits=[
        'deg'], dfIndex=2)  # Theta in deg

    new_R2_VH, new_Th2_VH = Amplitude_Phase(
        sensorObject.df2, 'X2 VH', 'Y2 VH', 'R2 VH [uPa]', 'Theta2 VH [deg]')
    sensorObject.addSubset(
        new_R2_VH/214.7483648, ['R2 VH [uPa]'], newUnits=['uPa'], dfIndex=2)  # Scale R to uPa
    sensorObject.addSubset(new_Th2_VH, ['Theta2 VH [deg]'], newUnits=[
        'deg'], dfIndex=2)  # Theta in deg

    sensorObject.df2.df['BKG Meas. Active'] = sensorObject.df2.df['BKG Meas. Active'].astype(
        bool)
    sensorObject.df2.df['BKG Meas. Active'] = sensorObject.df2.df['BKG Meas. Active'].astype(
        float)

    sensorObject.plotColumn = 'R1 VH [uPa]'

    return sensorObject


def ComPASV5PreScript(sensorObject):
    # # Resample to 1s, as it should be at ComPAS
    # timeIntervals = '1S' # 1 Second
    # sensorObject.df1.df = sensorObject.df1.df.resample(timeIntervals).interpolate()
    AnyBKG = False

    # Background
    BKGS = sensorObject.df1.df['BKG Meas. Active'].astype(bool).copy()
    AnyBKG = BKGS.sum().astype(bool)

    if AnyBKG:
        BKG_Values_X = sensorObject.df1.df['X1'].copy()
        BKG_Values_Y = sensorObject.df1.df['Y1'].copy()

        for index, value in reversed(list(enumerate(BKGS[:-1]))):
            if index >= 5:
                if not value:
                    # All Values where BKG was not active are set to None
                    BKG_Values_X[index] = None
                    BKG_Values_Y[index] = None
                else:
                    if BKGS[index-1] == False:
                        # BKG just started
                        # Watch out units! 1 index is here 1 second.
                        BKG_Values_X[index-5:index+120] = None
                        BKG_Values_Y[index-5:index+120] = None
                    if BKGS[index+1] == False:
                        # BKG just finished
                        BKG_Values_X[index-5:index+5] = None
                        BKG_Values_Y[index-5:index+5] = None
            else:
                BKG_Values_X[index] = None
                BKG_Values_Y[index] = None

        # Not sure wheter rolling mean is smart here...
        BKG_Values_X_df = pd.DataFrame({'X1 BKG': BKG_Values_X}, index=sensorObject.df1.df.index).rolling(
            30).mean().interpolate(method='nearest').ffill().bfill()
        BKG_Values_Y_df = pd.DataFrame({'Y1 BKG': BKG_Values_Y}, index=sensorObject.df1.df.index).rolling(
            30).mean().interpolate(method='nearest').ffill().bfill()

        sensorObject.addSubset(
            BKG_Values_X_df, ['X1 BKG'], newUnits=[''], dfIndex=1)
        sensorObject.addSubset(
            BKG_Values_Y_df, ['Y1 BKG'], newUnits=[''], dfIndex=1)

        sensorObject.signals.append('X1 BKG')
        sensorObject.signals.append('Y1 BKG')
        sensorObject.signalsForExport.append('X1 BKG')
        sensorObject.signalsForExport.append('Y1 BKG')

        # Subtract Interpolated Datasets
        # Subtracted_Signal_X = sensorObject.df1.df['X1'].copy().ffill().bfill() - sensorObject.df1.df['X1 BKG'].copy().rolling(10).mean().ffill().bfill()
        # Subtracted_Signal_Y = sensorObject.df1.df['Y1'].copy().ffill().bfill() - sensorObject.df1.df['Y1 BKG'].copy().rolling(10).mean().ffill().bfill()

        Subtracted_Signal_X = sensorObject.df1.df['X1'].copy().interpolate(
        ).ffill().bfill() - sensorObject.df1.df['X1 BKG'].copy()
        Subtracted_Signal_Y = sensorObject.df1.df['Y1'].copy().interpolate(
        ).ffill().bfill() - sensorObject.df1.df['Y1 BKG'].copy()

        X1_Sub = pd.DataFrame(
            {'X1 Subtracted': Subtracted_Signal_X}, index=sensorObject.df1.df.index)
        Y1_Sub = pd.DataFrame(
            {'Y1 Subtracted': Subtracted_Signal_Y}, index=sensorObject.df1.df.index)

        sensorObject.addSubset(
            X1_Sub, ['X1 Subtracted'], newUnits=[''], dfIndex=1)
        sensorObject.addSubset(
            Y1_Sub, ['Y1 Subtracted'], newUnits=[''], dfIndex=1)

        sensorObject.signals.append('X1 BKG')
        sensorObject.signals.append('Y1 BKG')
        sensorObject.signalsForExport.append('X1 BKG')
        sensorObject.signalsForExport.append('Y1 BKG')
        sensorObject.signals.append('X1 Subtracted')
        sensorObject.signals.append('Y1 Subtracted')
        sensorObject.signalsForExport.append('X1 Subtracted')
        sensorObject.signalsForExport.append('Y1 Subtracted')

        # Method to add BKG True for X Seconds after BKG was active:
        BKGS = sensorObject.df1.df['BKG Meas. Active'].astype(bool).copy()
        for index, value in reversed(list(enumerate(BKGS[:-1]))):
            if value:
                if BKGS[index+1] == False:
                    for indx2 in range(index, index+10):
                        # 60 because ComPAS data are 1 second and I want to add 70 seconds more BKG active.
                        if indx2 == len(BKGS):
                            break
                        else:
                            BKGS[indx2] = True
        sensorObject.df1.df['BKG Meas. Active'] = BKGS.astype(bool)

    return sensorObject


def ComPASV5PostScript(sensorObject):
    # Special Constants
    #Mic_Konstant = 214.7483648
    #Mic_Konstant = 215.2582778
    Mic_Konstant = 68.07064429

    # Green Channel Absorption Calibration
    Green_Amplitdue_NO2_1ppm = 1250  # uPa
    # Green_Amplitdue_NO2_1ppm = 1620 # uPa
    Green_Absorption_NO2_1ppm = 415.46  # 1/Mm

    AnyBKG = False
    # Cast Booleans
    BKGS = sensorObject.df2.df['BKG Meas. Active'].astype(bool).copy()
    sensorObject.df2.df['BKG Meas. Active'] = BKGS.tolist()

    AnyBKG = BKGS.sum().astype(bool)

    if AnyBKG:
        # Calculate BKG Amplitude and Phase after Average
        new_R1_BKG, new_Th1_BKG = Amplitude_Phase(
            sensorObject.df2, 'X1 BKG', 'Y1 BKG', 'R1 BKG [uPa]', 'Theta1 BKG [deg]')
        new_R1_BKG = new_R1_BKG/Mic_Konstant
        sensorObject.addSubset(new_R1_BKG, ['R1 BKG [uPa]'], newUnits=[
            'uPa'], dfIndex=2)  # Scale R to uPa
        sensorObject.addSubset(new_Th1_BKG, ['Theta1 BKG [deg]'], newUnits=[
            'deg'], dfIndex=2)  # Theta in deg

    # Calculate Signal Amplitude and Phase after Average
    new_R1, new_Th1 = Amplitude_Phase(
        sensorObject.df2, 'X1', 'Y1', 'R1 [uPa]', 'Theta1 [deg]')
    new_R1 = new_R1/Mic_Konstant
    sensorObject.addSubset(new_R1, ['R1 [uPa]'], newUnits=[
        'uPa'], dfIndex=2)  # Scale R to uPa
    # sensorObject.addSubset(new_R1*Green_Absorption_NO2_1ppm/Green_Amplitdue_NO2_1ppm, ['R1 [1/Mm]'],newUnits=['1/Mm'],dfIndex=2) # Scale R to uPa
    sensorObject.addSubset(new_Th1, ['Theta1 [deg]'], newUnits=[
        'deg'], dfIndex=2)  # Theta in deg

    new_R2, new_Th2 = Amplitude_Phase(
        sensorObject.df2, 'X2', 'Y2', 'R2 [uPa]', 'Theta2 [deg]')
    new_R2 = new_R2/Mic_Konstant
    sensorObject.addSubset(new_R2, ['R2 [uPa]'], newUnits=[
        'uPa'], dfIndex=2)  # Scale R to uPa
    sensorObject.addSubset(new_Th2, ['Theta2 [deg]'], newUnits=[
        'deg'], dfIndex=2)  # Theta in deg

    if AnyBKG:
        # Remove Signal Datas during BKG and fill them with linear interpolation
        R1_uPa_Copy = sensorObject.df2.df['R1 [uPa]'].copy()
        # R1_Mm_Copy = sensorObject.df2.df['R1 [1/Mm]'].copy()
        Theta1_Copy = sensorObject.df2.df['Theta1 [deg]'].copy()

        for index, value in enumerate(BKGS):
            if value:
                R1_uPa_Copy[index] = None
                # R1_Mm_Copy[index] = None
                Theta1_Copy[index] = None

        sensorObject.df2.df['R1 [uPa]'] = R1_uPa_Copy
        # sensorObject.df2.df['R1 [1/Mm]'] = R1_Mm_Copy
        sensorObject.df2.df['Theta1 [deg]'] = Theta1_Copy

        sensorObject.df2.df['R1 [uPa]'] = sensorObject.df2.df['R1 [uPa]'].interpolate(
        ).ffill().bfill()
        # sensorObject.df2.df['R1 [1/Mm]'] = sensorObject.df2.df['R1 [1/Mm]'].interpolate().ffill().bfill()
        sensorObject.df2.df['Theta1 [deg]'] = sensorObject.df2.df['Theta1 [deg]'].interpolate(
        ).ffill().bfill()

        # Calculate Signals after Average: Already subtracted X and Y BKGs in Pre-Script
        Subtracted_Signal_X = sensorObject.df2.df['X1 Subtracted']
        Subtracted_Signal_Y = sensorObject.df2.df['Y1 Subtracted']

        Calc_R = pd.DataFrame({'R1 BKG Subtracted [1/Mm]': np.sqrt(
            Subtracted_Signal_X**2+Subtracted_Signal_Y**2)}, index=sensorObject.df2.df.index)
        Calc_Theta = pd.DataFrame({'Theta1 BKG Subtracted [deg]': np.arctan2(
            Subtracted_Signal_Y, Subtracted_Signal_X)*180.0/np.pi}, index=sensorObject.df2.df.index)
        Calc_R = Calc_R/Mic_Konstant*Green_Absorption_NO2_1ppm/Green_Amplitdue_NO2_1ppm

        # Remove Signal Datas during BKG and fill them with linear interpolation
        for index, value in enumerate(BKGS):
            if value:
                Calc_R['R1 BKG Subtracted [1/Mm]'][index] = None
                Calc_Theta['Theta1 BKG Subtracted [deg]'][index] = None

        Calc_R = Calc_R.interpolate().ffill().bfill()
        Calc_Theta = Calc_Theta.interpolate().ffill().bfill()

        sensorObject.addSubset(Calc_R, [
            'R1 BKG Subtracted [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)  # Scale R to uPa
        sensorObject.addSubset(Calc_Theta, ['Theta1 BKG Subtracted [deg]'], newUnits=[
            'deg'], dfIndex=2)  # Theta in deg

        # Calculate Signal with given Datasets in ComPAS (after average). X(or Y) Green/Blue/red are already background subtracted within LabView.
        new_R1_Green, new_Th1_Green = Amplitude_Phase(
            sensorObject.df2, 'X Green [a.u.]', 'Y Green [a.u.]', 'R1_Green [1/Mm]', 'Theta1_Green [deg]')
        new_R1_Green = new_R1_Green/Mic_Konstant * \
            Green_Absorption_NO2_1ppm/Green_Amplitdue_NO2_1ppm
        sensorObject.addSubset(new_R1_Green, [
            'R1_Green [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)  # Scale R to uPa
        sensorObject.addSubset(new_Th1_Green, ['Theta1_Green [deg]'], newUnits=[
            'deg'], dfIndex=2)  # Theta in deg

        new_R1_BKG_Green, new_Th1_BKG_Green = Amplitude_Phase(
            sensorObject.df2, 'X BKG Green [a.u.]', 'Y BKG Green [a.u.]', 'R1_BKG_Green [1/Mm]', 'Theta1_BKG_Green [deg]')
        new_R1_BKG_Green/Mic_Konstant*Green_Absorption_NO2_1ppm/Green_Amplitdue_NO2_1ppm
        sensorObject.addSubset(new_R1_BKG_Green, [
            'R1_BKG_Green [1/Mm]'], newUnits=['1/Mm'], dfIndex=2)  # Scale R to uPa
        sensorObject.addSubset(new_Th1_BKG_Green, ['Theta1_BKG_Green [deg]'], newUnits=[
            'deg'], dfIndex=2)  # Theta in deg

        # Cast Booleans
        BKGS = sensorObject.df2.df['BKG Meas. Active'].astype(int).copy()
        sensorObject.df2.df['BKG Meas. Active'] = BKGS.tolist()

        # Other Stuff
        # sensorObject.df2.df['BKG Meas. Active'] = sensorObject.df2.df['BKG Meas. Active'].astype(bool)
        # sensorObject.df2.df['BKG Meas. Active'] = sensorObject.df2.df['BKG Meas. Active'].astype(float)

        # sensorObject.plotColumn = 'R1 [1/Mm]'
        sensorObject.plotColumn = 'R1 BKG Subtracted [1/Mm]'

    return sensorObject


def PAXPreScript(sensorObject):
    timeIntervals = '10S'  # 10 Seconds
    sensorObject.df1.df = sensorObject.df1.df.resample(
        timeIntervals).interpolate()
    # PAX is not recording data when in BKG/Filter modus, therefore resampling is needed and values are interpolated (linear).
    return sensorObject


def PAXPostScript(sensorObject):
    return sensorObject


def PMSPreScript(sensorObject):
    return sensorObject


def PMSPostScript(sensorObject):
    return sensorObject


def SMPS3080_ExpPreScript(sensorObject):
    timeIntervals = '60S'  # 10 Second
    sensorObject.df1.df = sensorObject.df1.df.resample(
        timeIntervals).pad().interpolate().ffill().bfill()
    return sensorObject


def SMPS3080_ExpPostScript(sensorObject):
    return sensorObject


def SMPS3080PreScript(sensorObject):
    return sensorObject


def SMPS3080PostScript(sensorObject):
    return sensorObject


def MSPTIPreScript(sensorObject):
    return sensorObject


def MSPTIPostScript(sensorObject):
    return sensorObject


def MSPTI_MetasPreScript(sensorObject):
    sensorObject.df1.df.index = sensorObject.df1.df.index.tz_localize(None)
    return sensorObject


def MSPTI_MetasPostScript(sensorObject):
    return sensorObject


def miniPTIPreScript(sensorObject):
    sensorObject.renameColumnInSensorDf(
        '60s Norm dphi2 R Vect (V)', '60s Norm dphi2 R Vect (arb)', newUnits='')
    sensorObject.renameColumnInSensorDf(
        '60s Ernest new (V)', '60s Ernest new (arb)', newUnits='')
    return sensorObject


def miniPTIPostScript(sensorObject):
    return sensorObject
