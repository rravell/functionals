'''
Created on Mar 28, 2019

@author: rravell
'''

import numpy as np

N=4
K=2
functionals=np.loadtxt("DATA_APS.txt")

size=np.shape(functionals)

newfunctionals=np.zeros((size[0],(N*K)**2))
for i in range(0,size[0]):
    for j in range(N**2,size[1]):
        GroupNumber=j%N
        PositionNumber=GroupNumber*N*K**2 
        if j<=N**2+(N-1):
            newfunctionals[i][PositionNumber]=functionals[i][j]
            newfunctionals[i][PositionNumber+1]=functionals[i][j]
        
        else:                
            newfunctionals[i][N*GroupNumber]+=functionals[i][j]
            newfunctionals[i][N*GroupNumber+2]=functionals[i][j]
        
for i in range(0,size[0]):
    for j in range(0,N**2):
        newfunctionals[i][N*j]+=functionals[i][j]       
        
    
    
np.savetxt("dataconverted.txt",newfunctionals)