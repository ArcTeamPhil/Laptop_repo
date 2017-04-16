#!/usr/bin/env python

class master_class():
    """Import classes which call functions"""

    def __init__(self):

        self.name = "master class"
        self.var = 33

    def __str__(self):
        return'('+str(self.name)+')'

    def init_nodes(self):

        from class_file import class_1
        # from class_file import class_2

        print("init_nodes launched")
        print

        ## instantiate class
        self.exe1 = class_1()
        print("class 1 var init: ", self.exe1.var)
        print("class 1 name init: ", self.exe1.name)

        ## instantiate 2nd class
        # self.exe2 = class_2()
        # self.exe2.name = self.name


    def launch_nodes(self):

        ## change the class 1 name
        self.exe1.name = self.name
        ## grab private var from class
        print("class 1 name passed: ", self.exe1.name)
        ## call function from function in class
        self.exe1.call_func_1()
        ## call func to change var
        self.exe1.call_func_2()

        print("master self.var: ", self.var)


        print

        # print("class 2: ", self.exe2.name)
        # self.exe2.call_func_1()
        # self.exe2.call_func_2()


    def init_class_1(self):
        from class_file import class_1






if __name__ == "__main__":




    ################### call master class
    exe = master_class()
    print

    exe.init_nodes()
    exe.launch_nodes()

    print
    print("launching classes seperately")
    print

    from class_file import class_1
    ## instantiate class
    exe1 = class_1()
    ## grab private var from class
    print("class 1: ", exe1.name)
    print("var 1: ", exe1.var)
    ## call function from function in class
    exe1.call_func_1()

    print

    # from class_file import class_2
    # ## instantiate 2nd class
    # exe2 = class_2()
    # print("class 2: ", exe2.name)
    # exe2.call_func_1()


    print

    print("master name: ", exe.name)
    print("master var: ", exe.var)
