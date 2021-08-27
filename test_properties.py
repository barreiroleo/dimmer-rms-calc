class Onda:
    def __init__(self, frec):
        self.__frec = frec
        self.__per = 1 / frec

    @property
    def frec(self):
        print(f"getter fre: {self.__frec}")
        return self.__frec

    @property
    def per(self):
        print(f"getter per: {self.__per}")
        return self.__per


    @frec.setter
    def frec(self, frec):
        self.__frec = frec
        self.__per = 1 / frec
        print(f"setter fre: {self.frec}")

    @per.setter
    def per(self, per):
        self.__per = per
        self.__frec = 1 / per
        print(f"setter per: {self.per}")

    @frec.deleter
    def frec(self):
        del self.__frec
        print("deletter frec")

sine = Onda(1)
print(f"sine.frec      ; {sine.frec}\n")
print(f"sine.per       ; {sine.per}\n")
sine.frec = 10
print(f"sine.frec = 10 ; {sine.frec}\n")
print(f"sine.per       ; {sine.per}\n")
sine.per = 0.1
print(f"sine.per = 0.1 ; {sine.per}\n")
print(f"sine.frec      ; {sine.frec}\n")