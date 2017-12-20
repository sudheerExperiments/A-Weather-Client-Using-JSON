import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import WeatherProcesser as wp


# For right frame --> Call this
class GraphicsDisplayFrame(tk.Frame):
    def __init__(self, root, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.root = root
        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self,bg='yellow')
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)


class WidgetsWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Status bar
        self.status_bar = StatusBar(self, self, bd=1, relief=tk.SUNKEN)

        self.center_frame = tk.Frame(self, bg='yellow')
        self.interface_setup = wp.InterfaceSetup(self, self.center_frame, self.status_bar)

        # Create a frame for displaying graphics
        self.center_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.center_frame.grid_propagate(True)

        self.status_bar.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)


class StatusBar(tk.Frame):
    def __init__(self, root, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.label = tk.Label(self)
        self.label.grid(row=0, sticky=tk.N + tk.E + tk.S + tk.W)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


def close_window_callback(root):
    if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()


widgets_window = WidgetsWindow()
# widgets_window.wm_state('zoomed')
widgets_window.title('Weather forcast system')
# window co-ordinates ==> y,x
widgets_window.minsize(500, 300)
widgets_window.protocol("WM_DELETE_WINDOW", lambda root_window=widgets_window: close_window_callback(root_window))
widgets_window.mainloop()