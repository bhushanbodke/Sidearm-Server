import threading
import asyncio
from Connection import Connection
from GUI import ServerUI
from ftp import Ftp
class App:
    def __init__(self):
        self.GUI = ServerUI(self)
        self.Connection = Connection(self)
        self.Ftp_connection =Ftp(self); 
        self.server_thread = None

    def server_thread_func(self):
        # This runs in a separate thread
        self.ws_loop = asyncio.new_event_loop()  # create a new loop for this thread
        asyncio.set_event_loop(self.ws_loop)
        self.ws_loop.run_until_complete(self.Connection.start_server())

    def start_server(self):
        self.server_thread = threading.Thread(target=self.server_thread_func, daemon=True)
        self.server_thread.start()
        #start ftp server 
        self.ftp_server_thread = threading.Thread(target=self.Ftp_connection.run_ftp,daemon=True)   
        self.ftp_server_thread.start();


    def stop_server(self):
        # Schedule stop on the server thread's loop
        if self.Connection.server and self.ws_loop.is_running():
            asyncio.run_coroutine_threadsafe(self.Connection.stop_server(), self.ws_loop)
            self.server_thread.join()
        if self.Ftp_connection.server:
            self.Ftp_connection.stop_ftp();
            self.ftp_server_thread.join();    
        

    def shutdown_app(self):
        print("Shutting down...")
        threading.Thread(target=self.stop_server, daemon=True).start()
        self.GUI.root.destroy()

    def run(self):
        self.start_server()
        self.GUI.run()

if __name__ == "__main__":
    app = App()
    app.run()