import numpy as np


def fun_Sine(t, f=1, a=1):
    w = 2 * np.pi * f
    return a * np.sin(w * t)


def fun_Dimmer(t, tInt_perc, f=1, a=1):
    periode = 1 / f
    tInt    = 0.5 * periode * (tInt_perc / 100)
    vt      = fun_Sine(t, f, a)
    vd      = 0
    if (0 <= t and t < tInt):
        vd = 0
    elif (tInt <= t and t < 0.5 * periode):
        vd = vt
    elif (0.5*periode <= t and t < 0.5*periode + tInt):
        vd = 0
    elif (0.5*periode + tInt <= t and t < periode):
        vd = vt
    return vd


def fun_rms_numeric(data_y):
    sum_y = 0
    for i in data_y:
        sum_y = sum_y + i**2
    rms = np.sqrt(sum_y / len(data_y))
    return rms


def fun_rms_simbolic(tInt_perc, frec=1, amp=1):
    periode = 1 / frec
    tInt    = 0.5 * periode * (tInt_perc / 100)
    T1, T2  = 0, periode

    def sine_integrate(t):
        w        = 2 * np.pi * frec
        int_a    = amp ** 2
        int_b    = t / 2
        int_c    = (np.sin(2*t*w) / (4*w))
        sine_int = int_a * (int_b - int_c)
        return sine_int

    rms_a  = 1 / (T2 - T1)
    rms_b1 = sine_integrate(T2 / 2)
    rms_b2 = sine_integrate(tInt)
    rms_b  = (rms_b1 - rms_b2) * 2
    rms    = np.sqrt(rms_a * rms_b)
    return rms