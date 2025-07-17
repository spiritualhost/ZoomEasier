#Importing everything from tkinter as well as the ttk submodule, which includes themed modern widgets
from tkinter import *
from tkinter import ttk

#Importing self-defined functions
import func as f

if __name__ == "__main__":
  
    #Setting up the main application window
    root = Tk()
    root.title("Zoom Easier")

    #Setting max and min window size
    root.minsize(300,200)
    root.maxsize(600,400)


    #Creating a content frame, which holds GUI contents
    #Columnconfigure and rowconfigure tell Tk to expand the frame to match the size of the window
    frm = ttk.Frame(root, padding=10)
    frm.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)  

    #Adding widgets to the content frame
    
    #Title
    ttk.Label(frm, text="Paste Zoom link below!").grid(column=1, row=0)

    #Link entry box
    link = StringVar()
    linkEntry = ttk.Entry(frm, width=50, textvariable=link)
    linkEntry.grid(column=1, row=1)

    #Enter button
       


    #Quit button
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=2)

    #Adding padding
    for child in frm.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    #Focus cursor on entry box and bind "Enter" to pressing activate button
    linkEntry.focus()

    #Starting the application
    root.mainloop()