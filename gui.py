from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from backup import *

import json

# TODO Add Log Window

class PyBackup:
    def __init__(self,root):
        root.title("PyBackup")
        mnuMain = MainMenu(root)
        root.config(menu=mnuMain)
        Main = MainFrame(root)  

class MainMenu(Menu):
    def __init__(self,root):
        Menu.__init__ (self,root)

        mnuFile = Menu(self,tearoff=0)
        self.add_cascade(label="File",menu=mnuFile)
        mnuFile.add_command(label="Quit",command=root.quit)

        mnuEdit = Menu(self,tearoff=0)
        self.add_cascade(label="Edit",menu=mnuEdit)
        mnuEdit.add_command(label="Preferences")

        mnuHelp = Menu(self,tearoff=0)
        self.add_cascade(label="Help",menu=mnuHelp)
        mnuHelp.add_command(label="About")

class MainFrame(Frame):
    def __init__(self,parent):
        Frame.__init__ (self,parent)

        global varSaveBackup

        # Load list of saved backups
        with open("backups.json","r",encoding="utf-8") as f:
            saved_backups = json.load(f)
        
        backups_list = list(saved_backups.keys())

        def SelectSource():
            varSource.set(filedialog.askdirectory(title = "Select Source Folder"))

        def SelectDestination():
            varDest.set(filedialog.askdirectory(title = "Select Destination Folder"))

        def RunNow():
            zip_backup(varSource.get(), varDest.get())
            messagebox.showinfo("PyBackup","Backup complete.")

        def SaveBackupPopup():
            Popup = Toplevel(parent)

            def SaveBackupName():
                varSaveBackup = txtValue.get()
                save_backup(varSource.get(),varDest.get(),varSaveBackup)
                Popup.destroy()

            def Cancel():
                Popup.destroy()

            lblEntry = Label(Popup,text="Enter a name for this backup:",font=("Helvetica",10))
            txtValue = Entry(Popup, font=("Helvetica",10))
            btnOK = Button(Popup,text="OK",width=10,command=SaveBackupName)
            btnCancel= Button(Popup,text="Cancel",width=10,command=Cancel)

            lblEntry.grid(row=0,column=0,columnspan=2,padx=10,pady=5)
            txtValue.grid(row=1,column=0,columnspan=2,padx=5,pady=5)
            btnOK.grid(row=2,column=0,sticky=(W,E),padx=5,pady=5)
            btnCancel.grid(row=2,column=1,sticky=(W,E),padx=5,pady=5)
            


        def LoadBackup(e):
            backup = load_backup(varSavedBackup.get())
            varSource.set(backup['source'])
            varDest.set(backup['dest'])


        # create widgets
        varSource=StringVar()
        btnSource = Button(self,text="Select Source",command=SelectSource)
        txtSource = Entry(self, textvariable=varSource,font=("Helvetica",10),width=30)

        varDest=StringVar()
        btnDest = Button(self,text="Select Destination",command=SelectDestination)
        txtDest = Entry(self, textvariable=varDest,font=("Helvetica",10),width=50)

        btnRunNow = Button(self,text="Run Now",command=RunNow)
        btnSaveBackup = Button(self,text="Save Backup",command=SaveBackupPopup)

        lblSelectSaved = Label(self,text="Select Saved Backup",font=("Helvetica",10))

        varSavedBackup = StringVar()
        cboSelectSaved = ttk.Combobox(self,textvariable=varSavedBackup,font=("Helvetica",10))
        cboSelectSaved['values'] = backups_list
        cboSelectSaved.bind("<<ComboboxSelected>>",LoadBackup)

        # grid the widgets
        btnSource.grid(row=0,column=0,sticky=(W),padx=5,pady=5)
        txtSource.grid(row=1,column=0,sticky=(W,E),padx=5,pady=5,columnspan=2)
        btnDest.grid(row=2,column=0,sticky=(W),padx=5,pady=5)
        txtDest.grid(row=3,column=0,sticky=(W,E),padx=5,pady=5,columnspan=2)
        btnRunNow.grid(row=4,column=0,padx=5,pady=5)
        btnSaveBackup.grid(row=4,column=1,padx=5,pady=5)
        lblSelectSaved.grid(row=5,column=0,padx=5,pady=5,columnspan=2)
        cboSelectSaved.grid(row=6,column=0,padx=5,pady=5,columnspan=2)

        self.grid(row=0,column=0,sticky=(W,E))
