from widget import Widget
import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from TkTrans import RoundedWiget

import os
import random


class image(Widget):

    def __init__(self, *args, **kwargs):
        super().__init__(percent=50, time=10, *args, **kwargs)
        
        self.app.geometry("380x380")
        self.image_path = "D:/perso/MJ/Vympel_A_stormtrooper_as_a_Viking_Snowy_Forest_background_Photo_5df4efa0-9878-413d-be7c-4411149cc16f.png"
        
        if not "image_path" in self.data or not os.path.exists(self.data["image_path"]) or len([i for i in os.listdir(self.data["image_path"]) if i.split(".")[-1].lower() in ["jpg", "png", "jpeg", "gif"]]) == 0:
            self.chose_file_button = RoundedWiget(tk.Button(master=self, text="Chose a folder", width=230, height=35, font=(None, 12), compound=tk.CENTER, command=self.__chose_folder), "#363636", "#222222")
            self.chose_file_button.pack(pady = 170)
        
        else:
            self.load_image()
            
    def __chose_folder(self):
        folder = fd.askdirectory()
        if folder:
            if len([i for i in os.listdir(folder) if i.split(".")[-1].lower() in ["jpg", "png", "jpeg", "gif"]]) > 0:
                self.data["image_path"] = folder
                self.chose_file_button.widget.destroy()
                self.update_config_file()
                self.load_image()
    
    def load_image(self):
        self.images = [f"{self.data['image_path']}/{i}" for i in os.listdir(self.data["image_path"]) if i.split(".")[-1].lower() in ["jpg", "png", "jpeg", "gif"]]
        self.change_image(random.choice(self.images))
        
        
        print(self.image_path)
        
        self.create()
        self.update()
        self.app.after(5800, self.load_image)

        
if __name__ == "__main__":
    test = image()
    test.app.mainloop()