from socket import *
from threading import *
from select import select

ip_port = ('127.0.0.1', 8080)
back_log = 5
buffer_size = 4096
server = socket(AF_INET, SOCK_STREAM)
CONTINUE = True
close_msg = 'Connection to server closed'
recv_msg = 'Message received'


def ser_loop():
    global CONTINUE
    while 1:
        server.listen(back_log)
        ready, _, _ = select([server], [], [], 1)
        if ready:
            con, addr = server.accept()
            while 1:
                try:
                    msg = con.recv(buffer_size)
                    if msg.decode('utf-8') == '1':
                        con.send(close_msg.encode('utf-8'))
                        con.close()
                    con.send(recv_msg.encode('utf-8'))
                    print('Message: ', msg.decode('utf-8'))
                except Exception as e:
                    break
        if not CONTINUE:
            break


def main():
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(ip_port)


if __name__ == '__main__':
    try:
        main()
        t0 = Thread(target=ser_loop)
        t0.start()
        m = input('Press <Enter> key to exit')
        CONTINUE = False
        t0.join()
    finally:
        server.close()
