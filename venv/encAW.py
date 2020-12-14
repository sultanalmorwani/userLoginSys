import os
from pynverse import inversefunc

class Encaw:
    def __init__(self, key,val):
        self.key = key
        self.val = val
    def enc_encrypt(self):
        listNum = []
        indexL = []
        for char in self.val:
            indx = self.val.index(char)
            if indx in indexL:
                num = ord(char) - ord(self.val[indexL[-1]])
            else:
                if indx == 0:
                    num = ord(char)
                else:
                    num = ord(self.val[indx]) - ord(self.val[indx - 1])
            listNum.append(num)
            indexL.append(indx)
        counter = 0
        k1 = 0.0
        k2 = 0.0
        k3 = 0.0
        fun = (lambda x: (((k1 / 3.4) * float(x)) + ((k2 / 3.9) * float(x))) * (k3 / 4.4))
        for i in self.key:
            counter += 1
            if counter < 5:
                k1 += ord(i)
            elif counter > 5 and counter < 10:
                k2 += ord(i)
            else:
                k3 += ord(i)
        cylistNum = []
        for num in listNum:
                cyNum = fun(num)
                cylistNum.append(round(float(cyNum)))
        return str(cylistNum).strip('[').replace(',','*|*').replace(' ','').strip(']')

    def enc_decrypt(self):
        delistNum = []
        enText = self.val.split('*|*')
        counter = 0
        k1 = 0.0
        k2 = 0.0
        k3 = 0.0
        fun = (lambda x: (((k1 / 3.4) * float(x)) + ((k2 / 3.9) * float(x))) * (k3 / 4.4))

        for i in self.key:
            counter += 1
            if counter < 5:
                k1 += ord(i)
            elif counter > 5 and counter < 10:
                k2 += ord(i)
            else:
                k3 += ord(i)

        for num in enText:
            try:
                float(num)
            except:
                return self.val

        for enVal in enText:
            invFun = inversefunc(fun, y_values = enVal)
            delistNum.append(round(float(invFun)))

        enText = delistNum
        val = ''
        charL = []
        if type(enText) == list:
            for num in enText:
                try:
                    num = int(num)
                except:
                    return self.val

                if len(charL) == 0:
                    char = chr(num)
                else:
                    char = ord(charL[-1]) + num
                    char = chr(char)
                charL.append(char)
                val += char
        else:
            return self.val


        return val
