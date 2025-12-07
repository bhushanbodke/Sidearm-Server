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
        self.websocket = None
    

    
    async def echo(self,websocket):
        # if already a device is not connected then accept the connection otherwise reject it 
        if not utils.is_connected:
            utils.is_connected = True;
            Log_queue.put(f"| [{datetime.datetime.now()}] Device connected...")
            self.websocket = websocket;
            try:
                async for message in websocket:
                    Log_queue.put(f"| [{datetime.datetime.now()}] Message [\"{message}\"]")
            except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError) as e:
            # Client intentionally closed or disappeared
                Log_queue.put(f"| [{datetime.datetime.now()}] Client disconnected: {e}")
            finally:
                utils.is_connected = False
                Log_queue.put(f"| [{datetime.datetime.now()}] Device connection closed")
                        
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
    