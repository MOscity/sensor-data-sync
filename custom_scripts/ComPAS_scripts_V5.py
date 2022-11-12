from lib import np, pd


def Amplitude_Phase(sensorObjectDf, X_Column, Y_Column, R_Name, Theta_Name):
    new_R = pd.DataFrame({R_Name: np.sqrt(
        sensorObjectDf.df[X_Column]**2+sensorObjectDf.df[Y_Column]**2)}, index=sensorObjectDf.df.index)
    new_Th = pd.DataFrame({Theta_Name: np.arctan2(
        sensorObjectDf.df[Y_Column], sensorObjectDf.df[X_Column])*180.0/np.pi}, index=sensorObjectDf.df.index)
    return new_R, new_Th

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


def ComPASV5PostScript(sensorObject, Mic_Konstant = 68.07064429, Green_Amplitdue_NO2_1ppm = 1250, Green_Absorption_NO2_1ppm = 415.46 ):
    # Special Constants
    # Mic_Konstant = 214.7483648
    # Mic_Konstant = 215.2582778
    # Mic_Konstant = 68.07064429

    # Green Channel Absorption Calibration
    # Green_Amplitdue_NO2_1ppm = 1250  # uPa
    # Green_Amplitdue_NO2_1ppm = 1620 # uPa
    # Green_Absorption_NO2_1ppm = 415.46  # 1/Mm

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
