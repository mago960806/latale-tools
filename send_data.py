import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 64644

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(10)
client.connect((SERVER_IP, SERVER_PORT))

data = "29 00 01 00 C0 AB 8D 6A 00 00 00 00 66 00 00 00 00 00 67 5A 45 5F 41 56 5B 16 A1 00 00 60 00 64 5E 77 02 1A 73 18 01 09 0F"

encoded_data = bytes.fromhex(data)
print(encoded_data)
while True:
    try:
        client.send(encoded_data)
        time.sleep(1)
        response = client.recv(1024)
        if not response:
            break
        print(response)
    except KeyboardInterrupt:
        pass
client.close()
