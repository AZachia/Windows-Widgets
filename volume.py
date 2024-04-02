from widget import Widget
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



class volume(Widget):
    """A simple volume widget that allows you to change the volume of the system."""
    def __init__(self, *args, **kwargs):
        
        self.volume = volume = cast(AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume))
        
        super().__init__(percent=100, time=10, *args, **kwargs)
        
        self.app = Style(theme='darkly').master
        self.app.geometry("460x115")
        
        self.label = tk.Label(master=self, text=self.get_volume(), width=5, font=("@Microsoft YaHei UI", 15))
        self.label.grid(row=0, column=0, padx=(10, 0), pady=35)
        self.label.bind("<Button-1>", self.get_pos)
        
        self.scale = ttk.Scale(master=self, from_=0, to=100, orient=tk.HORIZONTAL, value=self.get_volume(), length=300)
        self.scale.grid(row=0, column=1, padx=(10, 40), pady=45, sticky="news")
        
        self.scale_clicked = False
        self.scale.bind("<Button-1>", self.on_scale_click)
        self.scale.bind("<ButtonRelease-1>", self.on_scale_release)
        
        self.volume_loop()

        
    def get_volume(self):
        return round(self.volume.GetMasterVolumeLevelScalar() * 100)
    
    def set_volume(self, event = None, volume: int = 0):
        if event is not None:
            volume = self.scale.get()
        self.volume.SetMasterVolumeLevelScalar(volume / 100, None)

        
    def volume_loop(self):
        if self.scale_clicked:
            current_volume = int(self.scale.get())
            self.set_volume(volume=current_volume)
            self.label["text"] = current_volume if current_volume != 0 else "╳"
        else:
            current_volume = int(self.get_volume())
            self.scale.set(current_volume)
            self.label["text"] = current_volume if current_volume != 0 else "╳"
        self.app.after(100, self.volume_loop)

        
    def on_scale_click(self, event):
        self.scale_clicked = True
        x = event.x
        self.scale.set(int(x / self.scale.winfo_width() * 100))
        
    def on_scale_release(self, event):
        self.scale_clicked = False
        
        
if __name__ == "__main__":
    volume().app.mainloop()