# gui.py
import tkinter as tk
from tkinter import scrolledtext
from log import Log_queue
import utils
import discovery
import asyncio


class ServerUI:
    def __init__(self,app):
        self.root = tk.Tk()
        self.root.title("Android PC Control Server")
        self.root.geometry("800x600")
        self.root.overrideredirect(False)

        self.phones_name = "Phone"
        self.App = app;
        
        self.root.bind('<Key>',self.Events)        
        self.statusLable = tk.Label(font=("Arial", 12, "bold"),text="Connection Status : ")
        self.status = tk.Label(font=("Arial", 12, "bold"),text= f"{f"Connected to {self.phones_name}" if utils.is_connected else "Disconnected"}" 
                               ,foreground=f"{"green" if utils.is_connected else "red"}")
        self.statusLable.pack();
        self.status.pack();
        
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(log_frame, text="Logs:", font=("Arial", 11, "bold")).pack(anchor="w")

        self.log_area = scrolledtext.ScrolledText(log_frame, width=70, height=12)
        self.log_area.pack(fill="both", expand=True)


        
    def monitor_clip(self):
        try:
            current_content = self.root.clipboard_get()
            if (current_content):
                if current_content != utils.old_clip:
                    utils.old_clip = current_content
                    asyncio.run_coroutine_threadsafe(
                        self.App.Connection.websocket.send(utils.old_clip),
                        self.App.loop)
        except:
            print("NOTHING in clipboard")

        self.root.after(1000, self.monitor_clip)
        
    def update(self):   
        if not utils.is_connected:
            #broadcast the websocket port and ip to enable discovery
            discovery.send_udp(); 
        else:
            self.monitor_clip()

        self.status.config(font=("Arial", 12, "bold")
                           ,text= f"{f"Connected to {self.phones_name}" if utils.is_connected else "Disconnected"}" 
                               ,foreground=f"{"green" if utils.is_connected else "red"}")
        
        while not Log_queue.empty():
            msg = Log_queue.get()
            self.log_area.insert("end", msg + "\n")
            self.log_area.see("end")
        self.root.after(1000,self.update)       
    
    def Events(self,event):pass
    
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.App.shutdown_app);
        self.root.after(1000,self.update)
        self.root.mainloop()
        

