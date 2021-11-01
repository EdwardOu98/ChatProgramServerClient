import string
from socket import *

ip_port = ('127.0.0.1', 8080)
buffer_size = 4096
p = socket(AF_INET, SOCK_STREAM)


def getheader(x, msg):
    if x == '1':
        return 'LGI_' + msg
    elif x == '2':
        return 'REG_' + msg
    elif x == '3':
        return 'MSG_' + msg
    elif x == '4':
        return 'LGO_' + msg
    elif x == '0':
        return 'EXT_' + msg



try:
    p.connect(ip_port)

    while 1:
        msg_type = input('Please enter your message type: ')
        if msg_type not in string.digits:
            continue
        msg = input('Please enter your message: ')
        if not msg:
            continue
        msg = getheader(msg_type, msg)
        p.send(msg.encode('utf-8'))
        msg = p.recv(buffer_size)
        print(msg.decode('utf-8'))
        if msg_type == '0':
            break
except timeout:
    print('Socket error: timeout')
except error:
    print('Socket error: could not connect to server')
p.close()
