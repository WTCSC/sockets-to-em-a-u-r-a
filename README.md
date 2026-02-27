# Socket Word Guessing Game

A simple TCP socket-based word guessing game where a server picks a secret word and a client tries to guess it.

---

## How It Works

The **server** hosts the game. It picks a word and waits for the client to send guesses. The **client** connects and repeatedly submits guesses until they get it right.

---

## Potential Errors

### Server-Side

**`OSError: [Errno 98] Address already in use`**
Port 5001 is already occupied. This commonly happens if the server crashed without closing the socket properly. Fix by waiting a moment and retrying, or by adding `server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` before `bind()`.

**`ConnectionResetError` / `BrokenPipeError`**
The client disconnected unexpectedly mid-game. The `while True` loop has no `try/except` to handle this, so the server will crash instead of recovering gracefully.

**Logic bug — word not reset after correct guess**
When the client guesses correctly, `word` is updated via `input()`. However, the `if not msg: break` check comes *after* both `if msg != word` and `if msg == word`. If the client sends an empty message at any point, the server breaks without closing cleanly. Also, the two `if` checks are independent rather than `if/elif/else`, meaning a correct guess evaluates both branches unnecessarily.

**No timeout**
`server.accept()` blocks forever. If no client connects, the server hangs indefinitely.

---

### Client-Side

**`ConnectionRefusedError`**
The server isn't running or isn't reachable at `localhost:5001`. Start the server first.

**`TimeoutError` / `ConnectionResetError`**
The server closed the connection (e.g., due to a crash). The client has no error handling around `recv()` and will crash.

**Empty input sent to server**
If the user presses Enter without typing, an empty string is sent to the server. The client's `if not msg: break` check happens *before* sending, so this is handled on the client side — but the server's equivalent check comes *after* the send/receive loop, meaning the server may behave unexpectedly if it receives an empty string from another cause.

---

## Setup & Usage

### Requirements
- Python 3.x
- No external libraries needed

### Running the Game

**1. Start the server first:**
```bash
python3 server.py
```

**2. In a separate terminal, start the client:**
```bash
python3 client.py
```

**3. On the server**, enter the secret word when prompted.

**4. On the client**, type guesses and press Enter. The server will tell you if you're right or wrong.

---

## Recommended Fixes

```python
# Add before server.bind() to avoid "Address already in use" errors
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Wrap the recv loop in try/except for clean disconnection handling
try:
    msg = client.recv(1024).decode()
except (ConnectionResetError, BrokenPipeError):
    print("Client disconnected unexpectedly.")
    break

# Use if/elif/else instead of two independent if checks
if msg == word:
    ...
elif msg:
    ...
else:
    break
```

---

## File Structure

```
.
├── server.py   # Hosts the game, picks the word
├── client.py   # Connects and submits guesses
└── README.md
```