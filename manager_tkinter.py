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

##################################################################################################################################################################################

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

        # this uses code from password_database
        results = userlogin(myname, mypassword)

        if results[0] == "Error":
            if results[1] == "Username not found":
                messagebox.showerror("Error", "Username not found")
            else:
                messagebox.showerror("Error", "Password incorrect")
        else:
            messagebox.showinfo("Information", "Logged in " + myname)
            self.show_menu(results[1])  # Pass the 'userid' to show_menu


##################################################################################################################################################################################

    def show_menu(self, userid):
        # clear the window of any previous widgets
        self.clear_window()

        # row 1
        self.label = Label(self, text="Menu...", font=("Arial Narrow", 24))
        self.label.grid(row=1, column=1, columnspan=4, rowspan=1, padx=10, pady=10, sticky=W)

        # row 2
        self.new_credentialsButton = Button(self, text='Create new credentials', command=lambda: self.show_new_credentials(userid), width=20)
        self.new_credentialsButton.grid(row=2, column=3, columnspan=1, rowspan=1, padx=10, pady=10)

        # row 3
        self.searchButton = Button(self, text='Search', command=lambda: self.show_search(userid), width=20)
        self.searchButton.grid(row=3, column=3, columnspan=1, rowspan=1, padx=10, pady=10)

        # buttons at bottom of window
        self.logoutButton = Button(self, text='Log out', command=self.show_login, width=20)
        self.logoutButton.grid(row=20, column=1, columnspan=1, rowspan=1, padx=10, pady=10)

