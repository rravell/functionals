'''
Created on Mar 28, 2019

@author: rravell
'''


import numpy as np
from bellpolytope import BellPolytope
from syntaxlisp import LispHelper




def extendInequalityToDetecLoopholeSetting(inequality,N,K,parties):
    functional=inequality[1:]
    inputs=N**parties
    outputs=K**parties
    ineffResistInequality = []
    for nInputPair in range(inputs):
        oldCoeffForInputs=functional[nInputPair*outputs:(nInputPair+1)*outputs]
        newCoeffForInputs=np.zeros((K+1)**parties)
        for nOutput in range(K):
            newCoeffForInputs[(K+1)*nOutput:(K+1)*nOutput+K] = oldCoeffForInputs[nOutput*K:nOutput*K+K] 
        ineffResistInequality=np.append(ineffResistInequality,newCoeffForInputs)
        
    return ineffResistInequality


i=0
s=0
parties=2
InputsAlice= 4
InputsBob = 4
OutputsAlice=2
OutputsBob=2
NumberOfInequalities=174

functionals=np.loadtxt('dataconverted.txt')
poly=BellPolytope(InputsAlice,OutputsAlice)
InefficiencyResistantInequalities=np.zeros((NumberOfInequalities, InputsAlice*(OutputsAlice+1)*InputsBob*(OutputsBob+1)))
text=open("IneffFunctionals4433LispCG.txt",'w')
lisp=LispHelper
for j in range(0, NumberOfInequalities):
    NormalisedFunctional=np.zeros(InputsAlice*(OutputsAlice+1)*InputsBob*(OutputsBob+1))    
    vertices4422=np.matrix(poly.getVertices())
    values4422=np.dot(vertices4422,np.transpose(functionals[j][:]))
    minimum=np.amin(values4422)
    if minimum<-1: #JUST THE INEQUALITIES WE WANT
        InefficiencyResistantInequalities[j][:]=extendInequalityToDetecLoopholeSetting(functionals[j][:],InputsAlice,OutputsAlice,parties)
        vertices4433=BellPolytope(InputsAlice,OutputsAlice+1).getVertices()
        distributions=np.matrix(vertices4433)
        values4433=np.dot(distributions,np.transpose(InefficiencyResistantInequalities[j][:])) 
        maximum=np.amax(values4433)
        if maximum!=0:
            NormalisedFunctional=InefficiencyResistantInequalities[j][:]/maximum
        else:
            NormalisedFunctional=InefficiencyResistantInequalities[j][:]
        lispsyntax=lisp.syntaxlisp(lisp, NormalisedFunctional, 4, 3)
        text.write(lispsyntax + '\n')
text.close()

    
    
    
    
    
