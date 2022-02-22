import socket
import io
import re
import pdb
bytesToSend         = b'REGISTER sip:192.168.56.8 SIP/2.0\r\n\
Via: SIP/2.0/UDP 192.168.56.7:5060;rport;branch=z9hG4bKPjbbb623d6-20c8-4cfa-92ad-f92e37dbf825\r\n\
Max-Forwards: 70\r\n\
From: <sip:testclient@192.168.56.8>;tag=02fb5ff4-55b8-4c01-8741-3bd5f2e90249\r\n\
To: <sip:testclient@192.168.56.8>\r\n\
Call-ID: 590f1cbf-b0fc-45fe-9591-42aacd021473\r\n\
CSeq: 41493 REGISTER\r\n\
Contact: <sip:testclient@192.168.56.7:5060;ob>\r\n\
Expires: 300\r\n\
Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS\r\n\
Content-Length:  0\r\n'

register_pattern = re.compile(r'(?P<verb>REGISTER|INVITE)\s+sip:(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+SIP\/2\.0', re.IGNORECASE)

# sip address pattern 
sip_pattern = re.compile(r'\s*(?P<header>[A-Za-z-]+)\s*:\s*<sip:(?P<user>\w+)@(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:(?P<port>\d+))?\s*(;.*)?>\s*(;\s*tag=(?P<tag>[A-Za-z0-9-]+))?', re.IGNORECASE)
via_pattern = re.compile(r'Via:\s+SIP\/2\.0\/(?P<transport>UDP|TCP|TLS)\s+(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:(?P<port>\d+))?\s*(;\s*rport)?(\s*;\s*branch\s*=\s*(?P<branch>[A-Za-z0-9-]+))?', re.IGNORECASE)
cseq_pattern = re.compile(r'CSeq:\s*(?P<count>\d+)\s+(?P<verb>[A-Za-z]+)', re.IGNORECASE)
int_header = re.compile(r'\s*(?P<header>[A-Za-z-]+)\s*:\s*(?P<value>\d+)\s*$')  # headers with just an integer value
string_header = re.compile(r'\s*(?P<header>[A-Za-z-]+)\s*:\s*(?P<value>.+)')  # headers with just a string value


class Message:
    def __init__(self, messageBytes):
        self.message = messageBytes.decode('utf-8', 'ignore')
        header_list = self.message.split("\r\n")
        self._vias = [] 
        self._routes = []
        self._record_routes = []
        self._from = {'user': None, 'host': None, 'tag': False}
        self._to = {'user': None, 'host': None, 'tag': False}
        self._cseq = { 'id': None, 'action': None }   
                        
        # set request line
        register_match = re.search(register_pattern, header_list[0])
        if register_match:
            self.request_type = register_match.group('verb')
            self.request_uri = register_match.group('host')
        else:
            raise Exception("Invalid REQUEST LINE")

        for header in header_list[1:]:
            via_match = re.search(via_pattern, header)
            if via_match:
                self._vias.append(
                    { 'transport': via_match.group('transport'), 
                    'host': via_match.group('host'), 
                    'port': via_match.group('port'),
                    'branch': via_match.group('branch')
                    })
                continue
            cseq_match = re.search(cseq_pattern, header)
            if cseq_match:
                self._cseq = { 'count': cseq_match.group('count'), 
                               'verb': cseq_match.group('verb') }
                continue
            sip_match = re.search(sip_pattern, header)
            if sip_match:
                self.set_attribute(sip_match.group('header'), 
                {'host': sip_match.group('host'), 
                 'user': sip_match.group('user'),
                 'tag': sip_match.group('tag'),
                 'port': sip_match.group('port')   
                 })
                continue
            int_match = re.search(int_header, header)
            if int_match:
                self.set_attribute(int_match.group('header'), 
                        int(int_match.group('value')))
                continue
            string_match = re.search(string_header, header)
            if string_match:
                self.set_attribute(string_match.group('header'), 
                        string_match.group('value'))

    def set_attribute(self, name, value):
        name = '_' + name.replace('-', '_').lower()
        setattr(self, name, value)




message = Message(bytesToSend)
pdb.set_trace()

"""
localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")
# Listen for incoming datagrams


while(True):
    try:
        messageBytes, address = UDPServerSocket.recvfrom(bufferSize)
        message = messageBytes.decode('utf-8', 'ignore')
        register_match = re.search(register_pattern, message)
        if register_match:
            uri_ip = register_match.group('address')
        
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)
    except(io.InterruptedError):
        break
"""
