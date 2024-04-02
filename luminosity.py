from widget import Widget
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

import screen_brightness_control as sbc



class luminosity(Widget):
    def __init__(self, *args, **kwargs):
        
        super().__init__(percent=100, time=10, *args, **kwargs)
        self.app.geometry("460x115")
        
        self.label = tk.Label(master=self, text=self.get_lum(), width=5, font=("@Microsoft YaHei UI", 15))
        self.label.grid(row=0, column=0, padx=(10, 0), pady=35)
        self.label.bind("<Button-1>", self.get_pos)
        
        self.scale = ttk.Scale(master=self, from_=0, to=100, orient=tk.HORIZONTAL, value=self.get_lum(), length=300)
        self.scale.grid(row=0, column=1, padx=(10, 40), pady=45, sticky="news")
        
        self.scale_clicked = False
        self.scale.bind("<Button-1>", self.on_scale_click)
        self.scale.bind("<ButtonRelease-1>", self.on_scale_release)
        
        self.luminosity_loop()

        
    def get_lum(self):
        return sbc.get_brightness()[0]
    
    def set_lum(self, event = None, level: int = 0):
        sbc.set_brightness(level)

        
    def luminosity_loop(self):
        if self.scale_clicked:
            current_lum = int(self.scale.get())
            self.set_lum(level=current_lum)
            self.label["text"] = current_lum
        else:
            current_lum = int(self.get_lum())
            self.scale.set(current_lum)
            self.label["text"] = current_lum
        self.app.after(100, self.luminosity_loop)

        
    def on_scale_click(self, event):
        self.scale_clicked = True
        x = event.x
        self.scale.set(int(x / self.scale.winfo_width() * 100))
        
    def on_scale_release(self, event):
        self.scale_clicked = False
        
        
if __name__ == "__main__":
    luminosity().app.mainloop()