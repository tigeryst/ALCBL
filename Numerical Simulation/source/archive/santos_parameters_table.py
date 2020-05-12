# Generate table for Santos parameters to compare with literature
from soil_acoustic import capillary, santos_param
import pandas as pd
import numpy as np

SoBar = np.array([0.01,0.3,0.4,0.5,0.6,0.7])
S0 = 1 - SoBar

pc, dpcdS = capillary(SoBar, 1)
KcStar, B1, B2, M1, M2, M3 = santos_param(S0, pc, dpcdS, 0, 1)
result = np.array([SoBar,KcStar,B1,B2,M1,M2,M3])
result = pd.DataFrame(np.transpose(result),columns=['So','Kc*','B1','B2','M1','M2','M3'])
result.to_csv('../plots/export_dataframe.csv', index = False, header=True)