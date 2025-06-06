import socket
import os

CHUNK_SIZE = 1024

def send_file(filename, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the filename first
    base_name = os.path.basename(filename)
    sock.sendto(base_name.encode(), (ip, port))

    # Then send the file contents
    with open(filename, 'rb') as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            sock.sendto(data, (ip, port))

    # Send end marker
    sock.sendto(b'__END__', (ip, port))
    sock.close()
