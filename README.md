# Windows-Widgets
 <img src="https://skillicons.dev/icons?i=py,windows" />

<p style="text-align:center">A collection of beautifull and modern windows widgets written in python with tkinter</p>

![](assets/screenshot.png)

## ⚙️ Requirements

using [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap):
    
```bash
pip install ttkbootstrap
```

Works on Windows only and tested only on python 3.11 (but should work on higher versions, not tested on lower versions)

## 🛠️ Installation
To install the widgets, you have to clone the repository and copy the `widgets` folder to your project directory.

You can download in in zip format and extract it to your project directory or run the following command in your project directory:

```bash
git clone https://github.com/AZachia/Windows-Widgets.git && cd Windows-Widgets
```

## 🚀 Usage 
To run one widget especially, you just have to run it as a script.

## Create your own widget
To create your own widget, you have to create a new python file in the `widgets` folder and create a class that inherits from `widget.widget`:

```python
from widget import widget

class MyWidget(widget):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Your code here

if __name__ == "__main__":
    MyWidget().app.mainloop()
```

for example, to display a simple window with a label, you can do:

```python
from widget import widget
import tkinter as tk

class HelloWidget(widget):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = tk.Label(self.app, text="Hello, World!", font=("Arial", 20))
        self.label.pack(padx=30, pady=30)

if __name__ == "__main__":
    HelloWidget().app.mainloop()
```

## 📋 Widgets list
- [clock](clock.py) (display the current time with seconds)
- [datetime](date_time.py) (display the current date and time)
- [volume](volume.py) (set & get the system volume in real time)
- [luminosity](luminosity.py) (set & get the system luminosity in real time)
- [websearch](websearch.py) (search on google the text in the entry)

## 🤝 Contributing

If you want to contribute to this project, you can fork the repository and create a pull request.