##################################################################################################################################################################################

    def show_new_credentials(self, userid):
        # clear the window of any previous widgets
        self.clear_window()

        # row 1
        self.label = Label(self, text="Create Login Credentials...", font=("Arial Narrow", 24))
        self.label.grid(row=1, column=1, columnspan=4, rowspan=1, padx=10, pady=10, sticky=W)

        # row 2
        self.username1Label = Label(self, text="Username ", font=("Arial Narrow", 16))
        self.username1Label.grid(row=2, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.username1TextBox = Entry(self, width=50)
        self.username1TextBox.grid(row=2, column=2, columnspan=4, rowspan=1, padx=10, pady=10, sticky="w")
        self.username1TextBox.bind("<Tab>", self.focus_next_window)
        self.username1TextBox.focus()

        # work around for foreign characters
        self.username1TextBox.bind("<Control-n>", lambda event: self.username1TextBox.insert(999, "ñ"))
        self.username1TextBox.bind("<Control-Shift-N>", lambda event: self.username1TextBox.insert(999, "Ñ"))
        self.username1TextBox.bind("<Control-u>", lambda event: self.username1TextBox.insert(999, "ü"))
        self.username1TextBox.bind("<Control-Shift-U>", lambda event: self.username1TextBox.insert(999, "Ü"))

        # row 3
        self.password2Label = Label(self, text="Password", font=("Arial Narrow", 16))
        self.password2Label.grid(row=3, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.password2TextBox = Entry(self, show="*", width=50)
        self.password2TextBox.grid(row=3, column=2, columnspan=4, rowspan=1, padx=10, pady=10, sticky="w")
        self.password2TextBox.bind("<Tab>", self.focus_next_window)
        self.password2TextBox.focus()

        # row 4
        self.urlLabel = Label(self, text="URL", font=("Arial Narrow", 16))
        self.urlLabel.grid(row=4, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.urlTextBox = Entry(self, width=50)
        self.urlTextBox.grid(row=4, column=2, columnspan=4, rowspan=1, padx=10, pady=10, sticky="w")
        self.urlTextBox.bind("<Tab>", self.focus_next_window)
        self.urlTextBox.focus()

        # row 5
        self.nameLabel = Label(self, text="App / Website name", font=("Arial Narrow", 16))
        self.nameLabel.grid(row=5, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.nameTextBox = Entry(self, width=50)
        self.nameTextBox.grid(row=5, column=2, columnspan=4, rowspan=1, padx=10, pady=10, sticky="w")
        self.nameTextBox.bind("<Tab>", self.focus_next_window)
        self.nameTextBox.focus()

        # row 6
        self.createButton = Button(self, text='Create', command=lambda: self.new_credentials(userid), width=20)
        self.createButton.grid(row=6, column=1, columnspan=1, rowspan=1, padx=10, pady=10)

        self.backButton = Button(self, text='Back To Menu', command=lambda: self.show_menu(userid), width=20)
        self.backButton.grid(row=6, column=4, columnspan=1, rowspan=1, padx=10, pady=10)

            
    def new_credentials(self, userid):
        username = self.username1TextBox.get()
        password = self.password2TextBox.get()
        url = self.urlTextBox.get()
        name = self.nameTextBox.get()

        # Print values for debugging
        print(f"Username: {username}, Password: {password}, URL: {url}, Name: {name}")

        try:
            # this uses code from password_database
            create_password(userid, username, password, url, name)
            messagebox.showinfo("Created", "Program executed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create credentials: {e}")

        
##################################################################################################################################################################################
    def show_search(self, userid):
        # clear the window of any previous widgets
        self.clear_window()

        # row 1
        self.label = Label(self, text="Search...", font=("Arial Narrow", 24))
        self.label.grid(row=1, column=1, columnspan=4, rowspan=1, padx=10, pady=10, sticky=W)

        # row 2
        self.usernamexLabel = Label(self, text="Username ", font=("Arial Narrow", 16))
        self.usernamexLabel.grid(row=2, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.usernamexTextBox = Entry(self, width=50)
        self.usernamexTextBox.grid(row=2, column=2, columnspan=4, rowspan=1, padx=10, pady=10, sticky="w")
        self.usernamexTextBox.bind("<Tab>", self.focus_next_window)
        self.usernamexTextBox.focus()

        # work around for foreign characters
        self.usernamexTextBox.bind("<Control-n>", lambda event: self.usernamexTextBox.insert(999, "ñ"))
        self.usernamexTextBox.bind("<Control-Shift-N>", lambda event: self.usernamexTextBox.insert(999, "Ñ"))
        self.usernamexTextBox.bind("<Control-u>", lambda event: self.usernamexTextBox.insert(999, "ü"))
        self.usernamexTextBox.bind("<Control-Shift-U>", lambda event: self.usernamexTextBox.insert(999, "Ü"))

        # row 3
        self.passwordxLabel = Label(self, text="Password", font=("Arial Narrow", 16))
        self.passwordxLabel.grid(row=3, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.passwordxTextBox = Entry(self, show="*", width=50)
        self.passwordxTextBox.grid(row=3, column=2, columnspan=4, rowspan=1, padx=10, pady=10, sticky="w")
        self.passwordxTextBox.bind("<Tab>", self.focus_next_window)
        self.passwordxTextBox.focus()

        # row 4
        self.urlxLabel = Label(self, text="URL", font=("Arial Narrow", 16))
        self.urlxLabel.grid(row=4, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.urlxTextBox = Entry(self, width=50)
        self.urlxTextBox.grid(row=4, column=2, columnspan=4, rowspan=1, padx=10, pady=10, sticky="w")
        self.urlxTextBox.bind("<Tab>", self.focus_next_window)
        self.urlxTextBox.focus()

        # row 5
        self.namexLabel = Label(self, text="App / Website name", font=("Arial Narrow", 16))
        self.namexLabel.grid(row=5, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.namexTextBox = Entry(self, width=50)
        self.namexTextBox.grid(row=5, column=2, columnspan=4, rowspan=1, padx=10, pady=10, sticky="w")
        self.namexTextBox.bind("<Tab>", self.focus_next_window)
        self.namexTextBox.focus()

        # row 6
        self.searchButton = Button(self, text='Search', command=lambda: self.search(userid), width=20)
        self.searchButton.grid(row=6, column=1, columnspan=1, rowspan=1, padx=10, pady=10)

        self.backButton = Button(self, text='Back To Menu', command=lambda: self.show_menu(userid), width=20)
        self.backButton.grid(row=6, column=4, columnspan=1, rowspan=1, padx=10, pady=10)
           
    def search(self, userid):
        username = self.usernamexTextBox.get()
        password = self.passwordxTextBox.get()
        url = self.urlxTextBox.get()
        name = self.namexTextBox.get()

        # this uses code from password_database
        results = search(userid, username, password, url, name)
    
        if results:
            show_results(results)
        else:
            messagebox.showinfo("Information", "No records found")
    
    def show_results(self, results):
        for i in range(len(results)):
            for j in range(len(results[0])):
                 
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                 
                self.e.grid(row=i, column=j)
                self.e.insert(END, results[i][j])
        
##################################################################################################################################################################################

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
