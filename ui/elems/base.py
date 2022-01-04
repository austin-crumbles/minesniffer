from tkinter import Tk
from tkinter import ttk

root = Tk()
root.title("BombSniffer")
root.protocol('WM_DELETE_WINDOW', stop_threads)

s = ttk.Style()
s.theme_use('default')