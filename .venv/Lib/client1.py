import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import datetime

HOST = '127.0.0.1'
PORT = 12345
client_socket = None
connected = False
username = ""

def connect_to_server():
    global client_socket, connected, username
    username = simpledialog.askstring("Username", "Enter your username:")
    if not username:
        messagebox.showwarning("Username Required", "You must enter a username to connect.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(username.encode())
        connected = True
        log_message(f"[Connected as {username}]", "system")
        threading.Thread(target=receive_messages, daemon=True).start()
        connect_btn.config(state='disabled')
        disconnect_btn.config(state='normal')
        send_btn.config(state='normal')
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
