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



