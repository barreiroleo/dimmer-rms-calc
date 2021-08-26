import numpy as np
from scipy.optimize import bisect


class Dimmer:
    def __init__(self, frec, amp, time_int=0) -> None:
        self.frequency      = frec
        self.amplitud       = amp
        self.time_interrupt = time_int
        self._periode       = 1 / frec
        
        
    def _v_sine(self, t):
        omega = 2 * np.pi * self.frequency
        return self.amplitud * np.sin(omega * t)
    
    def v_dimmer(self, t):
        per  = self._periode
        tint = self.time_interrupt
        
        if (0 <= t and t < tint):
            return 0
        elif (tint <= t and t < 0.5 * per):
            return self._v_sine(t)
        elif (0.5*per <= t and t < 0.5*per + tint):
            return 0
        elif (0.5*per + tint <= t and t < per):
            return self._v_sine(t)
    
    def vrms_num(self):
        t_series = np.arange(0, self._periode, self._periode / 200)
        v_series = [self.v_dimmer(t) for t in t_series]
        v_sum    = 0
        for i in v_series:
            v_sum = v_sum + i**2
        rms = np.sqrt(v_sum / len(v_series))
        return rms
    
    def vrms_simbolic(self):
        amp, omega = self.amplitud, 2 * np.pi * self.frequency
        per, tint  = self._periode, self.time_interrupt
        T1, T2     = 0, per

        def sine_integrate(t):
            int_a    = amp ** 2
            int_b    = t / 2
            int_c    = (np.sin(2*t*omega) / (4*omega))
            sine_int = int_a * (int_b - int_c)
            return sine_int

        rms_a  = 1 / (T2 - T1)
        rms_b1 = sine_integrate(T2 / 2)
        rms_b2 = sine_integrate(tint)
        rms_b  = (rms_b1 - rms_b2) * 2
        rms    = np.sqrt(rms_a * rms_b)
        return rms
    
    def convert_rms_duty(self, vrms):
        vrms_max  = np.sqrt(2) * 0.5 * self.amplitud
        vrms_duty = 100 * vrms / vrms_max
        return vrms_duty
    
    def convert_duty_rms(self, vrms_duty):
        vrms_max = np.sqrt(2) * 0.5 * self.amplitud
        vrms     = vrms_duty * vrms_max
        return vrms
    
    def solve_tint_for_duty(self, duty_perc):
        def function(tint, bias=0):
            self.time_interrupt = tint
            vrms_max  = np.sqrt(2) * 0.5 * self.amplitud
            vrms_duty = self.vrms_simbolic() / vrms_max
            return vrms_duty - bias
        root = bisect(function, 0, self._periode * 0.5, args=(duty_perc / 100))
        return root
    