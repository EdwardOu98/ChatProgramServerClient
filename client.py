import string
from socket import *
from select import select
import tkinter as tk
import tkinter.messagebox
import sys

ip_port = ('127.0.0.1', 8080)
buffer_size = 8192
p = socket(AF_INET, SOCK_STREAM)


class LoginWindow:
    def __init__(self, master, client):
        self.master = master
        self.master.title('Global Connections Login/Registration Window')
        self.master.geometry('480x300+200+200')
        self.master.minsize(width=480, height=300)
        self.master.maxsize(width=480, height=300)
        self.master.config(bg='black')
        self.titleLabel = tk.Label(self.master, text="Please Enter Your Information", font=('calibri', 24, 'bold'),
                                   bg='black', fg='white')
        self.titleLabel.place(relx=0.05, rely=0.01)
        self.usrn_label = tk.Label(self.master, text="Username: ", font=('calibri', 16, 'bold'), bg='black', fg='white')
        self.usrn_label.place(relx=0.05, rely=0.2)
        self.usrn_entry = tk.Entry(self.master)
        self.usrn_entry.place(relx=0.32, rely=0.2, width=300)
        self.pw_label = tk.Label(self.master, text="Password: ", font=('calibri', 16, 'bold'), bg='black', fg='white')
        self.pw_label.place(relx=0.05, rely=0.4)
        self.pw_entry = tk.Entry(self.master, show='*')
        self.pw_entry.place(relx=0.32, rely=0.4, width=300)
        self.clearBTN = tk.Button(self.master, text='Clear Entry', command=self.cleartext, height=1, width=10,
                                  font=('calibri', 16, 'bold'))
        self.clearBTN.place(relx=0.5, rely=0.6)
        self.loginBTN = tk.Button(self.master, text='Login',
                                  command=lambda: self.login(self.usrn_entry.get(), self.pw_entry.get(), client),
                                  height=1, width=10, font=('calibri', 16, 'bold'))
        self.loginBTN.place(relx=0.2, rely=0.6)
        self.RegBTN = tk.Button(self.master, text='Register',
                                command=lambda: self.register(self.usrn_entry.get(), self.pw_entry.get(), client),
                                height=1, width=10, font=('calibri', 16, 'bold'))
        self.RegBTN.place(relx=0.2, rely=0.8)
        self.exitBTN = tk.Button(self.master, text='Exit', command=self.closewindow, height=1, width=10,
                                 font=('calibri', 16, 'bold'))
        self.exitBTN.place(relx=0.5, rely=0.8)

    def login(self, username, pswd, client):
        try:
            client.connect(('127.0.0.1', 8080))
        except timeout:
            print('Socket error: timeout')

    def register(self, username, pswd, p):
        try:
            p.connect(('127.0.0.1', 8080))
        except timeout:
            print('Socket error: timeout')

    def cleartext(self):
        self.usrn_entry.delete(0, tk.END)
        self.pw_entry.delete(0, tk.END)

    def closewindow(self):
        terminate = tkinter.messagebox.askyesno('Confirmation', 'Do you want to terminate the program?')
        if terminate > 0:
            self.master.destroy()
            sys.exit()
        else:
            pass


def main():
    root = tk.Tk()
    app = LoginWindow(root, p)
    root.mainloop()


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
