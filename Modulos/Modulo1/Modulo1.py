def palindromo(palabra):
    i = 3
    j = 0
    k = 4
    while(not j==i and not k==i):
        if (palabra[k]!= palabra[j]):
            return False
        else:
            k -=1
            j +=1
    return True

#print(palindromo("nadan"))

def ejercicios2():
    i = 0
    while(i<214):
        if (i%13 == 0):
            print i
            i+=1
        else:
            i+=1

#ejercicios2()

def ejercicios2dif():
    for i in range(214):
        if(i%13 == 0):
            print i

#ejercicios2dif()

def ejercicioGeringoso(palabra):
    res = ""
    for c in palabra:
        res += c
        if c == "a":
            res += "pa"
        elif c == "e":
            res +=  "pe"
        elif c == "i":
            res +=  "pi"
        elif c == "o":
            res +=  "po"
        elif c == "u":
            res +=  "pu"
    return res

#print(ejercicioGeringoso("hola"))

def geromgosoopt(palabra):
    vocales = ["a","e","i","o","u"]
    res = ""
    for c in palabra:
        res += c
        if c in vocales:
            res += "p" + c
    return res

#print(geromgosoopt("hola"))

def pelotaejercicio():
    i = 100
    j = 1
    while (not i < 0 and j!= 11):
        i = float((i * 3) / 5) 
        print(str(j) + " " + str(i))
        j+=1

#pelotaejercicio()

def maximo(a,b):
    if a<b:
        return b
    else:
        return a

def tachar_impares(lista):
    for i in range(len(lista)):
        if lista[i] % 2 == 0:
            lista[i] = "x"
    return lista

#print(tachar_impares([1,2,3,4,5,6,7,4,4,4,4,4,8,9]))        

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
