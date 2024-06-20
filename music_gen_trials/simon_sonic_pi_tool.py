import os
import socket
import subprocess
import sys
import threading
import time
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer

log_directory = os.path.expanduser(r"C:\Tools")
os.makedirs(log_directory, exist_ok=True)
SERVER_OUTPUT = os.path.join(log_directory, "server-output.log")
SERVER_ERRORS = os.path.join(log_directory, "server-errors.log")

class Logger:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def __call__(self, message, high=False):
        if high or self.verbose:
            print(message)

class Installation:
    default_paths = [
        r'C:\Program Files\Sonic Pi\app'
    ]

    # can't set those parameters for windows as I don't no to which one they correspond
    def __init__(self, path, logger):
        self.base = os.path.expanduser(path)
        self.log = logger
        
        # old for unix..
        # self.server_path = os.path.join(self.base, 'server/bin/sonic-pi-server.rb')
        # self.ruby_path = os.path.join(self.base, 'server/native/ruby/bin/ruby')
        
        # new for windows, doesnt work
        self.server_path = r'C:\Program Files\Sonic Pi\app\server\ruby\vendor\activesupport-7.0.6\lib\active_support\testing\parallelization\server.rb'
        self.ruby_path = r'C:\Program Files\Sonic Pi\app\server\native\ruby\bin\ruby.exe'
        
        print(self.server_path)
        

    def exists(self):
        return os.path.isfile(self.ruby_path) and os.path.isfile(self.server_path)

    @staticmethod
    def find_installation(verbose=False):
        logger = Logger(verbose)
        for path in Installation.default_paths:
            inst = Installation(path, logger)
            if inst.exists():
                logger(f"Found installation at: {inst.base}", True)
                return inst
        logger("Sonic Pi server executable not found :(", True)
        return None

    def run_server(self, background=True):
        args = [self.ruby_path, '-E', 'utf-8', self.server_path]
        stdout = open(SERVER_OUTPUT, 'w')
        stderr = open(SERVER_ERRORS, 'w')
        process = subprocess.Popen(args, stdout=stdout, stderr=stderr)
        if not background:
            return process.wait()
        return process

def send_osc_message(host, port, path, args):
    client = OSCClient(host, port, encoding='utf8')
    client.send_message(path, args)
    print(f"OSC message sent to {host}:{port}: {path} {args}")

def check_server_running(cmd_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('127.0.0.1', cmd_port))
            return False  # If binding succeeded, port is not in use
    except OSError:
        return True # Port is in use, possibly by the server

def stop_all_jobs(host, cmd_port):
    send_osc_message(host, cmd_port, '/stop_all_jobs', [])

def record_audio(host, cmd_port, path):
    send_osc_message(host, cmd_port, '/start-recording', [])
    print("Recording started. Press Enter to stop...")
    input()
    send_osc_message(host, cmd_port, '/stop-recording', [])
    send_osc_message(host, cmd_port, '/save-recording', [path])
    print(f"Recording saved to {path}")

def run_code(host, cmd_port, code):
    send_osc_message(host, cmd_port, '/run-code', [code])
    
def exec_code(host, cmd_port, code):
    send_osc_message(host, cmd_port, '/execute_code', [code])

def main():
    host = '127.0.0.1'
    cmd_port = 4560
    file_path = r"current_sonic_pi_code.txt"
    with open(file_path, 'r') as file:
        sonic_pi_code = file.read()
        
    
    installation = Installation.find_installation(verbose=True)
    if installation:
        process = installation.run_server(background=False)
        if process == 0:
            print("Server started successfully.")
            
            print(check_server_running(cmd_port))
            exec_code(host, cmd_port, sonic_pi_code)
        else:
            print("Failed to start server.")

if __name__ == '__main__':
    main()
