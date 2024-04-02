import random
import time
import tkinter as tk
from PIL import ImageGrab, Image, ImageTk, ImageDraw
import ttkbootstrap as ttk


def ShapeImage(color=(255, 255, 255), bg=(255, 255, 255), w=None, h=None, s=100, percent=None):
    new = Image.new('RGBA', (w, h), bg)
    draw = ImageDraw.Draw(new)

    if percent and percent <= 100 and percent >= 0:
        s = (percent / 100) * h / 2

    if s > h or s > w:
        s = w / 2 if h > w else h / 2

    if 2 * s < h:
        draw.rectangle([(0, 0 + s), (w, h - s)], fill=color)
    if 2 * s < w:
        draw.rectangle([(0 + s, 0), (w - s, h)], fill=color)

    draw.pieslice([(0, 0), (s + s, s + s)], start=180, end=270, fill=color)
    draw.pieslice([(w - 2 * s, 0), (w, s * 2)], start=270, end=360, fill=color)
    draw.pieslice([(0, h - 2 * s), (s * 2, h)], start=90, end=180, fill=color)
    draw.pieslice([(w - 2 * s, h - 2 * s), (w, h)], start=0, end=90, fill=color)
    return new


def center_crop(img, new_width=None, new_height=None, crop_methode="center"):
    if type(img) == str:
        img = Image.open(img)
    width, height = img.size
    if crop_methode == 'center':
        if width > height:
            left = (width - height) // 2
            upper = 0
            right = left + height
            bottom = height
            img = img.crop((left, upper, right, bottom))
        elif width < height:
            left = 0
            upper = (height - width) // 2
            right = width
            bottom = upper + width
            img = img.crop((left, upper, right, bottom))

    return img.resize((new_width, new_height))


class InvisibleCanvas:
    def __init__(self, root):
        self.root = root
        self.tk = root
        self.last_x, self.last_y, self.last_w, self.last_h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        self.cap()

    def cap(self):
        s = 500
        color = (255, 0, 0, 120)
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if (x != self.last_x) or (y != self.last_y) or (w != self.last_w) or (h != self.last_h):
            self.root.attributes("-alpha", 0)
            screenshot = ImageGrab.grab((x, y, x + w, y + h))
            self.root.attributes("-alpha", 1)
            screenshot = screenshot.convert('RGBA')

            # Convertir l'image PIL en PhotoImage Tkinter
            screenshot_tk = ImageTk.PhotoImage(
                Image.alpha_composite(screenshot, ShapeImage(color=color, w=w, h=h, s=s, bg=(0, 0, 0, 0))))

            # Effacer tout contenu précédent du canvas
            self.canvas.delete("all")

            # Afficher l'image sur le canvas
            self.canvas.create_image(0, 0, image=screenshot_tk, anchor="nw")

            # Conserver une référence à l'objet PhotoImage
            self.canvas.image = screenshot_tk

        self.last_x, self.last_y, self.last_w, self.last_h = x, y, w, h
        self.root.after(500, self.cap)



class RoundedWiget:
    def __init__(self, widget, bg='#7272ff', color="white", px=10000, percent=None, height=None, width=None):
        self.widget = widget
        widget.config(activebackground=color)
        self.root = widget.winfo_toplevel()
        self.px = px
        self.bkg = bg
        self.s = px
        self.percent = percent
        self.color = color
        self.root.after(1, self.create)
        self.widget.bind("<Visibility>", self.create)
        self.widget.bind("<Map>", self.create)
        self.widget.bind("<Configure>", self.create)

    def create(self, event=None):
        self.s = self.px
        self.widget.config(compound=tk.CENTER, borderwidth=0, relief=tk.FLAT)
        self.w = self.widget.winfo_width()
        self.h = self.widget.winfo_height()

        bg_img = ImageTk.PhotoImage(ShapeImage(w=self.w, h=self.h, color=self.bkg, bg=self.color, s=self.s, percent=self.percent))
        try:
            self.widget.config(image=bg_img)
            self.widget.image = bg_img
        except:
            self.widget.create_image(0, 0, image=bg_img, anchor="nw")
            self.widget.image = bg_img

    def pack(self, *args, **kwargs):
        self.widget.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.widget.grid(*args, **kwargs)

    def config(self, *args, **kwargs):
        self.widget.config(*args, **kwargs)


