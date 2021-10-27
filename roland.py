import socket
import time

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
                return self.mix_reply(0,0)

            else:
                # if not "OK" then return error
                return self.mix_reply(0,3)

        # exception to handle incorrect IP address
        except OSError as error:
            print(error)
            return self.mix_reply(0,3)

    # ROLAND MIXER DISCONNECT
    # @param self
    # @return reply
    def mix_disconnect(self):
        super().close()
        return self.mix_reply(0,1)

    # ROLAND SEND COMMAND
    # @param self
    # @param str: string, command to send to VR50HD in ASCII format
    # @return reply
    def mix_send(self, str, type, i):
        cmd = str

        try:
            # encode command to ascii format
            # send command, sleep 100ms, receive response
            self.send(cmd.encode("ascii"))
            time.sleep(0.1)
            msg = self.recv(1024)

            # check for OK response
            if msg == b'\r\n>OK\r\n>':
                return self.mix_reply(type, i)
            # check for QPG response
            elif msg.decode("ascii")[3] == "Q":
                qpg = int(msg.decode("ascii")[7])
                return self.mix_reply(type, qpg)
            # check for UVS response
            elif msg.decode("ascii")[3] == "U":
                return self.mix_reply(type, i)
            # check for VER response
            elif msg.decode("ascii")[3] == "V":
                return self.mix_reply(type, i)
            else:
                # handle no valid response
                return self.mix_reply(0,2)

        # handle socket error
        except socket.error:
            return self.mix_reply(0,3)

    # ROLAND REPLY HANDLER
    # @param self
    # @param src: int, selects type of message
    # @param i: int, gets content of message
    # @return status, input, except: string, completed message
    def mix_reply(self, type, i):
        if type == 0:
            status = {
                0: "CONNECTED",
                1: "DISCONNECTED",
                2: "MIXER ERR",
                3: "SOCKET ERR"
            }
            return status.get(i, "UNKNOWN ERR")

        elif type == 1:
            input = {
                0: "VIDEO 1",
                1: "VIDEO 2",
                2: "VIDEO 3",
                3: "VIDEO 4",
                4: "PinP",
                5: "PinP KEY",
                6: "PROGRAM",
                7: "STILL"
            }
            return input.get(i, "INPUT ERR")

        elif type == 2:
            source = {
                0: "SDI",
                1: "HDMI",
                2: "COMPOSITE",
                3: "RGB / COMPOSITE"
            }
            return source.get(i, "SOURCE ERROR")

        elif type == 3:
            still = {
                0: "STILL 1",
                1: "STILL 2",
                2: "STILL 3",
                3: "STILL 4"
            }
            return still.get(i, "STILL ERROR")

        elif type == 4:
            on_off = {
                0: "OFF",
                1: "ON"
            }
            return on_off.get(i, "ON / OFF ERROR")

        elif type == 5:
            transition = {
                0: "CUT",
                1: "MIX",
                2: "WIPE"
            }
            return transition.get(i, "TRANSITION ERROR")

        else:
            return "EXCEPT"

    # GET PGM INPUT
    # sends QPG command to Roland mixer and returns current PGM video
    # @param self
    # @return reply
    def qpg(self):
        cmd = "QPG;"
        msg = self.mix_send(cmd, 1, 0)

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
        msg = self.mix_send(cmd, 1, i)
        
        return msg

    # SET AUX INPUT
    # sends AUX command to Roland mixer and switches current AUX video
    # @param self
    # @param i: int, requested aux 0 <= i <= 6
    # @return reply
    def aux(self, i):
        cmd = "AUX:" + str(i) + ";"
        msg = self.mix_send(cmd, 1, i)

        return msg

    # SET STILL INPUT
    # sends STS command to Roland mixer to assign still source to still
    # @param self
    # @param i: int, requested still 0 <= i <= 3
    def sts(self, i):
        cmd = "STS:" + str(i) + ";"
        msg = self.mix_send(cmd, 3, i)

        return msg

    # SET VIS INPUT
    # sends VIS command to Roland mixer to assign video source to video input
    # @param self
    # @param i: int, requested input
    # @param j: int, video source to assign
    # @return reply
    def vis(self, i, j):
        # video inputs 3 & 4 cannot be set to Composite or RGB/Component
        if 2 <= i <= 3 and 2 <= j <= 3:
            return self.mix_reply(0,2)
        else:
            cmd = "VIS:" + str(i) + "," + str(j) + ";"
            msg = self.mix_send(cmd, 1, i)

            return (msg + " set to " + self.mix_reply(2, j))

    # SET PinP ON / OFF
    # sends PIP command to Roland mixer to toggle PinP ON or OFF
    # @param self
    # @param i: int, toggle ON (1) or OFF (0)
    # @return reply
    def pip(self, i):
        cmd = "PIP:" + str(i) + ";"
        msg = self.mix_send(cmd, 4, i)

        return msg

    # SET PinP KEY ON / OFF
    # sends PKY command to Roland mixer to toggle PinP / Key ON or OFF
    # @param self
    # @param i: int, toggle ON (1) or OFF (0)
    # @return reply
    def pky(self, i):
        cmd = "PKY:" + str(i) + ";"
        msg = self.mix_send(cmd, 4, i)

        return msg

    # SET STILL KEY ON / OFF
    # sends SKY command to Roland mixer to toggle Still / Key ON or OFF
    # @param self
    # @param i: int, toggle ON (1) or OFF (0)
    # @return reply
    def sky(self, i):
        cmd = "SKY:" + str(i) + ";"
        msg = self.mix_send(cmd, 4, i)

        return msg

    # SET OUTPUT FADE ON ? OFF
    # sends FDE command to Roland mixer to toggle Output Fade ON or OFF
    # @param self
    # @param i: int, toggle ON (1) or OFF (0)
    # @return reply
    def fde(self, i):
        cmd="FDE:" + str(i) + ";"
        msg = self.mix_send(cmd, 4, i)

        return msg

    # SET TRANSITION EFFECT
    # sends TRS command to Roland mixer to change transition effect
    # @param self
    # @param i: int, requested transition effect 0 <= i <=2
    # @return reply
    def trs(self, i):
        cmd = "TRS:" + str(i) + ";"
        msg = self.mix_send(cmd, 5, i)

        return msg