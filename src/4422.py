import scipy.io
import numpy as np
from bellpolytope import BellPolytope
from syntaxlisp import LispHelper

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

def extendInequalityToDetecLoopholeSetting(inequality,N,K,parties):
    functional=inequality[1:]
    inputs=N**parties
    outputs=K**parties
    ineffResistInequality = inequality[0:1]
    for nInputPair in range(inputs):
        oldCoeffForInputs=functional[nInputPair*outputs:(nInputPair+1)*outputs]
        newCoeffForInputs=np.zeros((K+1)**parties)
        for nOutput in range(K):
            newCoeffForInputs[(K+1)*nOutput:(K+1)*nOutput+K] = oldCoeffForInputs[nOutput*K:nOutput*K+K] 
        ineffResistInequality=np.append(ineffResistInequality,newCoeffForInputs)
        
    return ineffResistInequality

mat = scipy.io.loadmat('Inequalities_Only_4422_Raw.mat')
i=0
s=0
parties=2
InputsAlice= 4
InputsBob = 4
OutputsAlice=2
OutputsBob=2
NumberOfInequalities=175
BellMatrix=np.zeros((NumberOfInequalities, InputsAlice*OutputsAlice*InputsBob*OutputsBob+1))
for key in mat.keys():
    if s>=3: #TO GET RID OF HEADERS
        Matrix= np.array(mat.get(key))
        BellFunctional=GetBellFunctionals(Matrix,InputsAlice,InputsBob,OutputsAlice,OutputsBob)
        BellMatrix[i][1:]=BellFunctional
        BellMatrix[i][0]=-1
        i=i+1
    s=s+1

poly=BellPolytope(InputsAlice,OutputsAlice)
InefficiencyResistantInequalities=np.zeros((NumberOfInequalities, InputsAlice*(OutputsAlice+1)*InputsBob*(OutputsBob+1)+1))
text=open("IneffFunctionals4433Lisp.txt",'w')
lisp=LispHelper
for j in range(0, NumberOfInequalities):
    NormalisedFunctional=np.zeros(InputsAlice*(OutputsAlice+1)*InputsBob*(OutputsBob+1))    
    inequality=BellMatrix[j][:]
    vertices4422=np.matrix(poly.getVertices())
    values4422=np.dot(vertices4422,np.transpose(inequality[1:]))
    minimum=np.amin(values4422)
    if minimum<-1: #JUST THE INEQUALITIES WE WANT
        InefficiencyResistantInequalities[j][:]=extendInequalityToDetecLoopholeSetting(inequality,InputsAlice,OutputsAlice,parties)
        vertices4433=BellPolytope(InputsAlice,OutputsAlice+1).getVertices()
        distributions=np.matrix(vertices4433)
        values4433=np.dot(distributions,np.transpose(InefficiencyResistantInequalities[j][1:])) 
        maximum=np.amax(values4433)
        if maximum!=0:
            NormalisedFunctional=InefficiencyResistantInequalities[j][1:]/maximum
        else:
            NormalisedFunctional=InefficiencyResistantInequalities[j][1:]
        lispsyntax=lisp.syntaxlisp(lisp, NormalisedFunctional, 4, 3)
        text.write(lispsyntax + '\n')
text.close()


    
    
    
    
