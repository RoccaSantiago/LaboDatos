def ejercicio1():
    altura = 0.00011
    dia = 0
    while (altura<67.5):
        altura*=2
        dia+=1
    return dia

#print(ejercicio1())

def ejercicio2():
    i = 100
    j = 1
    while (not i < 0 and j!= 11):
        i = float((i * 3) / 5) 
        print(str(j) + " " + str(i))
        j+=1

def ejercicio3(palabra):
    vocales = ["a","i","o","u"]
    res = ""
    for i in range(len(palabra)):
        if ((not i==<len(palabra) or not i==len(palabra)-1) and palabra[i] in vocales):
            res+="e"
        else:
            res+=palabra[i]
    return res

print(ejercicio3("hola"))

def ejercicio4(n):
    if n%2==0:
        return True
    else:
        return False

def ejercicio5(lista):
    if 2 in lista:
        return True
    else:
        return False

def ejercicio6(n,lista):
    if n in lista:
        return True
    else:
        return False

def ejerciocio7(lista1, lista2):
    if len(lista1)>len(lista2):
        return lista1
    else: 
        return lista2

def ejercicio8(palabra):
    res = 0 
    for c in palabra:
        if c == "e":
            res+=1
    return res

def ejercicio9(lista):
    for i in range(len(lista)):
        lista[i] = lista[i] + 1
    return lista

def maximo(p1,p2):
    if len(p1)>len(p2):
        return p1
    else:
        return p2 

def ejercicio10(p1, p2):
    res = ""
    i = 0
    a = maximo(p1,p2)
    for i in range(a): 
        res += p1[i]
        res += p2[i]
    return res


        



        
