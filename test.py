from settings import *


class test(object):
    def __init__(self, MAX_PAGE):
        self.MAX_PAGE = MAX_PAGE     #已经变为局部变量
        self.lis=[]                  #声明变量

    def chi(self):
        self.MAX_PAGE += 2
        return self.MAX_PAGE

    def main(self):
        s = self.chi()
        s += 1      
        t = self.__init__(MAX_PAGE)
        self.lis.append(s)
        print('t', t)
        print(s)
        print(self.lis)

test = test(MAX_PAGE)
test.main()
print(MAX_PAGE)