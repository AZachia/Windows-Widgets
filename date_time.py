from widget import Widget
import tkinter as tk
from datetime import datetime



class date_time(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(percent=20, time=10, *args, **kwargs)
        
        self.time = tk.StringVar()
        self.time.set(datetime.now().strftime("%H:%M:%S"))
        self.time_label = tk.Label(self, textvariable=self.time, font=("Helvetica", 48))
        self.time_label.pack(expand=True, fill="both", padx=25, pady=(25, 0))
        self.time_label.bind("<Button-1>", self.get_pos)
        
        self.date = tk.StringVar()
        self.date.set(datetime.now().strftime("%A %d %B %Y").title())
        self.date_label = tk.Label(self, textvariable=self.date, font=("Helvetica", 24))
        self.date_label.pack(expand=True, fill="both", padx=25, pady=(0, 25))
        self.date_label.bind("<Button-1>", self.get_pos)
        
        self.update_time()
        
    def update_time(self):
        self.time.set(datetime.now().strftime("%H:%M:%S"))
        self.app.after(1000, self.update_time)
        

if __name__ == "__main__":
    date_time().app.mainloop()
