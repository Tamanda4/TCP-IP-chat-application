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


