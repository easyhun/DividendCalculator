import tkinter as tk
from tkinter import ttk
import os

def treeview(tree):
    style = ttk.Style()
    style.theme_use('default')

    style.configure("Treeview",
                    background="#FFFFFF",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")

    style.map('Treeview',
              background=[('selected', 'blue')],
              foreground=[('selected', 'white')])

    tree.config(style="Treeview")

def frame(frame):
    frame.configure(bg="#FFFFFF")
