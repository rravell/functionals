import scipy.io
import numpy as np
def GetBellFunctionals(Matrix, InputsAlice, InputsBob, OutputsAlice, OutputsBob):
    functional = np.zeros(InputsAlice*OutputsAlice*InputsBob*OutputsBob)
    s=0
    for i in range (0, InputsAlice):
        for j in range (0, InputsBob):
            for k in range (0, OutputsAlice):
                for l in range (0, OutputsBob):
                    functional[s]=-Matrix[2*i+k][2*j+l]
                    s=s+1             
    return(functional)


mat = scipy.io.loadmat('Inequalities_Only_3522_Raw.mat')
i=0
s=0
InputsAlice= 3
InputsBob = 5
OutputsAlice=2
OutputsBob=2
NumberOfInequalities=7
BellMatrix=np.zeros((NumberOfInequalities, InputsAlice*OutputsAlice*InputsBob*OutputsBob+1))
for key in mat.keys():
    if s>=3:
        Matrix= np.array(mat.get(key))
        BellFunctional=GetBellFunctionals(Matrix,InputsAlice,InputsBob,OutputsAlice,OutputsBob)
        BellMatrix[i][1:]=BellFunctional
        BellMatrix[i][0]=-1
        i=i+1
    s=s+1

