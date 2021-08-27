import numpy as np
from scipy.optimize import bisect
from tabulate import tabulate


class Dimmer:
    def __init__(self, frec, amp, time_int=0) -> None:
        self.__frequency = frec
        self.amplitud = amp
        self.time_interrupt = time_int
        self.__periode = 1 / frec

    @property
    def frequency(self): return self.__frequency
    @property
    def periode(self): return self.__periode

    @frequency.setter
    def frequency(self, frec):
        self.__frequency, self.__periode = frec, 1 / frec

    @periode.setter
    def periode(self, periode):
        self.__periode, self.__frequency = periode, 1 / periode

    def _v_sine(self, t):
        omega = 2 * np.pi * self.frequency
        return self.amplitud * np.sin(omega * t)

    def v_dimmer(self, t):  
        per = self.periode
        tint = self.time_interrupt
        # sourcery skip: flip-comparison
        if (0 <= t and t < tint):
            return 0
        elif (tint <= t and t < 0.5 * per):
            return self._v_sine(t)
        elif (0.5*per <= t and t < 0.5*per + tint):
            return 0
        elif (0.5*per + tint <= t and t < per):
            return self._v_sine(t)

    def vrms_simbolic(self):
        # TODO: Refactorear nombre del metodo y sus usos en un futuro.
        amp, omega = self.amplitud, 2 * np.pi * self.frequency
        per, tint = self.periode, self.time_interrupt
        T1, T2 = 0, per

        def sine_integrate(t):
            int_a = amp ** 2
            int_b = t / 2
            int_c = (np.sin(2*t*omega) / (4*omega))
            sine_int = int_a * (int_b - int_c)
            return sine_int

        rms_a = 1 / (T2 - T1)
        rms_b1 = sine_integrate(T2 / 2)
        rms_b2 = sine_integrate(tint)
        rms_b = (rms_b1 - rms_b2) * 2
        rms = np.sqrt(rms_a * rms_b)
        return rms

    def convert_rms_duty(self, vrms):
        vrms_max = np.sqrt(2) * 0.5 * self.amplitud
        vrms_duty = 100 * vrms / vrms_max
        return vrms_duty

    def convert_duty_rms(self, vrms_duty):
        vrms_max = np.sqrt(2) * 0.5 * self.amplitud
        vrms = vrms_duty * vrms_max
        return vrms

    def solve_tint_for_duty(self, duty_perc):
        # HACK: Se respalda el estado del time interrupt porque se utiliza calacular. Al final se restaura.
        time_interrupt_backup = self.time_interrupt
        
        def function(tint, bias=0):
            self.time_interrupt = tint
            vrms_max = np.sqrt(2) * 0.5 * self.amplitud
            vrms_duty = self.vrms_simbolic() / vrms_max
            return vrms_duty - bias
        root = bisect(function, 0, self.periode * 0.5, args=(duty_perc / 100))
        
        self.time_interrupt = time_interrupt_backup
        return root
    
    def print_dimmer_state(self):
        # TODO: Ver si conviene agregar un atributo de vrms actual. Se repite el calculo en ocaciones.
        vrms   = self.vrms_simbolic()
        duty   = self.convert_rms_duty(vrms)
        header = ["Amplitud [V]", "Frecuencia [Hz]", "Interrupción [s]", "Vrms [V]", "Duty [%]"]
        data   = [[self.amplitud, self.frequency, self.time_interrupt, vrms, duty]]
        print_table(header, data)

def print_table(header, data):
    print(tabulate(tabular_data=data, headers=header, tablefmt="simple",
                   numalign="center", stralign="center"))