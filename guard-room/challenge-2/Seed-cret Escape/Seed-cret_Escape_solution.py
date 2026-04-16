import random
import re
import socket
import string
import time

HOST = "localhost"
PORT = 1337
WINDOW = 3
TIMEOUT = 2.0

CHARACTERS = string.ascii_lowercase + string.digits
PREFIX_PATTERN = re.compile(r"The password is:\s*([a-z0-9]{5})\.{4,}", re.IGNORECASE)


def generate_password(seed):
    random.seed(seed)
    return ''.join(random.choice(CHARACTERS) for _ in range(15))


def parse_prefix(server_text):
    match = PREFIX_PATTERN.search(server_text)
    if match:
        return match.group(1)
    return None


def find_best_candidate(base_seed, window, prefix):
    # Test connection-time seed first, then nearby seeds.
    offsets = [0]
    for i in range(1, window + 1):
        offsets.extend((-i, i))

    for offset in offsets:
        seed = base_seed + offset
        candidate = generate_password(seed)
        if candidate.startswith(prefix):
            return seed, candidate

    return None


def recv_all_available(sock):
    chunks = []
    while True:
        try:
            part = sock.recv(4096)
            if not part:
                break
            chunks.append(part)
        except socket.timeout:
            break
    return b"".join(chunks).decode(errors="replace")


def main():
    try:
        with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as sock:
            connection_seed = int(time.time())
            sock.settimeout(TIMEOUT)

            # Read everything the server sends first, then parse and brute-force.
            server_text = recv_all_available(sock)

            print("Server output:")
            if server_text.strip():
                print(server_text.rstrip())
            else:
                print("(no initial server output received)")

            prefix = parse_prefix(server_text)
            if not prefix:
                print("Prefix not found in expected format 'The password is: xxxxx....'. Exiting.")
                return

            best_match = find_best_candidate(connection_seed, WINDOW, prefix)

            print(f"Connection-time Unix seed: {connection_seed}")
            print(f"Scanning seeds from {connection_seed - WINDOW} to {connection_seed + WINDOW}")
            print(f"Filtering for prefix: {prefix}")

            if not best_match:
                print("No candidates matched.")
                return

            best_seed, best_candidate = best_match
            print(f"Submitting best candidate from seed {best_seed}: {best_candidate}")
            sock.sendall((best_candidate + "\n").encode())

            reply = recv_all_available(sock)
            print("Server response:")
            if reply.strip():
                print(reply.rstrip())
            else:
                print("(no response received before timeout/close)")
    except OSError as exc:
        print(f"Connection/IO failed: {exc}")


if __name__ == "__main__":
    main()