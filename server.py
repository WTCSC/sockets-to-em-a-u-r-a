import socket
import random

# Load from Linux built-in dictionary
with open("/usr/share/dict/words") as f:
    WORDS = [word.strip().lower() for word in f if word.strip().isalpha()]  



def get_hint(word, hints_given):
    hints = [
        f"The word has {len(word)} letters.",
        f"The word starts with '{word[0]}'.",
        f"The word ends with '{word[-1]}'.",
        f"The word contains the letter '{random.choice(word)}'.",
    ]
    return hints[hints_given % len(hints)]

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Avoid "address in use" errors
server.bind(("localhost", 5001))
server.listen(1)
print("Server is listening on port 5001...")

try:
    conn, addr = server.accept()
    print(f"Client connected from {addr}")

    secret_word = random.choice(WORDS)  # Pick a random word
    print(f"Secret word is: {secret_word}")  # Only visible server-side
    hints_given = 0

    while True:
        try:
            guess = conn.recv(1024).decode()
            if not guess:
                print("Client disconnected.")
                break

            if guess == "HINT":
                hint = get_hint(secret_word, hints_given)
                hints_given += 1
                conn.send(hint.encode())
                continue

            if guess.lower() == secret_word.lower():
                conn.send("Correct! Well done!".encode())
                hints_given = 0  # Reset for new round
                secret_word = random.choice(WORDS)  # Pick a new word
                print(f"New secret word is: {secret_word}")
            else:
                conn.send("Wrong, try again!".encode())

        except ConnectionResetError:
            print("Client forcibly disconnected.")
            break

except KeyboardInterrupt:
    print("\nShutting down server...")

finally:
    conn.close()
    server.close()
    print("Server closed.")