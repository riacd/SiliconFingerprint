from os import urandom

def convertToBin( x):
    res = ''
    for i in range(8):
        if x & (1 << (7 - i)):
            res += '1'
        else:
            res += '0'
    return res


def convertToBytes( tmp):
    now = 1
    res = 0
    for i in range(1, len(tmp) + 1):
        if tmp[-i] == '1':
            res += now
        now = now * 2
    return bytes([res])

x = urandom(1) #len(x) = 8
print("x is", x)
seed = b''
w = '11111111'

for i in range(len(x)):
    tmp = convertToBin(int(x[i]))
    print("tmp is", tmp)
    tmpres = ''
    for j in range(len(tmp)):
        if tmp[j] == w[i * 8 + j]:
            tmpres += '0'
        else:
            tmpres += '1'
    print("tmpres is", tmpres)
    seed += convertToBytes(tmpres)

print(seed)