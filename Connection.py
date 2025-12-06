import asyncio
from log import Log_queue
import datetime
import utils
import websockets
import discovery 

class Connection:
    def __init__(self,app):
        self.server = None
        self.App = app
    
    def setclipboard(self,msg):
        self.App.GUI.root.clipboard_append(msg)
        self.App.GUI.root.update()
        print("set the clipboard")

    
    async def echo(self,websocket):
        if not utils.is_connected:
            utils.is_connected = True;
            Log_queue.put(f"| [{datetime.datetime.now()}] Device connected...")
            async for message in websocket:
                Log_queue.put(f"| [{datetime.datetime.now()}] Message [\"{message}\"]")
                message = message.split(",")
                if message[0] =="Clip":
                    self.setclipboard(message[1])


        else: 
            await websocket.send("already another device connected")
            websocket.close(4000,reason="already another device connected")     
            return

    async def stop_server(self):
        if self.server:
            self.server.close()  # Initiate server shutdown
            await self.server.wait_closed() # Wait for server to fully close
            print("Server closed.")
            return True
        return False
    
    
    async def start_server(self):
        Log_queue.put(f"| [{datetime.datetime.now()}] Server started...")
        self.server = await websockets.serve(self.echo, utils.ip_address, utils.PORT)
        await self.server.wait_closed()
    