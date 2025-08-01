#Importing libraries
import sys, logging

#Importing everything from tkinter as well as the ttk submodule, which includes themed modern widgets
from tkinter import *
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from ttkbootstrap.constants import *

#Importing self-defined functions
import func as f
import compatibility as c
from historymenu import HistoryDropdown

#Set up logging
logFile = "zoomeasier.log"
logging.basicConfig(
    filename=logFile,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":

    #Initialize the history menu instance
    hd = HistoryDropdown()

    #Pre-launch compatibility check (If not good to launch, close the program before a crash)
    if not c.goodToLaunch():
        messagebox.showerror("Compatibility Error", "Zoom is not installed. Please install Zoom before using this program.")
        logger.error("Error in launch, Zoom error. Is Zoom installed on the system?")
        sys.exit()
  
    #Setting up the main application window
    #root = Tk()
    style = Style("superhero")
    root = style.master
    root.title("Zoom Easier")

    #Functions for implementing right-click to paste link functionality
    #Spawn popup
    def popup(event):
        try:
            dropdownMenu.tk_popup(event.x_root,event.y_root) # Pop the menu up in the given coordinates
        finally:
            dropdownMenu.grab_release() #Go away once option is selected

    #Get copied item from system clipboard and insert into entry widget
    def paste():
        try:
            clipboard = root.clipboard_get()
            linkEntry.insert('end', clipboard)

        except Exception as e:
            logger.exception("Error in main.py, paste() function")


    #Populate dropdown menu
    dropdownMenu = Menu(root, tearoff=0)
    dropdownMenu.add_command(label="Paste", command=paste)

    #Setting max and min window size
    root.minsize(600,400)
    root.maxsize(1200,800)

    #Creating a content frame, which holds GUI contents
    #Columnconfigure and rowconfigure tell Tk to expand the frame to match the size of the window
    frm = ttk.Frame(root, padding=10)
    frm.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1) 

    #Adding menu bar for dropdown quick access
    menubar = Menu(root)
    fileMenu = Menu(menubar, tearoff=0)


    #historySub = hd.histChoices(fileMenu)
    #fileMenu.add_cascade(label="History", menu=historySub)

    #Initialize history handler and menu
    historyMenu = Menu(fileMenu, tearoff=0)
    historyMenu.configure(postcommand=lambda: hd.refreshHistoryMenu(historyMenu))
    fileMenu.add_cascade(label="History", menu=historyMenu)
    
    fileMenu.add_separator()
    fileMenu.add_command(label="Clear History", command=hd.clearHistory)

    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=root.quit)

    menubar.add_cascade(label="File", menu=fileMenu)
    root.config(menu=menubar)


    #Adding widgets to the content frame

    #Allow a selection of which information to give in order to join a meeting
    #Default to manual mode
    joinMode = StringVar(value="manual")

    link = StringVar(root)

    linkEntry = ttk.Entry(frm, width=50, textvariable=link)
    linkEntry.insert(0, "Enter Link")
    linkEntry.grid(column=1, row=0, sticky="ew")

    meetingID = StringVar(root)
    meetingEntry = ttk.Entry(frm, width=50, textvariable=meetingID)
    meetingEntry.insert(0, "Enter Meeting ID")
    meetingEntry.grid(column=1, row=0, sticky="ew")
    
    passcode = StringVar(root)
    passcodeEntry = ttk.Entry(frm, width=50, textvariable=passcode)
    passcodeEntry.insert(0, "Enter Meeting Passcode")
    passcodeEntry.grid(column=1, row=1, sticky="ew")

    ttk.Radiobutton(frm, text="Join via Link", variable=joinMode, value="link").grid(column=1, row=3, sticky="w")
    ttk.Radiobutton(frm, text="Join via ID + Passcode", variable=joinMode, value="manual").grid(column=1, row=4, sticky="w")

    def toggleInputs(*args):
        global mode
        mode = joinMode.get()
        if mode == "link":
            linkEntry.grid()
            meetingEntry.grid_remove()
            passcodeEntry.grid_remove()
        else:
            meetingEntry.grid()
            passcodeEntry.grid()
            linkEntry.grid_remove()

    toggleInputs()

    joinMode.trace_add("write", toggleInputs)


    #Enter button
    enterButton = ttk.Button(frm,
                              text="Enter...", 
                              command=lambda: f.startMeeting(f.convertLink(link.get())) if joinMode.get() == "link" else f.startMeeting(f.manualMeeting(meetingID.get(), passcode.get())))
    enterButton.grid(column=2, row=0) 


    #Need to direct manual data into function for parsing and shortcut creating
    #Create shortcut button
    shortcut = ttk.Button(frm, 
                          text="Create shortcut...", 
                          command=lambda: f.createShortcut(link.get()) if joinMode.get() == "link" else f.createShortcut(f"https://us02web.zoom.us/j/{meetingID.get()}?pwd={passcode.get()}"))
    shortcut.grid(column=1, row=5)

    #Clear all Button
    clearAll = ttk.Button(frm, text="Clear all", command=lambda: linkEntry.delete(0, END) if joinMode.get() == "link" else (meetingEntry.delete(0, END), passcodeEntry.delete(0, END)))
    clearAll.grid(column=1, row=6)


    #Quit button
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=7)


    #Adding padding
    for child in frm.winfo_children(): 
        child.grid_configure(padx=5, pady=5)


    #Bindings
    #Focus cursor on entry box and bind "Enter" to pressing activate button
    linkEntry.focus()
    root.bind("<Return>", lambda event: f.startMeeting(f.convertLink(link.get())))

    #Bind right-click to allow paste in entry box
    linkEntry.bind('<Button 3>', popup)


    #Starting the application
    root.mainloop()