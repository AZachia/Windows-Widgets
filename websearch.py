from widget import Widget
import tkinter as tk
import webbrowser
from PIL import Image, ImageTk
from urllib.parse import quote



class websearch(Widget):
    """A simple web search widget that opens a new tab in the default browser with the search query."""
    def __init__(self, *args, **kwargs):
        super().__init__(percent=100, theme="light", time=10, *args, **kwargs)
        
        image = Image.open("logo.png")
        image = image.resize((50, 50))
        image = ImageTk.PhotoImage(image)
        
        self.img = tk.Label(master=self, image=image, width=50, height=50)
        self.img["image"] = image
        self.img.image = image
        self.img.grid(row=0, column=0, padx=(20, 0))

        self.text = tk.Entry(self, width=30, borderwidth=0, highlightcolor=None, font=(None, 20))
        self.text["highlightthickness"] = 0
        self.text.grid(row=0, column=1, pady=20, padx=(10, 50))
        
        self.img.bind('<Button-1>', self.get_pos)
        self.text.bind("<Return>", self.open_website)
        self.app.bind("<Control-w>", self.exit)
        
        
    def open_website(self, event):
        """Open a new tab in the default browser with the search query."""
        link = "https://google.com/search?q=" + quote(self.text.get())
        webbrowser.open(link)
        self.text.delete(0, tk.END)
        
        
if __name__ == "__main__":
    websearch().app.mainloop()