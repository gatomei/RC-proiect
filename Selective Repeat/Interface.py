import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Client import Client
from Server import Server
import datetime
from threading import Thread

if __name__ == '__main__':

    server = Server()
    client = Client("")

    window = tk.Tk()
    window.minsize(600, 500)
    window.title("Selective Repeat")
    window.configure(background='black')

    flag = 0


    label = ttk.Label(window, text="Choose A File")
    label.grid(column=0, row=0)

    filename = tk.StringVar()
    combobox = ttk.Combobox(window, width=15, textvariable=filename)
    combobox['values'] = ('fisier.txt', 'fisier1.txt', 'fisier2.txt')
    combobox.grid(column=1, row=0)


    def select_file():
        global client
        client = Client(combobox.getvar('PY_VAR0'))

    button = ttk.Button(window, text="OK", command=select_file)
    button.grid(column=1, row=1)

    label_ClientIP = ttk.Label(window, text = "Client IP")
    label_ClientIP.place(relx=0.005, rely=0.1)
    label_ServerIP = ttk.Label(window, text="Server IP")
    label_ServerIP.place(relx = 0.005, rely=0.15)

    entry_ClientIP = ttk.Entry(window)
    entry_ClientIP.place(relx = 0.12, rely=0.1)
    entry_ClientIP.insert(0, client.getClientIP())
    entry_ServerIP = ttk.Entry(window)
    entry_ServerIP.place(relx = 0.12, rely=0.15)
    entry_ServerIP.insert(0, server.getServerIP())

    label_ClientPort = ttk.Label(window, text="Client Port")
    label_ClientPort.place(relx=0.005, rely=0.24)
    label_ServerPort = ttk.Label(window, text="Server Port")
    label_ServerPort.place(relx=0.005, rely=0.29)

    entry_ClientPort = ttk.Entry(window)
    entry_ClientPort.place(relx=0.12, rely=0.24)
    entry_ClientPort.insert(0, client.getClientPort())
    entry_ServerPort = ttk.Entry(window)
    entry_ServerPort.place(relx=0.12, rely=0.29)
    entry_ServerPort.insert(0, server.getServerPort())


    def start_transfer():

        if client.filename not in ('fisier.txt', 'fisier1.txt', 'fisier2.txt'):
            messagebox.showerror("Error", "File name not selected!")

        else:

            T = tk.Text(window, height=2, width=60)
            T.place(relx=0.005, rely=0.77)
            T.insert(tk.END, str(datetime.datetime.now()) + ": Starting file transfer...")

            server.setServerIP(entry_ServerIP.get())
            server.setServerPort(int(entry_ServerPort.get()))
            client.setClientIP(entry_ClientIP.get())
            client.setClientPort(int(entry_ClientPort.get()))
            server.open_com()
            client.open_com()
            thread_server = Thread(target=server.run)
            thread_client = Thread(target=client.run)
            thread_server.start()
            thread_client.start()

            thread_client.join()
            thread_server.join()

            server.close()
            client.close()

            T = tk.Text(window, height=2, width=60)
            T.place(relx=0.005, rely=0.87)
            T.insert(tk.END, str(datetime.datetime.now()) + ": Ending file transfer...")



    button = ttk.Button(window, text="Start transfer ", command=start_transfer)
    button.place(relx=0.005, rely=0.40)

    window.mainloop()


