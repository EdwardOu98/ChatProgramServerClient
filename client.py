from socket import *

ip_port = ('127.0.0.1', 8080)
p = socket(AF_INET, SOCK_STREAM)
p.connect(ip_port)

while 1:
    msg = input('Please enter your message: ')
    if not msg:
        continue
    p.send(msg.encode('utf-8'))
    if msg == '1':
        break

p.close()
