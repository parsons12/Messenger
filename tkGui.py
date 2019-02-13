from tkinter import *
from messenger import *
import tkinter.scrolledtext as tkst
from PIL import Image, ImageTk


#create popup window and its specific attributes and functions
class composePopupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        top.title('Compose')
        top.geometry('350x350')
        self.tolbl = Label(top, text = "To:")
        self.tolbl.place(relx = .1, rely=.2, anchor='c')
        self.tobox = Entry(top, width =20, highlightbackground = 'Black')
        self.tobox.place(relx = .5, rely=.2, anchor='c')
        self.msglbl = Label(top, text = "What would you like to say?")
        self.msglbl.place(relx = .5, rely=.4, anchor='c')
        self.replybox = Entry(top, width =30, highlightbackground = 'Black')
        self.replybox.place(relx = .5, rely=.55, anchor='c')
        self.sendBtn = Button(top, text="Send", command = self.send)
        self.sendBtn.place(relx = .4, rely = .7)
    def send(self):
        self.person = self.tobox.get()
        self.message = self.replybox.get()
        write_a_message(self.person, self.message)
        self.top.destroy()

#create add contact window and its specific attributes and functions
class addPopupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        top.title('Add Contact')
        top.geometry('350x350')
        self.namelbl = Label(top, text = "Name:")
        self.namelbl.place(relx = .1, rely=.2, anchor='c')
        self.namebox = Entry(top, width =20, highlightbackground = 'Black')
        self.namebox.place(relx = .5, rely=.2, anchor='c')
        self.infolbl = Label(top, text = "Email or Phone Number:")
        self.infolbl.place(relx = .5, rely=.4, anchor='c')
        self.infobox = Entry(top, width =30, highlightbackground = 'Black')
        self.infobox.place(relx = .5, rely=.55, anchor='c')
        self.addBtn = Button(top, text="Add", command = self.add)
        self.addBtn.place(relx = .4, rely = .7)
    def add(self):
        self.name=self.namebox.get()
        self.number=self.infobox.get()
        addContact(self.name, self.number)
        self.top.destroy()

#create delete contact window and its specific attributes and functions
class deletePopupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        top.title('Delete Contact')
        top.geometry('270x150')
        self.namelbl = Label(top, text = "Name:")
        self.namelbl.place(relx = .1, rely=.2, anchor='c')
        self.namebox = Entry(top, width =15, highlightbackground = 'Black')
        self.namebox.place(relx = .5, rely=.2, anchor='c')
        self.deleteBtn = Button(top, text="Delete", command = self.delete)
        self.deleteBtn.place(relx = .4, rely = .7)
    def delete(self):
        self.name=self.namebox.get()
        deleteContact(self.name)
        self.top.destroy()

#create reply window and its specific attributes and functions
class replyPopupWindow(object):
    def __init__(self,master,recipient):
        self.recipient = recipient
        top=self.top=Toplevel(master)
        top.title('Reply')
        top.geometry('350x350')
        self.msglbl = Label(top, text = "What would you like to say?")
        self.msglbl.place(relx = .5, rely=.3, anchor='c')
        self.replybox = Entry(top, width =30, highlightbackground = 'Black')
        self.replybox.place(relx = .5, rely=.5, anchor='c')
        self.sendBtn = Button(top, text="Send", command = self.reply)
        self.sendBtn.place(relx = .4, rely = .7)
    def reply(self):
        self.msg=self.replybox.get()
        write_a_message(self.recipient, self.msg)
        self.top.destroy()

#create main window and its specific attributes and functions
class mainWindow(object):
    def __init__(self,master):
        self.master=master
        #specify the main window background image
        img = Image.open("cartoon.jpg")#change file for different background
        photo = ImageTk.PhotoImage(img)
        label = Label(root, image = photo)
        label.image = photo # keep a reference!
        label.pack()

        #create and place all widgets
        self.text = tkst.ScrolledText(label,
                                 width = 50,
                                 height = 10,
                                 highlightbackground = 'Black')
        self.text.place(relx=.5,rely=.25, anchor='c')
        self.deleteContactBtn = Button(master, text="DeleteContact", command = self.deletePopup)
        self.deleteContactBtn.place(relx=.85,rely=.9, anchor='c')

        self.addContactBtn = Button(master, text="Add Contact", command = self.addPopup)
        self.addContactBtn.place(relx=.6,rely=.9, anchor='c')

        self.getMsgBtn = Button(master, text="Check Inbox", command = self.getMsg)
        self.getMsgBtn.place(relx=.35,rely=.9, anchor='c')

        self.composeBtn = Button(master, text="Compose", command = self.composePopup)
        self.composeBtn.place(relx=.1,rely=.9, anchor='c')

        self.replybtn = Button(master, text="Reply?", command = self.replyPopup)

        self.showContactsBtn = Button(master, text="Show Contacts", command = self.getContacts)
        self.showContactsBtn.place(relx=.5,rely=.75, anchor='c')


    def composePopup(self):
        self.replybtn.place_forget()
        self.w=composePopupWindow(self.master)
    def deletePopup(self):
        self.replybtn.place_forget()
        self.w=deletePopupWindow(self.master)
    def addPopup(self):
        self.replybtn.place_forget()
        self.w=addPopupWindow(self.master)
    def replyPopup(self):
        recipient = self.text.get("1.0","end-1c").splitlines()
        recipient = recipient[0]
        self.w=replyPopupWindow(self.master, recipient)

    def getMsg(self):
        msg = checkMail()
        self.text.delete(1.0, END)
        self.text.insert(INSERT, msg)
        if(msg != 'NO NEW MESSAGES'):
            self.replybtn.place(relx=.5,rely=.62, anchor='c')
        else:
            self.replybtn.place_forget()

    def getContacts(self):
        self.replybtn.place_forget()
        self.text.delete(1.0, END)
        record = show_contacts()
        for person in record:
            self.text.insert(INSERT, person)
            self.text.insert(INSERT, "\n")

if __name__ == "__main__":
    root=Tk()
    root.title("Messenger")
    root.geometry("450x300")
    root.resizable(False, False)
    app = mainWindow(root)
    root.mainloop()
