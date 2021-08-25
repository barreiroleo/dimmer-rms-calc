import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.optimize import bisect

from functions import *


def main():
    for i in range(100+1):
        print("duty([per/2] * {:>14.10f}%)= {:>6.2f}%".format(solve_tInt(i), i))

    init_plot()


def gen_data(tInt_perc=50, frec=1, amp=1):
    samples = 100
    periode = 1 / frec
    t = np.linspace(0, periode, samples)
    v_dimmer = [fun_Dimmer(ti, tInt_perc, frec, amp) for ti in t]
    rms_dimmer = fun_rms_simbolic(tInt_perc, frec, amp) * np.ones(samples)
    return [t, v_dimmer, rms_dimmer]


def init_plot():
    global fig, ax1, l1, l2
    t_series, vt_series, rms_series = gen_data()
    plt.ion()

    fig, ax1 = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.35, top=0.95, right=0.89, wspace=0, hspace=0)

    l1, = plt.plot(t_series, vt_series)
    l2, = plt.plot(t_series, rms_series)

    plt.grid(True)
    update_plot()
    setting_sliders()
    ax1.set_ylabel(r'Amplitud [v]')
    secax_y = ax1.secondary_yaxis(
        'right', functions=(rms_to_duty, duty_to_rms))
    secax_y.set_ylabel(r'Duty [%]')
    plt.show(block=True)


def update_plot(tInt_perc=50, frec=1, ampl=1):
    global fig, ax1, l1, l2
    t_series, vt_series, rms_series = gen_data(tInt_perc, frec, ampl)
    # Plot data
    l1.set_xdata(t_series), l2.set_xdata(t_series)
    l1.set_ydata(vt_series), l2.set_ydata(rms_series)
    # Update legend
    sine_str = r'$v(t) = \mathcal{A} \mathrm{sin}(2 \omega t)$'
    rms_str = "RMS: {:.5f}".format(rms_series[0])
    ax1.legend([sine_str, rms_str])
    # Update limits
    ax1.set_xlim(np.min(0), np.max(1 / frec))
    ax1.set_ylim(-ampl, ampl)


def setting_sliders():
    def update_sliders(val):
        update_plot(slide_tInt.val, slide_frec.val, slide_amp.val)
        frec, ampl, tInt_perc = slide_frec.val, slide_amp.val, slide_tInt.val
        rms_unit = (np.sqrt(2) / 2) * ampl
        rms_value = fun_rms_simbolic(tInt_perc, frec=frec, amp=ampl) / rms_unit
        slide_duty.set_val(rms_value * 100)

    def update_slider_duty(val):
        tint = solve_tInt(slide_duty.val, slide_frec.val, slide_amp.val)
        slide_tInt.set_val(tint)

    global ax_frec, ax_amp, ax_tInt, ax_duty, ax_solve
    global slide_frec, slide_amp, slide_tInt, slide_duty, btn_solve
    ax_frec = plt.axes([0.1, 0.10, 0.80, 0.03])
    ax_amp = plt.axes([0.1, 0.15, 0.80, 0.03])
    ax_tInt = plt.axes([0.1, 0.20, 0.80, 0.03])
    ax_duty = plt.axes([0.1, 0.25, 0.6, 0.03])
    ax_solve = plt.axes([0.8, 0.25, 0.1, 0.03])
    slide_frec = Slider(ax_frec, 'Frec',  1.0, 50,  valinit=1,  valstep=1)
    slide_amp = Slider(ax_amp,  'Amp',   1.0, 311, valinit=1,  valstep=1)
    slide_tInt = Slider(ax_tInt, '%Int',  0.0, 100, valinit=50, valstep=1)
    slide_duty = Slider(ax_duty, '%Duty', 0.0, 100, valinit=50, valstep=1)
    btn_solve = Button(ax_solve, 'Solve')
    slide_frec.on_changed(update_sliders)
    slide_amp.on_changed(update_sliders)
    slide_tInt.on_changed(update_sliders)
    # slide_duty.on_changed(solve_tInt)
    btn_solve.on_clicked(update_slider_duty)


def rms_to_duty(x):
    vrms = x
    # vrms = fun_rms_simbolic(slide_tInt.val, slide_frec.val, slide_amp.val)
    vrms_max = np.sqrt(2) * 0.5 * slide_amp.val
    vrms_duty = 100 * vrms / vrms_max
    return vrms_duty


def duty_to_rms(x):
    vrms_duty = x
    vrms_max = np.sqrt(2) * 0.5 * slide_amp.val
    vrms = vrms_duty * vrms_max / 100
    return vrms


def solve_tInt(duty, frec=1, amp=1):
    def function(tInt_perc, bias=0):
        rms_unit = (np.sqrt(2) / 2) * amp
        rms_value = fun_rms_simbolic(tInt_perc, frec=frec, amp=amp) / rms_unit
        return rms_value - bias
    root = bisect(function, 0, 100, args=(duty / 100))
    return root


if __name__ == "__main__":
    main()
