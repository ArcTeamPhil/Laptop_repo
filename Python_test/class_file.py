#!/usr/bin/env python

class class_1():

    def __init__(self):

        self.name = "class_1"
        self.var = 1

    def call_func_1(self):
        from func_1 import func_1

        func_1(self)

    def call_func_2(self):
        """Update the var"""

        from func_1 import func_2

        func_2(self)

        print("updated var in class1 : ", self.var )

class class_2():

    def __init__(self):

        self.name = "class_2"
        self.var = 2

    def call_func_1(self):
        from func_1 import func_1


        func_1(self)


    def call_func_2(self):
        """Update the var"""

        from func_1 import func_2

        func_2(self)

        print("updated var in class2: ", self.var )
