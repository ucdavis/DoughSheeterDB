import pandas as pd
import os
from datetime import datetime
import numpy as np

# Get the indices of the files to analyze
D = os.listdir()
indices = [i for i,s in enumerate(D) if 'csv' in s and 'Avg' not in s]
if not indices:
    raise ValueError("No CSV files in diretory")
Dcsv = [D[i] for i in indices]

# Loop through the files
for file in np.arange(np.size(Dcsv)):
    filename = Dcsv[file]
    inPassTable = pd.read_csv(filename,header=None)
    inPassTable.pop(1) # get rid of the numerical label for position
    inPassTable.iloc[:,0] = inPassTable.iloc[:,0].apply(lambda x: 
        datetime.utcfromtimestamp(x/1000).strftime('%S.%f')) # convert time
    inPassTable = inPassTable.sort_values(by=[0,2]) # sort by time
    inPassTable.iloc[:,0] = inPassTable.iloc[:,0].astype(float)
    inPassHeight = inPassTable.iloc[:,[0,2]]
    G = inPassHeight.groupby(0).mean() # average the height across the belt
    zero = G[G<2.5].dropna().index.to_series().values.astype(float)
    zeroIdx = inPassTable.iloc[:,0].isin(zero) # only time points < 2.5 mm
    zeroCorrectTable = inPassTable[zeroIdx.values]
    zeroCorrectTable.pop(0)
    ZC = zeroCorrectTable.groupby(2).mean().reset_index() # average baseline
    realIdx = ~inPassTable.iloc[:,0].isin(zero) # dough locations
    doughTable = inPassTable[realIdx.values]

    # This loop goes through each row and applies the baseline correction
    vals = []
    for i in np.arange(np.size(doughTable.iloc[:,0])):
        row = doughTable.iloc[i,:]
        idx = ZC.iloc[:,0].isin([row.iloc[1]])
        while sum(idx) == 0:
            nextVal = row.iloc[1]+(0.3*np.sign(np.random.randn()))
            idx = ZC.iloc[:,0].isin([nextVal])
        corr = ZC.iloc[idx.values,1]
        final = row.iloc[2]-corr.values
        vals.append(np.asscalar(final))
    doughTable['Corrected Height'] = vals
    finalDoughTable = doughTable.iloc[:,[0,-1]]
    # Before averaging across the belt, get rid of values < 2.5 mm to remove
    # regions on either side of the dough
    finalDoughTable = finalDoughTable[finalDoughTable['Corrected Height'] > 2.5]
    finalDoughTable.iloc[:,0] = round(finalDoughTable.iloc[:,0]-finalDoughTable.iloc[0,0],2)
    timeHeight = finalDoughTable.groupby(0).mean() # average across the belt
    timeHeight.to_csv(filename[:-4]+"_HeightAvg.csv", sep=',' , index_label='Time [s]')
