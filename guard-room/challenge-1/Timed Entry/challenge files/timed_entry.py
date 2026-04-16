import socketserver
import os
import time
from pathlib import Path

HOST = "0.0.0.0"
PORT = 1227
CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}_!@#$%^&*()-=+[]"

# grab the password from txt file
# Grab secrets relative to this script so startup does not depend on cwd.
BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "timed_entry_password.txt", "r", encoding="utf-8") as f:
    SECRET_PASSWORD = f.read().strip()

# grab the flag from txt file
with open(BASE_DIR / "timed_entry_flag.txt", "r", encoding="utf-8") as f:
    FLAG = f.read().strip()

def vulnerable_compare(input_str, secret_str):
    for index, secret_char in enumerate(secret_str):
        if index >= len(input_str):
            return False
        if input_str[index] != secret_char:
            return False
        time.sleep(0.05)
    return len(input_str) == len(secret_str)


class ChallengeHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            self.wfile.write(b"Welcome to the vault.\n")
            
            while True:
                self.wfile.write(b"Password: ")
                self.wfile.flush()

                supplied = self.rfile.readline(1024)
                if not supplied:
                    return

                password = supplied.decode(errors="replace").strip()
                if vulnerable_compare(password, SECRET_PASSWORD):
                    self.wfile.write((FLAG + "\n").encode())
                    self.wfile.flush()
                    return
                else:
                    self.wfile.write(b"Access Denied\n")
                    self.wfile.flush()
        except BrokenPipeError:
            return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    with ThreadedTCPServer((HOST, PORT), ChallengeHandler) as server:
        print(f"Listening on {HOST}:{PORT}")
        server.serve_forever()


if __name__ == "__main__":
    main()
