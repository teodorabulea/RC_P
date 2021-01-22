import socket
import traceback

""" Creare o clasa Connection pentru transferul de pachete in socket. """
class Connection:

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.settimeout(30)
        self.__host_ip = socket.gethostbyname('mqtt.eclipse.org')

    """ Creare conexiune a socketului catre host ip. """
    def establish_connection(self):
        print("ip:", self.__host_ip)
        try:
            self.__socket.connect((self.__host_ip, 1883))
        except socket.error:
            traceback.print_exc()

    def set_host_ip(self, _ip):
        self.__host_ip = _ip

    """ Trimitere pachete(byte array). """
    def send(self, packet):
        self.__socket.sendall(packet)

    """ Inchidere socket. """
    def close(self):
        self.__socket.close()

    """ Primire pachete(byte array). """
    def receive(self, byte_size):
        return self.__socket.recv(byte_size)