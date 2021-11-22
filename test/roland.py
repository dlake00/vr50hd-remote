import socket
import time

from enum import Enum

class vr50hd(socket.socket):
    # ROLAND SOCKET INITIALISE
    # create IPv4 STREAMing socket
    # @param self
    # @return None
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    # ROLAND MIXER CONNECT
    # @param self
    # @param IP_ADDR: string, IPv4 address (xxx.xxx.xxx.xxx)
    # @return reply
    def mix_connect(self, IP_ADDR):
        TCP_IP = IP_ADDR
        TCP_PORT = 8023

        try:
            print("ATTEMPT CONNECT TO VR50HD ON: " + str(TCP_IP))
            self.connect((TCP_IP, TCP_PORT))

            # read VR50HD response
            msg = self.recv(1024)

            # check for "Welcome" ASCII response from mixer
            if msg == b'Welcome to VR-50HD MKII.\r\n>':
                return

            else:
                # if not "OK" then return error
                return

        # exception to handle incorrect IP address
        except OSError as error:
            print(error)
            return

    # ROLAND MIXER DISCONNECT
    # @param self
    # @return reply
    def mix_disconnect(self):
        super().close()
        return

    class Status(Enum):
        mix_off = 0, "OFF"
        mix_on = 1, "ON"
        mix_cnnct = 2, "CONNECTED"
        mix_dcnnct = 3, "DISCONNECTED"
        mix_error = 4, "MIXER ERROR"
        sock_error = 5, "SOCKET ERROR"

    class Source(Enum):
        sdi_1 = 0, "SDI 1"
        sdi_2 = 1, "SDI 2"
        sdi_3 = 2, "SDI 3"
        sdi_4 = 3, "SDI 4"
        hdmi_1 = 4, "HDMI 1"
        hdmi_2 = 5, "HDMI 2"
        hdmi_3 = 6, "HDMI 3"
        hdmi_4 = 7, "HDMI 4"
        comp_1 = 8, "COMPOSITE 1"
        comp_2 = 9, "COMPOSITE 2"
        rgb_1 = 10, "RGB / COMPONENT 1"
        rgb_2 = 11, "RGB / COMPONENT 2"

    class Input(Enum):
        0 = [0, "VIDEO", "VIDEO 1"]
        1 = [1, "VIDEO", "VIDEO 2"]
        2 = [2, "VIDEO", "VIDEO 3"]
        3 = [3, "VIDEO", "VIDEO 4"]
        4 = [4, "PinP", "PinP"]
        5 = [5, "PinP", "PinP / Key"]
        6 = [6, "PGM", "PROGRAM"]
        7 = [7, "STILL", "STILL 1"]
        8 = [8, "STILL", "STILL 2"]
        9 = [9, "STILL", "STILL 3"]
        10 = [10, "STILL", "STILL 4"]
    
    def rtn_Input(self, i):
        return self.Input[i][2]

    # ROLAND SEND COMMAND
    # @param self
    # @param str: string, command to send to VR50HD in ASCII format
    # @return reply
    def mix_send(self, str):
        cmd = str

        try:
            # encode command to ascii format
            # send command, sleep 100ms, receive response
            self.send(cmd.encode("ascii"))
            time.sleep(0.1)
            msg = self.recv(1024)

            # check for OK response
            if msg == b'\r\n>OK\r\n>':
                return
            # check for QPG response
            elif msg.decode("ascii")[3] == "Q":
                # qpg = int(msg.decode("ascii")[7])
                return
            # check for UVS response
            elif msg.decode("ascii")[3] == "U":
                return
            # check for VER response
            elif msg.decode("ascii")[3] == "V":
                return
            else:
                # handle no valid response
                return

        # handle socket error
        except socket.error:
            return

    def test_cmd(self, i):
        msg = self.rtn_Input(i)
        print(msg)
        return msg

    # SET PGM INPUT
    # sends PGM command to Roland mixer and switches current PGM video
    # @param self
    # @param i: int, requested pgm 0 <= i <= 4
    # @return reply
    def pgm(self, i):
        cmd = "PGM:" + str(i) + ";"
        if i == 4:
            i = 7
        else:
            i
        self.mix_send(cmd)

        msg = self.rtn_Input(i)
        
        return ("PGM changed to: " + msg)

    # ROLAND REPLY HANDLER
    # @param self
    # @param src: int, selects type of message
    # @param i: int, gets content of message
    # @return status, input, except: string, completed message
    """
    def mix_reply(self, type, i):
        if type == 0:
            status = {
                0: "OFF",
                1: "ON",
                2: "CONNECTED",
                3: "DISCONNECTED",
                4: "MIXER ERR",
                5: "SOCKET ERR"
            }
            return status.get(i, "UNKNOWN ERR")

        elif type == 1:
            video = {
                0: "VIDEO 1",
                1: "VIDEO 2",
                2: "VIDEO 3",
                3: "VIDEO 4"
            }
            return video.get(i, "INPUT ERR")

        elif type == 2:
            still = {
                0: "STILL 1",
                1: "STILL 2",
                2: "STILL 3",
                3: "STILL 4"
            }
            return still.get(i, "STILL ERROR")

        elif type == 3:
            sdi = {
                0: "SDI 1",
                1: "SDI 1",
                2: "SDI 3",
                3: "SDI 4"
            }
            return sdi.get(i, "SOURCE ERROR")

        elif type == 4:
            hdmi = {
                4: "HDMI 1",
                5: "HDMI 2",
                6: "HDMI 3",
                7: "HDMI 4"
            }
            return hdmi.get(i, "SOURCE ERROR")

        elif type == 5:
            composite = {
                8: "COMPOSITE 1",
                9: "COMPOSITE 2"
            }
            return composite.get(i, "SOURCE ERROR")

        elif type == 6:
            component = {
                10: "RGB / COMPONENT 1",
                11: "RGB / COMPONENT 2"
            }
            return component.get(i, "SOURCE ERROR")

        elif type == 7:
            transition = {
                0: "CUT",
                1: "MIX",
                2: "WIPE"
            }
            return transition.get(i, "TRANSITION ERROR")

        else:
            return "EXCEPT"
            """