class TransparentWidget:
    def __init__(self, widget, bg='white', color="red", px=10000, percent=None, imbgcolor=None):
        self.widget = widget
        self.root = widget.winfo_toplevel()
        self.px = px
        self.bkg = bg
        self.color = color
        self.root.attributes('-transparentcolor', self.color)
        self.s = px
        self.percent = percent
        self.x = self.widget.winfo_x()
        self.y = self.widget.winfo_y()
        self.w = self.widget.winfo_width()
        self.h = self.widget.winfo_height()
        self.start = True
        if imbgcolor == None:
            self.imbgcolor = color
        else:
            self.imbgcolor = imbgcolor
        self.root.after(10, self.create)

    def create(self):
        self.s = self.px
        if self.start == True:
            self.x = self.widget.winfo_x()
            self.y = self.widget.winfo_y()
            self.w = self.widget.winfo_width()
            self.h = self.widget.winfo_height()
        self.start = False
        print(self.x, self.y, self.h, self.w)

        b = ShapeImage(w=self.w, h=self.h, color=self.bkg, bg=self.imbgcolor, s=self.s, percent=self.percent)

        screenshot_tk = ImageTk.PhotoImage(b)
        try:
            self.widget.config(image=screenshot_tk)
            self.widget.image = screenshot_tk
        except:
            self.widget.create_image(0, 0, image=screenshot_tk, anchor="nw")
            self.widget.image = screenshot_tk
            print("in")

        self.root.after(10, self.create)

"""
class TransparentWindow(tk.Canvas):
    def __init__(self, root=None, bg='white', color="red", size=10000, percent=None, time: int = 100, image=None,
                 bg_image=None):
        if root == None:
            root = tk.Tk()
        super().__init__(root)
        self.root = root
        self.time = time
        self.size = size
        self.bkg = bg
        self.percent = percent
        self.last_x, self.last_y, self.last_w, self.last_h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
        self.color = color
        if self.root.attributes('-transparentcolor'):
            self.color = self.root.attributes('-transparentcolor')
        self.root.attributes('-transparentcolor', self.color)
        self.s = size
        self.bg_image = bg_image
        self.last_image = self.bg_image

        self.pack(fill="both", expand=True)
        self.image = image
        self.root.after(10, self.create)

    def create(self):
        self.s = self.size
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        test = ShapeImage(w=w, h=h, color=self.bkg, bg=self.color, s=self.s, percent=self.percent)

        if self.bg_image:
            if self.bg_image != self.last_image:
                test3 = center_crop(self.bg_image, w, h)
                test = Image.alpha_composite(test3.convert('RGBA'), test.convert('RGBA'))
                self.last_image = self.bg_image
        screenshot_tk = ImageTk.PhotoImage(test)
        self.delete("all")
        self.create_image(0, 0, image=screenshot_tk, anchor="nw")
        self.image = screenshot_tk
        self.root.after(10, self.create)

    def mainloop(self):
        self.root.mainloop()

"""
class InvisibleCanvas2(tk.Canvas):
    def __init__(self, root, color=(255, 0, 0, 120), size=100, percent=None, time: int = 100):
        super().__init__(root)
        self.root = root
        self.percent = percent
        self.time = time
        self.last_x, self.last_y, self.last_w, self.last_h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
        self.color = color
        self.s = size
        self.pack(fill="both", expand=True)

        self.cap()

    def cap(self):
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if (x != self.last_x) or (y != self.last_y) or (w != self.last_w) or (h != self.last_h):
            self.root.attributes("-alpha", 0)
            screenshot = ImageGrab.grab((x, y, x + w, y + h))
            self.root.attributes("-alpha", 1)
            screenshot = screenshot.convert('RGBA')
            screenshot_tk = ImageTk.PhotoImage(Image.alpha_composite(screenshot,
                                                                     ShapeImage(w=w, h=h, percent=self.percent,
                                                                                color=self.color, bg=(0, 0, 0, 0),
                                                                                s=self.s)))
            self.delete("all")
            self.create_image(0, 0, image=screenshot_tk, anchor="nw")
            self.image = screenshot_tk

        self.last_x, self.last_y, self.last_w, self.last_h = x, y, w, h
        self.root.after(self.time, self.cap)






###-------------------------------------------------------------------------------------------------


