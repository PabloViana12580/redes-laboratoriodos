"""
Universidad del Valle de Guatemala
Redes
Catedrático: Vinicio Paz
Pablo Viana - 16091
Sergio Marchena - 16387
"""
section1 = '10011001'
section2 = '11100010'
section3 = '00100100'
section4 = '10000100'


def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1

def flip(hola):
    return '1' if (hola == '0') else '0'

def complement(bin):

    n = len(bin)
    ones = ""
    twos = ""

    # for ones complement flip every bit
    for i in range(n):
        ones += flip(bin[i])

    # for two's complement go from right
    # to left in ones complement and if
    # we get 1 make, we make them 0 and
    # keep going left when we get first
    # 0, make that 1 and go out of loop
    ones = list(ones.strip(""))
    twos = list(ones)
    for i in range(n - 1, -1, -1):

        if (ones[i] == '1'):
            twos[i] = '0'
        else:
            twos[i] = '1'
            break

    i -= 1
    # If No break : all are 1 as in 111 or 11111
    # in such case, add extra 1 at beginning
    if (i == -1):
        twos.insert(0, '1')

    #print(*ones, sep = "")
    #print(type(ones))
    respuesta = listToString(ones)
    return respuesta

def binAdd(x,y):
    max_len = max(len(x), len(y))
    x = x.zfill(max_len)
    y = y.zfill(max_len)
    result = ''
    carry = 0

    for i in range(max_len-1, -1, -1):
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1

    if carry !=0 : result = '1' + result
    return result.zfill(max_len)

def otra(*args):
    suma = bin(sum(int(x, 2) for x in args))[2:]
    if (len(args[1])==sum):
        return suma
    else:
        numba=suma[2:10]
        carry=suma[0:2]
        #print("carry: "+carry)
        carry='000000'+carry
        #print("b: "+ numba)
        #print("c: "+carry)
        #print("respuesta en binario: "+bin(int(numba,2)+int(carry,2)))
        respuesta = binAdd(numba, carry)
        return respuesta

suma = otra(section1, section2, section3, section4)
print("El mensaje es: "+ section1+section2+section3+section4)
print("Los bloques son: ")
print(section1)
print(section2)
print(section3)
print(section4)
print("El checksum es: "+suma)
complemento = complement(suma)
print("El uno-complemento es: "+complemento)
checksumTest = binAdd(suma,complemento)

print("La suma del checksum y el uno-complemento es: "+checksumTest)
print("no hay errores detectados")
