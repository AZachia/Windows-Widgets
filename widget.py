from turtle import st

from ttkbootstrap import style
from TkTrans import TransparentWindow
import ttkbootstrap as ttk
from  ttkbootstrap import Style
import json


class Widget(TransparentWindow):
    def __init__(self, jsondata: dict = {}, root=ttk.Window(), percent=50, theme="dark", *args, **kwargs):
        if theme == "dark":
            self.bkg = (34, 34, 34)
            self.app = Style(theme='darkly').master
        elif theme == 'light':
            self.bkg = 'white'
        else:
            self.bkg = theme
        
        self.style = style
        super().__init__(root, percent=percent, bg=self.bkg, *args, **kwargs)
        self.app = self.root
        self.app.overrideredirect(True)

        self.bind('<Button-1>', self.get_pos)
        
        self.configfile = "widgetconfig"
        
        self.widgetname = type(self).__name__
        self.jsondata = jsondata
        
        self.data = self.open_config()
        self.xwin = self.data["xwin"]
        self.ywin = self.data["ywin"]
        
        
        self.app.geometry(f'+{self.xwin}+{self.ywin}')
        
        self.app.bind("<Alt-F4>", self.exit)
        
    
    def open_config(self):
        try:
            with open(self.configfile+'.json', 'r') as f:
                data = json.load(f)
            if data is None:
                raise FileNotFoundError
        except FileNotFoundError:
            data = {self.widgetname: {
            "xwin":0,
            "ywin":0}
        }
            with open(self.configfile+'.json', 'w') as f:
                json.dump(data, f)
        
        if not self.widgetname in data:
            
            data[self.widgetname] = {"xwin": 0, "ywin": 0}

            with open(self.configfile+'.json', 'w') as f:
                json.dump(data, f)
        
        return data[self.widgetname]
    
    
    
    def update_config_file(self):
        with open(self.configfile+'.json', 'r') as f:
            content = json.load(f)

        with open(self.configfile+'.json', 'w') as f:
            content[self.widgetname] = self.data
            json.dump(content, f)
    
    def update_position(self, newx: int, newy: int):
        self.data["xwin"] = newx
        self.data["ywin"] = newy
        self.update_config_file()

        
        
    def get_pos(self, event):

        xwin = self.app.winfo_x()
        ywin = self.app.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event):
            self.app.config(cursor="fleur")
            new_x = event.x_root + xwin
            new_y = event.y_root + ywin
            self.app.geometry(f'+{new_x}+{new_y}')
            self.update_position(new_x, new_y)

        def release_window(event):
            self.app.config(cursor="arrow")
            
        event.widget.bind('<B1-Motion>', move_window)
        event.widget.bind('<ButtonRelease-1>', release_window)
        
    def exit(self, *args, **kwargs):
        self.app.destroy()
        exit()
        
        
if __name__ == "__main__":
    
    class Test1(Widget):
        def __init__(self, *args, **kwargs):
            super().__init__( *args, **kwargs)
            self.close = ttk.Button(self, text="X", command=exit)
            self.close.pack(padx=20, pady=20)
            
            
    Test1().mainloop()