class TransparentWindow(tk.Canvas):
    def __init__(self,
                 root=None,
                 bg='white',
                 color="lightblue",
                 size=10000,
                 percent=None,
                 time: int = 100,
                 image_path=None,
                 crop_methode='center',
                 border_raduis:list|tuple = None,
                 titlebar = False,
                 titlebar_color = 'lightgrey',
                 titlebar_height = 50):



        if root == None:
            root = tk.Tk()
        super().__init__(root)
        self.root = root
        self.time = time
        self.size = size
        self.bkg = bg
        self.percent = percent
        self.last_x, self.last_y, self.last_w, self.last_h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
        self.color = color
        if self.root.attributes('-transparentcolor'):
            self.color = self.root.attributes('-transparentcolor')
        self.root.attributes('-transparentcolor', self.color)
        self.s = size
        self.pack(fill="both", expand=True)
        self.image_path = image_path
        self.time = time
        self.crop_methode = crop_methode
        self.widgets = []
        if titlebar == True:

            def get_pos(event):  # this is executed when the title bar is clicked to move the window

                    xwin = root.winfo_x()
                    ywin = root.winfo_y()
                    startx = event.x_root
                    starty = event.y_root

                    ywin = ywin - starty
                    xwin = xwin - startx

                    def move_window(event):  # runs when window is dragged
                        root.config(cursor="fleur")
                        root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

                    def release_window(event):  # runs when window is released
                        root.config(cursor="arrow")

                    self.titlebar.bind('<B1-Motion>', move_window)
                    self.titlebar.bind('<ButtonRelease-1>', release_window)
                    title_bar_title.bind('<B1-Motion>', move_window)
                    title_bar_title.bind('<ButtonRelease-1>', release_window)


            self.titlebar = tk.Canvas(self, height=30)
            self.titlebar.pack(fill='both')
            self.titlebar_color = titlebar_color
            self.titlebar_height = titlebar_height

            self.titlebar.bind('<Button-1>', get_pos)


            if percent and percent <= 100 and percent >= 0:
                s = (percent / 100) * self.root.winfo_height() / 2

            close_button = tk.Button(self.titlebar, text='  ×  ', command=self.root.destroy, bg='#10121f', padx=2, pady=2,font=("calibri", 10), bd=0, fg='white', highlightthickness=0)
            expand_button = tk.Button(self.titlebar, text=' 🗖 ', bg='#10121f', padx=2, pady=2, bd=0, font=("calibri", 10), highlightthickness=0)
            minimize_button = tk.Button(self.titlebar, text=' - ', bg='#10121f', padx=2, pady=2, bd=0, font=("calibri", 10), highlightthickness=0)
            title_bar_title = tk.Label(self.titlebar, text="Mon appli", bg=self.titlebar_color, bd=0, font=("helvetica", 10),highlightthickness=0)

            close_button["bg"] = self.titlebar_color
            expand_button["bg"] = self.titlebar_color
            minimize_button["bg"] = self.titlebar_color
            title_bar_title["bg"] = self.titlebar_color


            close_button["fg"] = "black"
            expand_button["fg"] = "black"
            minimize_button["fg"] = "black"
            title_bar_title["fg"] = "black"

            close_button.pack(side="right", ipadx=7, ipady=0, padx=(0, int(s)))
            expand_button.pack(side="right", ipadx=7, ipady=0)
            minimize_button.pack(side="right", ipadx=7, ipady=0)
            title_bar_title.pack(side="left", padx=30)


        else: self.titlebar = None


        self.root.after(10, self.create)
        self.bind("<Visibility>", self.create)
        self.bind("<Map>", self.create)
        self.bind("<Configure>", self.create)

    def create(self, event=None):
        self.s = self.size
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        back = ShapeImage(w=w, h=h, color=self.bkg, bg=self.color, s=self.s, percent=self.percent)

        if self.titlebar != None:

            title_img = ShapeImage(w=w, h=h, color=self.titlebar_color, bg=self.color, s=self.s, percent=self.percent)
            largeur, _ = title_img.size
            title_img = title_img.crop((0, 0, largeur, self.titlebar_height))
            #title_img = title_img.resize((30, self.titlebar.winfo_width()))
            title_img = ImageTk.PhotoImage(title_img)
            self.titlebar.delete("all")
            self.titlebar.create_image(0, 0, image=title_img, anchor="nw")
            self.titlebar.image = title_img


        if self.image_path:
            back = Image.alpha_composite(center_crop(self.image_path, w, h, crop_methode=self.crop_methode).convert('RGBA'), back.convert('RGBA'))
            back.show()
            exit()

        screenshot_tk = ImageTk.PhotoImage(back)
        self.delete("all")
        self.create_image(0, 0, image=screenshot_tk, anchor="nw")
        self.image = screenshot_tk

    def mainloop(self):
        self.root.mainloop()
        
    def change_image(self, image_path):
        self.image_path = image_path
        self.create()



###-------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    a = TransparentWindow(root=ttk.Window(), percent=20, titlebar=True)
    a.root.overrideredirect(True)

    button = RoundedWiget(tk.Button(a, width=230, height=35), bg="red")
    button.config(text="Clique ici")
    button.pack(pady=20, padx=30)

    def clic():
        button.bkg = random.choice(("yellow", "red", "green", 'orange'))
        button.create()

    button = RoundedWiget(tk.Button(a, width=230, height=35, command=clic))
    button.config(text="Clique ici")
    button.pack(pady=20, padx=30)

    a.mainloop()
