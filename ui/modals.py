from tkinter import ttk
import logging

def make_gridsize_modal(parent, widthvar, heightvar, validation_func):
    root = parent.root
    frame = ttk.Frame(root, style="modal.TFrame")
    disclaim_text = ttk.Label(
        frame,
        text="Grid size will update in the next game"
    )
    dim_frame = ttk.Frame(frame, style="modal.TFrame")
    width_label = ttk.Label(
        dim_frame,
        text="W",
        style="option.TLabel"
    )
    width_entry = ttk.Entry(
        dim_frame,
        width=2,
        textvariable=widthvar,
        validate="focusout",
        validatecommand=validation_func,
        invalidcommand=invalid,
        justify="center"
    )
    height_label = ttk.Label(
        dim_frame,
        text="H",
        style="option.TLabel"
    )
    x_label = ttk.Label(dim_frame, text="x")
    height_entry = ttk.Entry(
        dim_frame,
        width=2,
        textvariable=heightvar,
        validate="focusout",
        validatecommand=validation_func,
        invalidcommand=invalid,
        justify="center"
    )
    close_button = ttk.Button(
        frame, 
        text="Close", 
        command=parent.hide_gridsize_modal
    )

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)

    width_entry.grid(row=0, column=0, pady=5, ipadx=10, ipady=10)
    x_label.grid(row=0, column=1, padx="15")
    height_entry.grid(row=0, column=2, pady=5, ipadx=10, ipady=10)
    width_label.grid(row=1, column=0, pady=(1, 5))
    height_label.grid(row=1, column=2, pady=(1, 5))

    disclaim_text.grid(row=0, column=0, columnspan=2, pady=(10, 0))
    dim_frame.grid(row=2, column=0, columnspan=2)
    close_button.grid(row=3, column=0, pady=(5, 10), columnspan=2)

    return frame

def invalid():
    logging.warn("Invalid dimensions")
