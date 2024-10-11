# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 09:32:14 2022

@author: Abbas Moosajee
"""
from itertools import groupby
import numpy as np

# filename = 'input1.txt'
# data = np.loadtxt(filename, delimiter=',', skiprows=1, dtype=float);

# a = np.array(data);
# result = [list(v) for k,v in groupby(a,np.isfinite) if k];

# elvesclr=[sum(i) for i in result];

# max(elvesclr)

# %%

data2 = np.loadtxt('input2.txt', delimiter=whitespace, skiprows=0, dtype=str);