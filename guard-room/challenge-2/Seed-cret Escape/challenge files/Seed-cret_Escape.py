import socket
import random
import threading
import time
import string

MAX_CONCURRENT_CLIENTS = 10

# grab flag from seed-cret_flag.txt and store it in a variable
with open('seed-cret_flag.txt', 'r') as f:
    FLAG = f.read().strip()

def generate_password():
    """Generate a 15-character password using time-based seed."""
    # remember Bob, choose a more secure method for real applications
    # random.seed() + random.choice() is not secure, and we don't want anyone breaking into our vault!

    random.seed(int(time.time()))
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(15))

def handle_client(conn, addr):
    """Handle a single client connection."""
    try:
        conn.sendall(b"Welcome to the Vault.\n")
        conn.sendall(b"I bet you can't guess this password even if I give you the first 5 characters!\n")

        while True:
            password = generate_password()
            hint = f"""The password is: {password[:5]}..........\nYour guess: """
            conn.sendall(hint.encode())
            
            data = conn.recv(1024)
            if not data:
                break
            user_input = data.decode().strip()
            
            if user_input == password:
                conn.sendall(FLAG.encode() + b"\n")
                break
            else:
                conn.sendall(b"Access Denied. Try again...\n")
                time.sleep(1)
    
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    
    finally:
        conn.close()


def client_worker(conn, addr, limiter):
    """Run a single client session and release a slot when complete."""
    try:
        handle_client(conn, addr)
    finally:
        limiter.release()

def main():
    """Start the CTF server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 1337))
    server.listen(5)
    limiter = threading.BoundedSemaphore(MAX_CONCURRENT_CLIENTS)
    print(f"Server listening on port 1337 (max {MAX_CONCURRENT_CLIENTS} concurrent clients)...")
    
    try:
        while True:
            conn, addr = server.accept()
            if not limiter.acquire(blocking=False):
                conn.sendall(b"Server busy. Try again in a moment.\n")
                conn.close()
                continue

            print(f"Connection from {addr}")
            thread = threading.Thread(
                target=client_worker,
                args=(conn, addr, limiter),
                daemon=True,
            )
            thread.start()
    
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    
    finally:
        server.close()

if __name__ == "__main__":
    main()