empleado_01 = []

empleado_01.append([20222333,45,2,20000])
empleado_01.append([33456234,40,0,25000])
empleado_01.append([45432345,41,1,10000])


#%%

def salarioActividad01(empleados,umbral):
    res = []
    for empleado in empleados:
        if empleado[3]>umbral:
            res.append(empleado)
    return res

#print(salarioActividad01(empleado_01, 15000))

#%%

empleado_02 = empleado_01.copy()

empleado_02.append([43967304,37,0,12000])
empleado_02.append([42236276,36,0,18000])

#print(salarioActividad01(empleado_02, 15000))

#%%

empleado_03 = []

empleado_03.append([20222333,20000,45,2])
empleado_03.append([33456234,25000,40,0])
empleado_03.append([45432345,10000,41,1])
empleado_03.append([43967304,12000,37,0])
empleado_03.append([42236276,18000,36,0])

def salarioActividad03(empleados,umbral):
    res = []
    for empleado in empleados:
        if empleado[1]>umbral:
            agregado = []
            
            agregado.append(empleado[0])
            agregado.append(empleado[2])
            agregado.append(empleado[3])
            agregado.append(empleado[1])
            
            res.append(agregado)

    return res

#print(salarioActividad03(empleado_03, 15000))

#%%

empleado_04 = []

empleado_04.append([20222333,33456234,45432345,43967304,42236276,])
empleado_04.append([20000,25000,10000,12000,18000])
empleado_04.append([45,40,41,37,36])
empleado_04.append([2,0,1,0,0])

def salarioActividad04(empleados,umbral):
    
    superadores = []
    for i in range(len(empleado_04[1])):
        if (empleado_04[1][i]>umbral):
            superadores.append(i)
            
    res = []
    for i in superadores:
        agregado = []
        agregado.append(empleados[0][i])
        agregado.append(empleados[1][i])
        agregado.append(empleados[2][i])
        agregado.append(empleados[3][i])
        
        res.append(agregado)
    return res

print(salarioActividad04(empleado_04, 15000))