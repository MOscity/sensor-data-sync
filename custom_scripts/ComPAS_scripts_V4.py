from lib import np, pd


def Amplitude_Phase(sensorObjectDf, X_Column, Y_Column, R_Name, Theta_Name):
    new_R = pd.DataFrame({R_Name: np.sqrt(
        sensorObjectDf.df[X_Column]**2+sensorObjectDf.df[Y_Column]**2)}, index=sensorObjectDf.df.index)
    new_Th = pd.DataFrame({Theta_Name: np.arctan2(
        sensorObjectDf.df[Y_Column], sensorObjectDf.df[X_Column])*180.0/np.pi}, index=sensorObjectDf.df.index)
    return new_R, new_Th


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
