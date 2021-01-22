from abc import ABC, abstractmethod

packet_fixed_header = {
    'CONNECT': b'\x10',
    'CONNACK': b'\x20',
    'PUBLISH': b'\x30',
    'PUBACK': b'\x40',
    'PUBREC': b'\x50',
    'PUBREL': b'\x62',
    'PUBCOMP': b'\x70',
    'SUBSCRIBE': b'\x82',
    'SUBACK': b'\x90',
    'UNSUBSCRIBE': b'\xA2',
    'UNSUBACK': b'\xB0',
    'PINGREQ': b'\xC0',
    'PINGRESP': b'\xD0',
    'DISCONNECT': b'\xE0',
    'AUTH': b'\xF0',
}

""" Clasa abstracta Packet
    -> daca serverul nu primeste un pachet connect in timp util dupa Network Connection atunci serverul ar trebui sa inchida Network Connection  """
class Packet(ABC):

    @abstractmethod
    def parse(self):
        pass


""" Implementare clasa Connect-> creaza pachet connect """
class Connect(Packet):

    qos = 0

    packet_payload = {
        'client_id': bytearray(),  """ identififica clientul fata de server-> UTF-8"""
                                   'will_topic': bytearray(),
        'will_topic': bytearray(),
        'will_payload': bytearray(),
        'username': "",
        'password': ""
    }
    packet_variable_header = {
        'protocol_name': "MQTT",
        'version': b'\x05',
        'connect_flags': b'\x02',  # connect flags
        'keep_alive': b'\x00\x05',  # keep alive
        'properties': b'\x11\x00\x00\x00\x0a',  # properties
    }

    def set_qos(self, _qos):
        self.qos = _qos

    def set_username(self, _username):
        self.packet_payload['username'] = _username

    def set_password(self, _password):
        self.packet_payload['password'] = _password

    def parse(self):
        packet = bytearray()  # initialize the packet to be sent
        variable_header = bytearray()  # initialize an empty byte array to create the variable header

        # Fixed header
        packet += packet_fixed_header['CONNECT']

        # Variable header
        variable_header += b'\x00'  # Add a offset to the length field
        variable_header += bytes([len(self.packet_variable_header['protocol_name'])])
        variable_header += self.packet_variable_header['protocol_name'].encode('UTF-8')
        variable_header += self.packet_variable_header['version']  # version 5
        variable_header += self.packet_variable_header['connect_flags']
        variable_header += self.packet_variable_header['keep_alive']
        variable_header += bytes([len(self.packet_variable_header['properties'])])
        variable_header += self.packet_variable_header['properties']

        # Payload
        payload = b'\x00'
        payload += bytes([len(self.packet_payload['username'])])
        payload += self.packet_payload['username'].encode('UTF-8')
        variable_header += payload

        # Arrange the final packet
        packet_length = bytes([len(variable_header)])  # calculate the length of the remaining packet
        packet += packet_length  # add the length as bytes to the packet
        packet += variable_header  # add the whole variable_header to the packet
        return packet
