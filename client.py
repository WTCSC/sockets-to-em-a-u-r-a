import socket

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server (replace with the server machine’s IP if needed)
client.connect(("localhost", 5001))
print("Connected to server")

# Send messages and receive responses
while True:
    msg = input("Guess the word: ")
    if not msg:
        break
    client.send(msg.encode())
    response = client.recv(1024).decode()
    print(f"Server says: {response}")

client.close()