#Requirements:
# Enter site/app name to access password 
# function to generate safe passwords 
# Interaction w/ database to store and retrieve passwords
# autocopy to clipboard

from password_database import *
from hashing_passwords import *

import psycopg2
import os

from tkinter import *
from tkinter import messagebox

class AdminWindow(Frame):

    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        self.show_login()
        
    #code to ensure users can tab between fields on the GUI
    def focus_next_window(self,event):
        event.widget.tk_focusNext().focus()
        return("break")

    # clear the window of all widgets
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    # exit the python program
    def client_exit(self):
        exit()


    def show_login(self):

        # clear the widow of any previous widgets
        self.clear_window()
        
        # row 1
        self.label = Label(self,text="Login...", font=("Arial Narrow",24))
        self.label.grid(row=1, column = 1, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky=W)

        # row 2 - one line of text
        
        self.usernameLabel = Label(self, text="Username", font=("Arial Narrow",16))
        self.usernameLabel.grid(row=2, column = 1, columnspan = 1, rowspan = 1, padx=10, pady=10)
        self.usernameTextBox = Entry(self,width=50)
        self.usernameTextBox.grid(row=2, column = 2, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky="w")
        self.usernameTextBox.bind("<Tab>", self.focus_next_window)
        self.usernameTextBox.focus()

        # work around for foriegn characaters
        self.usernameTextBox.bind("<Control-n>", lambda event: self.usernameTextBox.insert(999,"ñ"))
        self.usernameTextBox.bind("<Control-Shift-N>", lambda event: self.usernameTextBox.insert(999,"Ñ"))
        self.usernameTextBox.bind("<Control-u>", lambda event: self.usernameTextBox.insert(999,"ü"))
        self.usernameTextBox.bind("<Control-Shift-U>", lambda event: self.usernameTextBox.insert(999,"Ü"))
        
        # add logo
        self.welcome = PhotoImage(file = "logo.png")
        self.welcomeimage =Label(self, image=self.welcome).grid(row = 2, column = 7, columnspan = 1, rowspan = 1, padx=10, pady=10)
        
        # row3
        self.password1Label = Label(self, text="Password", font=("Arial Narrow",16))
        self.password1Label.grid(row=3, column = 1, columnspan = 1, rowspan = 1, padx=10, pady=10)       
        self.password1TextBox = Entry(self,show="*",width=50)
        self.password1TextBox.grid(row=3, column = 2, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky="w")
        self.password1TextBox.bind("<Tab>", self.focus_next_window)
        self.password1TextBox.focus()
       
        # row4
        self.loginButton = Button(self,text='Login',command=self.login,width=20)
        self.loginButton.grid(row=4, column = 1, columnspan = 1, rowspan = 1, padx=10, pady=10)

        

        
    def login(self):
        
        myname = self.usernameTextBox.get()
        mypassword = self.password1TextBox.get()

        #this uses code from password_database
        results = userlogin(myname, mypassword)

        if results[0] == "Error":
            if results[1] == "Username not found":
                messagebox.showerror("Error", "Username not found")
            else:
                messagebox.showerror("Error", "Password incorrect")
        else:
            messagebox.showinfo("Information","Logged in " + myname)
            self.show_menu(results[0])


    def show_menu(self,userid):
           
        # clear the widow of any previous widgets
        self.clear_window()

        # row 1
        self.label = Label(self,text="Menu...", font=("Arial Narrow",24))
        self.label.grid(row=1, column = 1, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky=W)

        # row 2
        self.new_passwordButton = Button(self,text='Create new password',command=self.new_password,width=20)
        self.new_passwordButton.grid(row=2, column = 3, columnspan = 1, rowspan = 1, padx=10, pady=10)

        # row 3
        self.searchButton = Button(self,text='Find a password',command=self.search,width=20)
        self.searchButton.grid(row=3, column = 3, columnspan = 1, rowspan = 1, padx=10, pady=10)
        
        self.show_allButton = Button(self,text='Show all',command=self.show_all,width=24)
        self.show_allButton.grid(row=4, column = 3, columnspan = 1, rowspan = 1, padx=10, pady=10)
        
        # buttons at bottom of window
        self.logoutButton = Button(self,text='Log out',command=self.show_login,width=20)
        self.logoutButton.grid(row=20, column = 1, columnspan = 1, rowspan = 1, padx=10, pady=10)

    def show_new_password(self):
        # clear the widow of any previous widgets
        self.clear_window()

        # row 1
        self.label = Label(self,text="Create Login Credentials...", font=("Arial Narrow",24))
        self.label.grid(row=1, column = 1, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky=W)

        # row 2 
        
        self.usernameLabel = Label(self, text="Username ", font=("Arial Narrow",16))
        self.usernameLabel.grid(row=2, column = 1, columnspan = 1, rowspan = 1, padx=10, pady=10)
        self.usernameTextBox = Entry(self,width=50)
        self.usernameTextBox.grid(row=2, column = 2, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky="w")
        self.usernameTextBox.bind("<Tab>", self.focus_next_window)
        self.usernameTextBox.focus()

        # work around for foriegn characaters
        self.usernameTextBox.bind("<Control-n>", lambda event: self.usernameTextBox.insert(999,"ñ"))
        self.usernameTextBox.bind("<Control-Shift-N>", lambda event: self.usernameTextBox.insert(999,"Ñ"))
        self.usernameTextBox.bind("<Control-u>", lambda event: self.usernameTextBox.insert(999,"ü"))
        self.usernameTextBox.bind("<Control-Shift-U>", lambda event: self.usernameTextBox.insert(999,"Ü"))
        
        # row3
        self.password2Label = Label(self, text="Password", font=("Arial Narrow",16))
        self.password2Label.grid(row=3, column = 1, columnspan = 1, rowspan = 1, padx=10, pady=10)       
        self.password2TextBox = Entry(self,show="*",width=50)
        self.password2TextBox.grid(row=3, column = 2, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky="w")
        self.password2TextBox.bind("<Tab>", self.focus_next_window)
        self.password2TextBox.focus()

        # row4
        self.urlLabel = Label(self, text="URL", font=("Arial Narrow",16))
        self.urlLabel.grid(row=4, column = 1, columnspan = 1, rowspan = 1, padx=10, pady=10)       
        self.urlTextBox = Entry(self,width=50)
        self.urlTextBox.grid(row=4, column = 2, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky="w")
        self.urlTextBox.bind("<Tab>", self.focus_next_window)
        self.urlTextBox.focus()

        # row5
        self.nameLabel = Label(self, text="App / Website name", font=("Arial Narrow",16))
        self.nameLabel.grid(row=5, column = 1, columnspan = 1, rowspan = 1, padx=10, pady=10)       
        self.nameTextBox = Entry(self,width=50)
        self.nameTextBox.grid(row=5, column = 2, columnspan = 4, rowspan = 1, padx=10, pady=10, sticky="w")
        self.nameTextBox.bind("<Tab>", self.focus_next_window)
        self.nameTextBox.focus()

        create_password(username,password,url,name)


    def search(self):
        # clear the widow of any previous widgets
        self.clear_window()

    def show_all(self):
        # clear the widow of any previous widgets
        self.clear_window()
        
###############################################
###############################################
# MAIN PROGRAM
if __name__ == "__main__":

    # root window created. Here, that would be the only window, but you can later have windows within windows.
    root = Tk()
    root.geometry("1000x800")

    # invoke the button on the return key
    root.bind_class("Button", "<Key-Return>", lambda event: event.widget.invoke())

    # remove the default behavior of invoking the button with the space key
    root.unbind_class("Button", "<Key-space>")

    # start fullscreen
    root.attributes("-fullscreen", True)
    root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

    #creation of an instance
    app = AdminWindow(root)

    #mainloop 
    root.mainloop() 
