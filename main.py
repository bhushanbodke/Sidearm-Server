import threading
import asyncio
from Connection import Connection
from GUI import ServerUI

class App:
    def __init__(self):
        self.GUI = ServerUI(self)
        self.Connection = Connection(self)
        self.server_thread = None

    def server_thread_func(self):
        # This runs in a separate thread
        self.loop = asyncio.new_event_loop()  # create a new loop for this thread
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.Connection.start_server())

    def start_server(self):
        self.server_thread = threading.Thread(target=self.server_thread_func, daemon=True)
        self.server_thread.start()

    def stop_server(self):
        # Schedule stop on the server thread's loop
        if self.Connection.server and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.Connection.stop_server(), self.loop)
            self.server_thread.join()

    def shutdown_app(self):
        print("Shutting down...")
        self.stop_server()
        self.GUI.root.destroy()

    def run(self):
        self.start_server()
        self.GUI.run()

if __name__ == "__main__":
    app = App()
    app.run()