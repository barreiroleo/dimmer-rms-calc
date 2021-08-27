import numpy as np
from functions import *


class bisector:
    xinf, xsup       = 0,            0
    xmed, xmed_old   = 0,            0
    err_rel, err_obj = float('inf'), 0
    iter_n, max_iter = 0,            500

    def __init__(self, function, xinf, xsup, err_obj=1e-4, max_iter=500, bias=0, verbose=False, *args, **kwargs):
        self.xinf    , self.xsup     = xinf,     xsup
        self.err_obj , self.max_iter = err_obj,  max_iter
        self.function, self.bias     = function, bias
        self.args    , self.kwargs   = args,     kwargs
        self.verbose                 = verbose

    def next_iter(self):
        self.iter_n   += 1
        self.xmed_old  = self.xmed
        self.xmed      = (self.xinf + self.xsup) / 2
        self.calc_error()

        self.yinf = self.function(self.xinf, *self.args, **self.kwargs) - self.bias
        self.ymed = self.function(self.xmed, *self.args, **self.kwargs) - self.bias
        self.logs('iter')
        
        if self.ymed == 0:
            self.err_rel = 0
            return
        elif self.yinf * self.ymed < 0:
            self.xsup  = self.xmed
        elif self.yinf * self.ymed > 0:
            self.xinf  = self.xmed
        else:
            raise Exception('Fail iter_xmed')

    def calc_error(self):
        self.err_rel = 100 * (self.xmed - self.xmed_old) / self.xmed
        self.err_rel = abs(self.err_rel)

    def run(self):
        self.logs('header')
        while((self.err_rel > self.err_obj) and (self.iter_n < self.max_iter)):
            self.next_iter()
        
        if self.err_rel == 0: self.logs('exact')
        else: self.logs('results')
        return(self.xmed)
    
    def logs(self, item):
        if self.verbose is True:
            if item == 'header':
                print("Iter | xinf{0:4} | xsup{0:4} | xmed{0:4} | eps{0:5} | y(xmed)".format(''))
                print("{:=>60}".format(''))
            if item == 'iter':
                print("{:>4} | {:^8.4f} | {:^8.4f} | {:^8.4f} | {:_>8.4f} | {:^8.4f}".
                    format(self.iter_n, self.xinf, self.xsup, self.xmed, self.err_rel, self.ymed))
        if item == 'results':
            if self.err_rel <= self.err_obj: print("Finish by eps: {:.4e}".format(self.err_rel))
            if self.iter_n >= self.max_iter: print("Finish by iter: {}".format(self.iter_n))
            print("Xroot: {0}".format(self.xmed))
        if item == 'exact':
            print ("Exact root found: {}".format(self.xmed))


# TEST
# def function(tInt_perc):
#     frec, ampl = 1, 1
#     rms_unit   = (np.sqrt(2) / 2) * ampl
#     rms_dimmer = fun_rms_simbolic(tInt_perc, frec=frec, amp=ampl) / rms_unit
#     return rms_dimmer


# solver = bisector(function, xinf=0, xsup=100, bias=0.1, err_obj=1e-5, verbose=False)
# sol = solver.run()
# print("rms({:.4f}) = {:.4f}".format(sol, function(sol)))