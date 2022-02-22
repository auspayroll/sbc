import socket

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
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

print(bytesToSend)
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])

print(msg)