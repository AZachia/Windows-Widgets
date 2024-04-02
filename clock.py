from widget import Widget
import tkinter as tk
from datetime import datetime



class clock(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(percent=20, time=10, *args, **kwargs)
        self.time = tk.StringVar()
        self.time.set(datetime.now().strftime("%H:%M:%S"))
        self.label = tk.Label(self, textvariable=self.time, font=("Helvetica", 48))
        self.label.pack(expand=True, fill="both", padx=25, pady=25)
        self.label.bind("<Button-1>", self.get_pos)
        
        self.update_time()
        
    def update_time(self):
        self.time.set(datetime.now().strftime("%H:%M:%S"))
        self.app.after(1000, self.update_time)
        

if __name__ == "__main__":
    clock().app.mainloop()