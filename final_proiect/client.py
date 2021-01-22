"""default host
broker test host
mqtt.eclipse.org
port 1883"""

import connection as conn
from packet_struct import *
from packets import *
import queue

result = queue.Queue()


""" Clasa Client defineste comportamentul utilizatorului"""
class Client:

    def __init__(self, client_id, username=None, password=None, host_ip=None, qos=0):
        self.__username = username
        self.__client_id = client_id
        self.__password = password
        self.__host_ip = host_ip
        self.__topic_publish = ""
        self.__message_publish = ""
        self.__topics = []
        self.__unsubscribe_topics = []
        self.__connection = conn.Connection()
        self.__is_connected = False
        self.__struct = packet_struct()
        self.__qos = qos

    """ Conectarea """
    def connect(self):
        self.__connection.establish_connection()
        if self.__host_ip is not None:
            self.__connection.set_host_ip(self.__host_ip)

        connect_packet = Connect()
        connect_packet.set_username(self.__username)
        connect_packet.set_password(self.__password)
        connect_packet.set_qos(self.__qos)
        packet = connect_packet.parse()

        self.__connection.send(packet)  # Send the connect packet
        self.__struct.byte_code = self.__connection.receive(1024)  # Receive the response packet
        assert self.__struct.byte_code[0:1] == packet_fixed_header['CONNACK']

        """Pachetul primit este un pachet de confirmare."""
        if self.__struct.byte_code[3:4] == b'\x00':  # Verificare:byte3= 0-> success
            self.__is_connected = True
            self.__struct.message = "Connect: success."
            result.put(self.__struct)
        else:
            self.__struct.message = "Connect: failed."
            result.put(self.__struct)


    def get_connection(self):
        return self.__connection

    """ Metoda getter """
    def get_is_connected(self):
        return self.__is_connected

if __name__ == "__main__":

    client = None
    username = input("Username = ")
    password = input("Password = ")
    qos=input("qos=")
    client=Client("123", username=username, password=password, qos=qos)
    client.connect()
