import numpy as np 
import pandas as pd 
import os 
import subprocess
from NMSSMParamsUpdater import NMSSMParamsUpdater
from NMSSMToolsUpdater import NMSSMFileHandler

os.chdir('/gpfs/home/argiannakopo/NMSSMStuff/NMSSMTools_6.1.2')
nmssmtools = NMSSMFileHandler('inp.dat')

nmssm_params = pd.DataFrame({
    'tanb' : pd.Series(dtype='float'),
    'mA' : pd.Series(dtype='float'),
    'lam': pd.Series(dtype='float'),
    'kappa': pd.Series(dtype='float'),
    'At/M': pd.Series(dtype='float'),
    'Ak' : pd.Series(dtype='float'),
    'mhiggs': pd.Series(dtype='object'),
    'errors': pd.Series(dtype='object')
})

for tb in [5, 20, 50]:
    for mA in [1000, 3000, 5000]:
        for n in [2,3,4,5,6]:
            for lam in np.linspace(0.01, 1, 8):
                for kappa in np.linspace(0.001,0.75, 8):
                    for Ak in np.linspace(-1000, 10, 5):
                        nmssmtools.update_nmssm_params(lam, kappa, tb, n*1000, Ak, mA )
                        with open('output_log_file.log', 'w') as f:
                            subprocess.run('./run inp.dat', stdout=f, stderr=f, shell=True)
                            mass_array = nmssmtools.find_higgs_mass('spectr.dat')
                            errors = nmssmtools.find_higgs_error('spectr.dat')
                            new_row = pd.DataFrame({'tanb' :[tb], 'mA' : [mA], 'lam' : [lam], 'kappa' : [kappa], 'At/M' : [n], 'Ak':[Ak], 'mhiggs': [mass_array], 'errors' : [errors]})

                            nmssm_params = pd.concat([nmssm_params, new_row], ignore_index=True)


nmssm_params.to_csv('nmssm_params_mass_1000.csv')
