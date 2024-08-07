import os
import ctypes
import getpass
import socket
import subprocess

class System():
    def get_home(self):
        return os.path.expanduser("~")
    
    def get_username(self):
        return getpass.getuser()

    def get_hostname(self):
        return socket.gethostname()

    def is_admin(self):
        try:
            admin = os.getuid() == 0
        except AttributeError:
            admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return admin
    
    def run(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.stdout.read().decode("utf-8")
    
    def run_cd(self, path):
        os.chdir(path)
        return os.getcwd()
