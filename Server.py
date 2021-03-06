from socket import *
from threading import *
from select import select
import os.path
import json

ip_port = ('127.0.0.1', 8080)
back_log = 5
buffer_size = 4096
server = socket(AF_INET, SOCK_STREAM)
CONTINUE = True
close_msg = 'EXT_Connection to server closed'
recv_msg = 'MSR_Message received'
reg_msg_succ = 'RES_Registration success'
reg_msg_fail = 'REF_Registration failed! Username already exist'
login_succ = 'LIS_Successfully login as '
login_fail_usn = 'LIF_Username not found'
login_fail_psw = 'LIF_Incorrect password'


def ser_loop():
    global CONTINUE
    global reg_msg_succ
    global reg_msg_fail
    global recv_msg
    global close_msg
    while 1:
        server.listen(back_log)
        ready, _, _ = select([server], [], [], 1)
        if ready:
            con, addr = server.accept()
            while 1:
                try:
                    msg = con.recv(buffer_size).decode('utf-8')
                    header, body = msg.split('_', 1)
                    if header == 'EXT':
                        con.send(close_msg.encode('utf-8'))
                        con.close()
                    elif header == 'REG':
                        usrname, pswd = body.split('_', 1)
                        status = register(usrname, pswd)
                        if status:
                            con.send(reg_msg_succ.encode('utf-8'))
                        else:
                            con.send(reg_msg_fail.encode('utf-8'))
                    elif header == 'LGI':
                        usrname, pswd = body.split('_', 1)
                        status = login(usrname, pswd)
                        if status == 1:
                            con.send(login_succ.encode('utf-8'))
                        elif status == 0:
                            con.send(login_fail_usn.encode('utf-8'))
                        else:
                            con.send(login_fail_psw.encode('utf-8'))
                    # con.send(recv_msg.encode('utf-8'))
                    print('Message: ', body)
                except Exception as e:
                    break
        if not CONTINUE:
            break


def register(usrname, pswd):
    filename = 'userinfo.json'
    userinfo = {}
    if os.path.exists(filename):
        file = open(filename, 'r')
        userinfo = json.load(file)
        for key in userinfo:
            if key == usrname:
                file.close()
                return False
    file = open(filename, 'r+')
    userinfo[usrname] = pswd
    json.dump(userinfo, file)
    file.close()
    print('Registration completed')
    return True


def login(username, password):
    userinfo = {}
    file = open('userinfo.json', 'r')
    userinfo = json.load(file)
    ex_flag = False
    for key in userinfo:
        if key == username:
            ex_flag = True
            break
    if not ex_flag:
        return 0  # username not found
    if userinfo[username] == password:
        return 1  # login is successful
    return -1   # incorrect password


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
