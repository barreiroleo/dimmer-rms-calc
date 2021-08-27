import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from dimmer import Dimmer, print_table

dimmer = Dimmer(frec=50, amp=1)

def main():
    init_plot()

def init_plot():
    global fig, ax1, l1, l2
    t_serie, v_serie, vrms_serie = gen_data()
    plt.ion()

    fig, ax1 = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.35, top=0.95, right=0.89, wspace=0, hspace=0)

    l1, = plt.plot(t_serie, v_serie)
    l2, = plt.plot(t_serie, vrms_serie)

    plt.grid(True)
    update_plot()
    setting_sliders()
    ax1.set_ylabel(r'Amplitud [v]')
    secax_y = ax1.secondary_yaxis('right', functions=(
        dimmer.convert_rms_duty, dimmer.convert_rms_duty))
    secax_y.set_ylabel(r'Duty [%]')
    plt.show(block=True)


def gen_data():
    t_serie = np.linspace(0, dimmer.periode, 100)
    v_serie = [dimmer.v_dimmer(t) for t in t_serie]
    vrms_serie = dimmer.vrms_simbolic() * np.ones(len(t_serie))
    return [t_serie, v_serie, vrms_serie]


def update_plot():
    global fig, ax1, l1, l2
    t_serie, v_serie, vrms_serie = gen_data()
    # Plot data
    l1.set_xdata(t_serie), l2.set_xdata(t_serie)
    l1.set_ydata(v_serie), l2.set_ydata(vrms_serie)
    # Update legend
    sine_str = r'$v(t) = \mathcal{A} \mathrm{sin}(2 \omega t)$'
    rms_str = "RMS: {:.5f}".format(vrms_serie[0])
    ax1.legend([sine_str, rms_str])
    # Update limits
    ax1.set_xlim(0, dimmer.periode)
    ax1.set_ylim(-dimmer.amplitud, dimmer.amplitud)


def setting_sliders():
    global ax_frec, ax_amp, ax_tInt, ax_duty, ax_solve, ax_table
    global slide_frec, slide_amp, slide_tInt, slide_duty, btn_solve, btn_table
    
    def update_sliders(val):
        dimmer.frequency      = slide_frec.val
        dimmer.amplitud       = slide_amp.val
        dimmer.time_interrupt = dimmer.periode * 0.5 * slide_tInt.val / 100
        vrms_max              = np.sqrt(2) * 0.5 * dimmer.amplitud
        slide_duty.set_val(100 * dimmer.vrms_simbolic() / vrms_max)
        update_plot()

    def do_tint_solve(val):
        tint = dimmer.solve_tint_for_duty(slide_duty.val)
        slide_tInt.set_val(100 * tint / (dimmer.periode * 0.5))
        dimmer.print_dimmer_state()
    
    def do_tint_table_solve(val):
        for i in range(100+1):
            tint = dimmer.solve_tint_for_duty(i)
            print(f"duty({tint*1e3:>13.10f} ms)= {i:>6.2f}%")
        dimmer.print_dimmer_state()
            
    ax_frec    = plt.axes([0.12, 0.10, 0.80, 0.03])
    ax_amp     = plt.axes([0.12, 0.15, 0.80, 0.03])
    ax_tInt    = plt.axes([0.12, 0.20, 0.60, 0.03])
    ax_table   = plt.axes([0.80, 0.20, 0.10, 0.03])
    ax_duty    = plt.axes([0.12, 0.25, 0.60, 0.03])
    ax_solve   = plt.axes([0.80, 0.25, 0.10, 0.03])
    slide_frec = Slider(ax_frec, 'Frec Hz', 1.0, 50, valinit=1,  valstep=1)
    slide_amp  = Slider(ax_amp,  'Ampl V', 1.0, 311, valinit=1,  valstep=1)
    slide_tInt = Slider(ax_tInt, 'Int. %', 0.0, 100, valinit=50, valstep=1)
    slide_duty = Slider(ax_duty, 'Duty %', 0.0, 100, valinit=50, valstep=1)
    btn_table  = Button(ax_table,'Table')
    btn_solve  = Button(ax_solve,'Solve')
    slide_frec.on_changed(update_sliders)
    slide_amp.on_changed(update_sliders)
    slide_tInt.on_changed(update_sliders)
    btn_solve.on_clicked(do_tint_solve)
    btn_table.on_clicked(do_tint_table_solve)


if __name__ == "__main__":
    main()
