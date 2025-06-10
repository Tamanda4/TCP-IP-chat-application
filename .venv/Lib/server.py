import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = '127.0.0.1'
PORT = 12345
clients = []
server_running = False
server_socket = None

def start_server():
    global server_socket, server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        log("[SERVER STARTED] Listening on {}:{}".format(HOST, PORT))
        server_running = True
        threading.Thread(target=accept_clients, daemon=True).start()
    except Exception as e:
        log(f"[ERROR] {e}")

def stop_server():
    global server_running, server_socket
    server_running = False
    for client in clients:
        client.close()
    if server_socket:
        server_socket.close()
    log("[SERVER STOPPED]")

def accept_clients():
    while server_running:
        try:
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            log(f"[CONNECTED] {addr}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
            thread.start()
        except:
            break


def handle_client(client_socket, addr):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            log(f"[{addr}] {msg}")
            broadcast(f"{addr}: {msg}", client_socket)
        except:
            break
    clients.remove(client_socket)
    client_socket.close()
    log(f"[DISCONNECTED] {addr}")


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)


def log(message):
    output.config(state='normal')
    output.insert(tk.END, message + '\n')
    output.config(state='disabled')
    output.see(tk.END)


root = tk.Tk()
root.title("TCP Server")

frame = tk.Frame(root)
frame.pack(pady=10)

start_btn = tk.Button(frame, text="Start Server", command=start_server)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(frame, text="Stop Server", command=stop_server)
stop_btn.grid(row=0, column=1, padx=5)

output = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled')
output.pack(padx=10, pady=10)

root.protocol("WM_DELETE_WINDOW", lambda: [stop_server(), root.destroy()])
root.mainloop()





