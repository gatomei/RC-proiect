import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Client import Client
from Server import Server
import datetime



if __name__ == '__main__':

    server = Server()
    client = Client("")

    window = tk.Tk()
    window.minsize(600, 500)
    window.title("Selective Repeat")
    window.configure(background='black')

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


    T = tk.Text(window, height=2, width=25)
    T.place(relx=0.005, rely=0.1)
    T.insert(tk.END, "Client IP: " + client.clientIP + "\nClient Port: " + str(client.clientPort))

    T = tk.Text(window, height=2, width=25)
    T.place(relx=0.005, rely=0.18)
    T.insert(tk.END, "Server IP: " + server.serverIP + "\nServer Port: " + str(server.serverPort))

    def start_transfer():

        if client.filename not in ('fisier.txt', 'fisier1.txt', 'fisier2.txt'):
            messagebox.showerror("Error", "File name not selected!")

        else:

            T = tk.Text(window, height=2, width=60)
            T.place(relx=0.005, rely=0.36)
            T.insert(tk.END, str(datetime.datetime.now()) + ": Starting file transfer...")

            server.open_com()
            client.open_com()
            client.run()
            server.run()

            T = tk.Text(window, height=2, width=60)
            T.place(relx=0.005, rely=0.50)
            T.insert(tk.END, str(datetime.datetime.now()) + ": Ending file transfer...")



    button = ttk.Button(window, text="Start transfer ", command=start_transfer)
    button.place(relx=0.005, rely=0.28)

    window.mainloop()

