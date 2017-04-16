#!/usr/bin/env python

def func_1(self):

    func_name = "func 1"

    func_call = self.name

    print("name passed from class: ", func_call)

def func_2(self):

    ## change var in master func
    self.var = 22

    print("change var in func_2: ", self.var )
