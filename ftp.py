from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import utils
from log import Log_queue
import datetime


class Ftp:
    def __init__(self,app):
        self.App = app ;
        self.authorizer = DummyAuthorizer();

        self.authorizer.add_user(utils.ftp.get("name"),utils.ftp.get("pass"),"./FtpShared",perm="elradfmwMT")

        self.handler = FTPHandler;
        self.handler.authorizer = self.authorizer

        # Define the server host and port
        # '' means listen on all available interfaces (LAN)
        self.SERVER_HOST = '0.0.0.0'
        self.SERVER_PORT = 2121
        self.server = None

    def stop_ftp(self):
        if self.server:
            Log_queue.put(f"| [{datetime.datetime.now()}] Stopped the ftp server")   
            self.server.close_all()

    def run_ftp(self):
        self.server = FTPServer((self.SERVER_HOST,self.SERVER_PORT),self.handler);
        Log_queue.put(f"| [{datetime.datetime.now()}] Started the ftp server")    
        self.server.serve_forever();