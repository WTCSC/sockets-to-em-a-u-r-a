import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("localhost", 5001))
    print("Connected to server")
except ConnectionRefusedError:
    print("Error: Could not connect to server. Is it running?")
    exit(1)
except socket.timeout:
    print("Error: Connection attempt timed out.")
    exit(1)

try:
    guess_count = 0  # Track number of guesses

    while True:
        msg = input("Guess the word: ")
        if not msg:
            break

        guess_count += 1

        try:
            client.send(msg.encode())
        except BrokenPipeError:
            print("Error: Lost connection while sending.")
            break

        try:
            response = client.recv(1024).decode()
            if not response:
                print("Server disconnected.")
                break
            print(f"Server says: {response}")

            # Every 3 guesses, request a hint
            if guess_count % 3 == 0:
                print("You've made 3 guesses! Requesting a hint...")
                client.send("HINT".encode())
                hint = client.recv(1024).decode()
                print(f"Hint: {hint}")

            # Reset count if they got it right
            if "correct" in response.lower():
                guess_count = 0

        except ConnectionResetError:
            print("Error: Server forcibly closed the connection.")
            break

except KeyboardInterrupt:
    print("\nDisconnecting from server...")

finally:
    client.close()
    print("Connection closed.")