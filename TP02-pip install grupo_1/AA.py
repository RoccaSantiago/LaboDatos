import numpy as np

def Verificar(C):
    suma = 0
    for i in range(0,3):
        for j in range(0,3):
            suma += C[j][i]
        if suma != 9:
            return False

    dia = 0
    for i in range(0,3): 
        dia += C[i][i] 
    
    if dia != 9:
        return False

    else:
        return True
    

suma = 0
a = [[],[],[]]

def CC(C,j,b):
    global suma
    A = C.copy()

    if j == b:
        if len(C[j]) == b:
            print(A)
            if Verificar(C):
                print("------SUMO------")
                suma += 1
        return None
    
    else:
        for k in range(1,b+1):
            A[j].append(k)
            CC(A,j,b)

                
CC(a,0,3)

print(suma)