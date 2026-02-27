import socket



# Create a socket object (IPv4 + TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to 0.0.0.0:5000
server.bind(("0.0.0.0", 5001))

# Listen for connections
server.listen(1)
print("Waiting for connection...")

# Accept client connection
client, addr = server.accept()
print(f"Connected to {addr}")

word = input("What is the word they have to guess?: ")

# Receive and echo messages
while True:
    msg = client.recv(1024).decode()
    if msg != word:
        print(f"Received: {msg}")
        client.send(f"Guess is wrong, try again".encode())
    if msg == word:
        print(f"Received: {msg}")
        client.send(f"You have guessed the word".encode())
        word = input("Client has guessed the last word, please pick a new word: ")
    if not msg:
        break

client.close()
server.close()