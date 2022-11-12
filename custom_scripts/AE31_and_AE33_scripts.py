from lib import pd, timedelta

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

