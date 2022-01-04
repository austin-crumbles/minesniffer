"""Loading window"""
bar_win = Toplevel(root)
bar_win.withdraw()
bar_f = Frame(bar_win)
bar_label = Label(bar_f, text="Loading BombSniffer...")
bar_f.grid(padx=10, pady=10)
bar_label.grid(pady=(0, 5))
bar_win.deiconify()