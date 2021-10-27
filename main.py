import roland
import tkinter as tk


def socket_create():
    # create custom Roland socket instance
    global mixer
    mixer = roland.vr50hd()

    socket_connect()
    return

def socket_connect():
    # get IP from user input
    IP = entry_ip.get()

    # send connect cmd
    cmd = mixer.mix_connect(IP)

    # update label text
    label_ip_status.config(text=cmd)

    print(cmd)
    return

def socket_drop():
    try:
        mixer
    except NameError:
        return
    else:    
        cmd = mixer.mix_disconnect()
        label_ip_status.config(text=cmd)
        print(cmd)
    return

def qpg():
    cmd = mixer.qpg()
    print("qpg: " + cmd)

def pgm(i):
    cmd = mixer.pgm(i)
    label_pgm.config(text="PGM: " + cmd)
    print("pgm: " + cmd)

def aux(i):
    cmd = mixer.aux(i)
    label_aux.config(text="AUX: " + cmd)
    print("aux: " + cmd)

def pip(i):
    cmd = mixer.pip(i)
    label_pip.config(text="PinP: " + cmd)
    if i == 1:
        btn_pip0.config(command=lambda: pip(0))
    else:
        btn_pip0.config(command=lambda: pip(1))
    print("PinP: " + cmd)

def pky(i):
    cmd = mixer.pky(i)
    label_pky.config(text="PinP KEY: " + cmd)
    if i == 1:
        btn_pky0.config(command=lambda: pky(0))
    else:
        btn_pky0.config(command=lambda: pky(1))
    print("PinP KEY: " + cmd)

def sky(i):
    cmd = mixer.sky(i)
    label_sky.config(text="Still KEY: " + cmd)
    if i == 1:
        btn_sky0.config(command=lambda: sky(0))
    else:
        btn_sky0.config(command=lambda: sky(1))
    print("Still KEY: " + cmd)

def fde(i):
    cmd = mixer.fde(i)
    label_fde.config(text="Output Fade: " + cmd)
    if i == 1:
        btn_fde0.config(command=lambda: fde(0))
    else:
        btn_fde0.config(command=lambda: fde(1))
    print("Output Fade: " + cmd)

def app_exit():
    socket_drop()
    exit()

# ! INTERFACE ! #

# initialise tkinter window
window = tk.Tk()
window.title("VR50HD Remote Control")
#window.geometry("320x640")

# frames
ip_frame = tk.Frame(window, padx = 10, pady = 10)
ip_frame.pack()

pgm_frame = tk.Frame(window, padx = 10, pady = 10)
pgm_frame.pack()

aux_frame = tk.Frame(window, padx = 10, pady = 10)
aux_frame.pack()

pip_frame = tk.Frame(window, padx = 10, pady = 10)
pip_frame.pack()

# grids

# connection management interface
label_ip = tk.Label(ip_frame, text="IPv4 Address:")
label_ip.grid(row = 0, column = 0)
entry_ip = tk.Entry(ip_frame)
entry_ip.grid(row = 1, column = 0, columnspan= 3, pady = 10, ipadx = 60)
label_ip_status = tk.Label(ip_frame, text="NOT CONNECTED")
label_ip_status.grid(row = 0, column = 2)
btn_ip_c = tk.Button(ip_frame, height = 3, width = 8, text="Connect", command=socket_create)
btn_ip_c.grid(row = 2, column = 0)
btn_ip_d = tk.Button(ip_frame, height = 3, width = 8, text="Disconnect", command=socket_drop)
btn_ip_d.grid(row = 2, column = 1)

# pgm interface
label_pgm = tk.Label(pgm_frame, text="PGM:")
label_pgm.grid(row = 0, column = 0)
btn_pgm0 = tk.Button(pgm_frame, height = 3, width = 8, text="Video 1", command=lambda: pgm(0))
btn_pgm0.grid(row = 1, column = 0)
btn_pgm1 = tk.Button(pgm_frame, height = 3, width = 8, text="Video 2", command=lambda: pgm(1))
btn_pgm1.grid(row = 1, column = 1)
btn_pgm2 = tk.Button(pgm_frame, height = 3, width = 8, text="Video 3", command=lambda: pgm(2))
btn_pgm2.grid(row = 1, column = 2)
btn_pgm3 = tk.Button(pgm_frame, height = 3, width = 8, text="Video 4", command=lambda: pgm(3))
btn_pgm3.grid(row = 1, column = 3)
btn_pgm4 = tk.Button(pgm_frame, height = 3, width = 8, text="Still", command=lambda: pgm(4))
btn_pgm4.grid(row = 2, column = 0)

# aux interface
label_aux = tk.Label(aux_frame, text="AUX:")
label_aux.grid(row = 0, column = 0)
btn_aux0 = tk.Button(aux_frame, height = 3, width = 8, text="Video 1", command=lambda: aux(0))
btn_aux0.grid(row = 1, column = 0)
btn_aux1 = tk.Button(aux_frame, height = 3, width = 8, text="Video 2", command=lambda: aux(1))
btn_aux1.grid(row = 1, column = 1)
btn_aux2 = tk.Button(aux_frame, height = 3, width = 8, text="Video 3", command=lambda: aux(2))
btn_aux2.grid(row = 1, column = 2)
btn_aux3 = tk.Button(aux_frame, height = 3, width = 8, text="Video 4", command=lambda: aux(3))
btn_aux3.grid(row = 1, column = 3)
btn_aux4 = tk.Button(aux_frame, height = 3, width = 8, text="PinP", command=lambda: aux(4))
btn_aux4.grid(row = 2, column = 0)
btn_aux5 = tk.Button(aux_frame, height = 3, width = 8, text="PinP Key", command=lambda: aux(5))
btn_aux5.grid(row = 2, column = 1)
btn_aux6 = tk.Button(aux_frame, height = 3, width = 8, text="Program", command=lambda: aux(6))
btn_aux6.grid(row = 2, column = 2)

# pip interface
label_pip = tk.Label(pip_frame, text="PinP:")
label_pip.grid(row = 0, column = 0)
btn_pip0 = tk.Button(pip_frame, height = 3, width = 8, text="Toggle", command=lambda: pip(1))
btn_pip0.grid(row = 1, column = 0)

# pky interface
label_pky = tk.Label(pip_frame, text="PinP KEY:")
label_pky.grid(row = 0, column = 1)
btn_pky0 = tk.Button(pip_frame, height = 3, width = 8, text="Toggle", command=lambda: pky(1))
btn_pky0.grid(row = 1, column = 1)

# sky interface
label_sky = tk.Label(pip_frame, text="Still KEY:")
label_sky.grid(row = 0, column = 2)
btn_sky0 = tk.Button(pip_frame, height = 3, width = 8, text="Toggle", command=lambda: sky(1))
btn_sky0.grid(row = 1, column = 2)

# fde interface
label_fde = tk.Label(pip_frame, text="Output Fade:")
label_fde.grid(row = 0, column = 3)
btn_fde0 = tk.Button(pip_frame, height = 3, width = 8, text="Toggle", command=lambda: fde(1))
btn_fde0.grid(row = 1, column = 3)

# exit interface
btn_exit = tk.Button(window, text="Exit", command=app_exit)
btn_exit.pack()

window.mainloop()