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

def test_cmd(i):
    cmd = mixer.test_cmd(i)
    print("test: " + cmd)

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

btn_test_cmd = tk.Button(text="test", command= lambda: test_cmd(1))
btn_test_cmd.pack()

# exit interface
btn_exit = tk.Button(window, text="Exit", command=app_exit)
btn_exit.pack()

window.mainloop()