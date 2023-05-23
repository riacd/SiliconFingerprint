from bch_fuzzy_extractor.bch import Bch, GF
import numpy as np
from os import urandom

def convertToBin(x):
    res = ''
    for i in range(8):
        if x & (1 << (7-i)):
            res += '1'
        else:
            res += '0'
    return res


#511 376 15
class FE:
    def __init__(self, n, t):
        self.n = n
        self.t = t

    def convertToBin(self, x):
        res = ''
        for i in range(8):
            if x & (1<<(7-i)):
                res += '1'
            else:
                res += '0'
        return res

    def convertToBytes(self, tmp):
        now = 1
        res = 0
        for i in range(1, len(tmp)+1):
            if tmp[-i] == '1':
                res += now
            now = now*2
        return bytes([res])


    def SS(self, w):
        m = 9
        t = self.t
        poly_str = "1000010001"
        field = GF(m, poly_str)
        code = Bch(field, t)
        rng1 = list(np.random.randint(2, size=code.k))
        #print("rng1 in SS is",rng1)
        r = code.encode(rng1)


        #print("in SS r is", r)
        for i in range(len(r)):
            if (w[i] == '0' and r[i] == 0) or (w[i] == '1' and r[i] == 1):
                r[i] = 0
            else:
                r[i] = 1
        s = r
        # print(s)
        #print('in SS s is', s)
        return s

    def rec(self, w2, s):
        codeword = s.copy()
        for i in range(len(codeword)):
            if (w2[i] == '0' and codeword[i] == 0) or (w2[i] == '1' and codeword[i] == 1):
                codeword[i] = 0
            else:
                codeword[i] = 1
        #print("in rec r2 is ", codeword)
        m = 9
        t = self.t
        poly_str = "1000010001"
        field = GF(m, poly_str)
        code = Bch(field, t)
        decoded_msg = code.decode(codeword)
        # print(len(decoded_msg))
        #print("decode in in Rec is",decoded_msg)
        r = code.encode(decoded_msg)
        #print("r in Rec is", r)

        # print(ecc)
        # print(s)
        w = ''
        for i in range(len(r)):
            if r[i] == s[i]:
                w += '0'
            else:
                w += '1'
        w += '1'
        #print('w in rec is', w)
        return w


    def generate(self, w):
        s = self.SS(w)

        x = urandom(64) #len(x) = 512
        #print("x is", x)
        seed = b''

        for i in range(len(x)):
            tmp = convertToBin(int(x[i]))
            tmpres = ''
            for j in range(len(tmp)):
                if tmp[j] == w[i * 8 + j]:
                    tmpres += '0'
                else:
                    tmpres += '1'
            seed += self.convertToBytes(tmpres)

        R = np.frombuffer(seed, dtype=np.uint8)
        # print('seed in generate is', seed)
        return R, s, x

    def reproduce(self, w2, s, x):
        w = self.rec(w2, s)

        seed = b''
        for i in range(len(x)):
            tmp = convertToBin(int(x[i]))
            tmpres = ''
            for j in range(len(tmp)):
                if tmp[j] == w[i * 8 + j]:
                    tmpres += '0'
                else:
                    tmpres += '1'
            seed += self.convertToBytes(tmpres)
        # print('seed in reproduce is', seed)
        R = np.frombuffer(seed, dtype=np.uint8)
        return R


if __name__ == "__main__":
    w = ''
    for i in range(512):
        w += '1'

    fe = FE(511, 15)
    #
    # print(w)
    # s = fe.SS(w)
    #
    #
    # w2 = ''
    # for i in range(512):
    #     w2 += '0'
    # print('w2 is ', w2)
    # print('rec w is', fe.rec(w2, s))
    # print(len(w2))

    print('w is,', w)
    R1, ecc, x = fe.generate(w)

    w2 = '000000000000000'
    for i in range(497):
        w2 += '1'

    print('w2 is,', w2)
    R2 = fe.reproduce(w2, ecc, x)
    print(R1)
    print(R2)
    if not R1 == R2:
        print("Fail")
    # t = urandom(2)
    # print(t)
    # print(int(t[0]))
    # t1 =   fe.convertToBin(int(t[0]))
    # print(t1)
    # t2 =  fe.convertToBytes(t1)
    # print(t2)






