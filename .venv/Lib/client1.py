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


def disconnect_from_server():
    global connected
    if connected:
        try:
            client_socket.close()
            connected = False
            log_message("[Disconnected]", "system")
        except:
            pass
    connect_btn.config(state='normal')
    disconnect_btn.config(state='disabled')
    send_btn.config(state='disabled')


def send_message():
    msg = msg_entry.get()
    if msg and connected:
        try:
            client_socket.send(msg.encode())
            timestamp = datetime.datetime.now().strftime("%H:%M")
            display_bubble(f"You", msg, timestamp, align='right', bg='#DCF8C6')
            msg_entry.delete(0, tk.END)
        except:
            log_message("[Error sending message]", "system")


def receive_messages():
    while connected:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                parts = msg.split(": ", 1)
                if len(parts) == 2:
                    sender, content = parts
                    timestamp = datetime.datetime.now().strftime("%H:%M")
                    align = 'left' if sender != username else 'right'
                    bg = '#E5E5EA' if sender != username else '#DCF8C6'
                    display_bubble(sender, content, timestamp, align=align, bg=bg)
                else:
                    log_message(msg, "system")
        except:
            break


def log_message(msg, tag):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, msg + "\n", tag)
    chat_area.config(state='disabled')
    chat_area.see(tk.END)


def display_bubble(sender, message, timestamp, align='left', bg='#E5E5EA'):
    chat_area.config(state='normal')
    bubble = f"{sender}: {message}\n{timestamp}"
    chat_area.insert(tk.END, f"{bubble}\n", align)
    chat_area.tag_configure('left', justify='left', lmargin1=10, background=bg, spacing3=5)
    chat_area.tag_configure('right', justify='right', rmargin=10, background=bg, spacing3=5)
    chat_area.config(state='disabled')
    chat_area.see(tk.END)
