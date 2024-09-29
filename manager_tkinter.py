from password_database import *
import sqlite3
import os
import pyperclip  # For copying password to clipboard
from tkinter import *
from tkinter import messagebox
from hashlib import sha256  # For hashing passwords

class AdminWindow(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=1)
        self.show_login()

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def client_exit(self):
        exit()

###########################LOGIN###########################################################################################################

    def show_login(self):
        self.clear_window()

        # row 1
        self.label = Label(self, text="Login...", font=("Arial Narrow", 24))
        self.label.grid(row=1, column=1, columnspan=4, rowspan=1, padx=10, pady=10, sticky=W)

        # row 2 - Username
        self.usernameLabel = Label(self, text="Username", font=("Arial Narrow", 16))
        self.usernameLabel.grid(row=2, column=1, padx=10, pady=10)
        self.usernameTextBox = Entry(self, width=50)
        self.usernameTextBox.grid(row=2, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.usernameTextBox.bind("<Tab>", self.focus_next_window)
        self.usernameTextBox.focus()

        # Foreign characters workaround
        self.usernameTextBox.bind("<Control-n>", lambda event: self.usernameTextBox.insert(999, "ñ"))
        self.usernameTextBox.bind("<Control-Shift-N>", lambda event: self.usernameTextBox.insert(999, "Ñ"))
        self.usernameTextBox.bind("<Control-u>", lambda event: self.usernameTextBox.insert(999, "ü"))
        self.usernameTextBox.bind("<Control-Shift-U>", lambda event: self.usernameTextBox.insert(999, "Ü"))

        # Add logo
        self.welcome = PhotoImage(file=os.path.join(os.path.dirname(__file__), "logo.png"))
        self.welcomeimage = Label(self, image=self.welcome)
        self.welcomeimage.grid(row=2, column=7, padx=10, pady=10)

        # row 3 - Password
        self.password1Label = Label(self, text="Password", font=("Arial Narrow", 16))
        self.password1Label.grid(row=3, column=1, padx=10, pady=10)
        self.password1TextBox = Entry(self, show="*", width=50)  # Initially hides the password
        self.password1TextBox.grid(row=3, column=2, columnspan=4, padx=10, pady=10, sticky="w")

        # row 4 - Show Password Checkbutton
        self.show_password_var = IntVar()  # Integer variable to track the checkbox state
        self.show_password_checkbox = Checkbutton(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        self.show_password_checkbox.grid(row=4, column=2, sticky="w")

        # row 5 - Login Button
        self.loginButton = Button(self, text='Login', command=self.login, width=20)
        self.loginButton.grid(row=4, column=1, padx=10, pady=10)

        # row 6 - New User Button
        self.newUserButton = Button(self, text='Create New User', command=self.show_new_user, width=20)
        self.newUserButton.grid(row=4, column=3, padx=10, pady=10)

    def toggle_password(self):
        """Toggle the password visibility based on the checkbox."""
        if self.show_password_var.get():  # If checkbox is checked, show the password
            self.password1TextBox.config(show="")
        else:  # If unchecked, hide the password
            self.password1TextBox.config(show="*")

    def login(self):
        myname = self.usernameTextBox.get()
        mypassword = self.password1TextBox.get()

        # Call the userlogin function to validate the user
        results = userlogin(myname, mypassword)

        if not results:
            messagebox.showerror("Error", "No results found")
            return

        if results[0] == "Error":
            if results[1] == "Username not found":
                messagebox.showerror("Error", "Username not found")
            else:
                messagebox.showerror("Error", "Password incorrect")
        else:
            messagebox.showinfo("Information", "Logged in " + myname)
            print(results[2])
            self.show_menu(results[2])  # Pass the 'userid' to show_menu

###########################MENU############################################################################################################

    def show_menu(self, userid):
        self.clear_window()

        # row 1 - Menu label
        self.label = Label(self, text="Menu...", font=("Arial Narrow", 24))
        self.label.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky=W)

        # row 2 - Create new credentials button
        self.new_credentialsButton = Button(self, text='Create new credentials', command=lambda: self.show_new_credentials(userid), width=20)
        self.new_credentialsButton.grid(row=2, column=3, padx=10, pady=10)

        # row 3 - Search button
        self.searchButton = Button(self, text='Search', command=lambda: self.show_search(userid), width=20)
        self.searchButton.grid(row=3, column=3, padx=10, pady=10)

        # Logout button
        self.logoutButton = Button(self, text='Log out', command=self.show_login, width=20)
        self.logoutButton.grid(row=20, column=1, padx=10, pady=10)


###########################NEW USER########################################################################################################
    def show_new_user(self):
        self.clear_window()

        # row 1
        self.label = Label(self, text="Create New User...", font=("Arial Narrow", 24))
        self.label.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky=W)

        # row 2 - New Username entry
        self.newUsernameLabel = Label(self, text="Username", font=("Arial Narrow", 16))
        self.newUsernameLabel.grid(row=2, column=1, padx=10, pady=10)
        self.newUsernameTextBox = Entry(self, width=50)
        self.newUsernameTextBox.grid(row=2, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.newUsernameTextBox.bind("<Tab>", self.focus_next_window)

        # row 3 - New Password entry
        self.newPasswordLabel = Label(self, text="Password", font=("Arial Narrow", 16))
        self.newPasswordLabel.grid(row=3, column=1, padx=10, pady=10)
        self.newPasswordTextBox = Entry(self, show="*", width=50)
        self.newPasswordTextBox.grid(row=3, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.newPasswordTextBox.bind("<Tab>", self.focus_next_window)

        # row 4 - Create Button
        self.createUserButton = Button(self, text='Create User', command=self.create_user, width=20)
        self.createUserButton.grid(row=4, column=1, padx=10, pady=10)

        # Back Button
        self.backButton = Button(self, text='Back To Login', command=self.show_login, width=20)
        self.backButton.grid(row=4, column=3, padx=10, pady=10)

    def create_user(self):
        username = self.newUsernameTextBox.get()
        password = self.newPasswordTextBox.get()
        hashed_password = self.hash_password(password)  # Hash the password before storing it

        try:
            # Assuming a create_user function exists in password_database
            create_user(username, hashed_password)
            messagebox.showinfo("Created", "User created successfully")
            self.show_login()  # Go back to login screen
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {e}")

###########################NEW DATA###########################################################################################################

    def show_new_credentials(self, userid):
        self.clear_window()

        # row 1
        self.label = Label(self, text="Create Login Credentials...", font=("Arial Narrow", 24))
        self.label.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky=W)

        # row 2 - Username entry
        self.username1Label = Label(self, text="Username ", font=("Arial Narrow", 16))
        self.username1Label.grid(row=2, column=1, padx=10, pady=10)
        self.username1TextBox = Entry(self, width=50)
        self.username1TextBox.grid(row=2, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.username1TextBox.bind("<Tab>", self.focus_next_window)

        # row 3 - Password entry
        self.password2Label = Label(self, text="Password", font=("Arial Narrow", 16))
        self.password2Label.grid(row=3, column=1, padx=10, pady=10)
        self.password2TextBox = Entry(self, show="*", width=50)
        self.password2TextBox.grid(row=3, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.password2TextBox.bind("<Tab>", self.focus_next_window)

        # row 4 - URL entry
        self.urlLabel = Label(self, text="URL", font=("Arial Narrow", 16))
        self.urlLabel.grid(row=4, column=1, padx=10, pady=10)
        self.urlTextBox = Entry(self, width=50)
        self.urlTextBox.grid(row=4, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.urlTextBox.bind("<Tab>", self.focus_next_window)

        # row 5 - App/Website name entry
        self.nameLabel = Label(self, text="App / Website name", font=("Arial Narrow", 16))
        self.nameLabel.grid(row=5, column=1, padx=10, pady=10)
        self.nameTextBox = Entry(self, width=50)
        self.nameTextBox.grid(row=5, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.nameTextBox.bind("<Tab>", self.focus_next_window)

        # row 6 - Create Button
        self.createButton = Button(self, text='Create', command=lambda: self.new_credentials(userid), width=20)
        self.createButton.grid(row=6, column=1, padx=10, pady=10)

        self.backButton = Button(self, text='Back To Menu', command=lambda: self.show_menu(userid), width=20)
        self.backButton.grid(row=6, column=4, padx=10, pady=10)

    def new_credentials(self, userid):
        username = self.username1TextBox.get()
        password = self.password2TextBox.get()
        hashed_password = hash_password(password)  # Hash the password before storing it
        url = self.urlTextBox.get()
        name = self.nameTextBox.get()

        try:
            # Ensure userid is an integer
            userid = int(userid)  
            create_password(userid, username, hashed_password, url, name)
            messagebox.showinfo("Created", "Password created and stored")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create credentials: {e}")

###########################SEARCH###########################################################################################################
    def show_search(self, userid):
        self.clear_window()

        # row 1 - Search label
        self.label = Label(self, text="Search...", font=("Arial Narrow", 24))
        self.label.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky=W)

        # row 2 - Username entry
        self.usernamexLabel = Label(self, text="Username", font=("Arial Narrow", 16))
        self.usernamexLabel.grid(row=2, column=1, padx=10, pady=10)
        self.usernamexTextBox = Entry(self, width=50)
        self.usernamexTextBox.grid(row=2, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.usernamexTextBox.bind("<Tab>", self.focus_next_window)

        # row 3 - Name entry
        self.nameLabel = Label(self, text="App / Website Name", font=("Arial Narrow", 16))
        self.nameLabel.grid(row=3, column=1, padx=10, pady=10)
        self.nameTextBox = Entry(self, width=50)
        self.nameTextBox.grid(row=3, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.nameTextBox.bind("<Tab>", self.focus_next_window)

        # row 4 - URL entry
        self.urlLabel = Label(self, text="URL", font=("Arial Narrow", 16))
        self.urlLabel.grid(row=4, column=1, padx=10, pady=10)
        self.urlTextBox = Entry(self, width=50)
        self.urlTextBox.grid(row=4, column=2, columnspan=4, padx=10, pady=10, sticky="w")
        self.urlTextBox.bind("<Tab>", self.focus_next_window)

        # row 5 - Search button
        self.searchButton = Button(self, text='Search', command=lambda: self.perform_search(userid), width=20)
        self.searchButton.grid(row=5, column=1, padx=10, pady=10)

        # Back Button
        self.backButton = Button(self, text='Back To Menu', command=lambda: self.show_menu(userid), width=20)
        self.backButton.grid(row=5, column=4, padx=10, pady=10)

    def perform_search(self, userid):
        username = self.usernamexTextBox.get()
        name = self.nameTextBox.get()  
        url = self.urlTextBox.get()    

        try:
            # Call the search function with username, name, and url, allowing them to be None
            results = search(userid, username, name, url)

            if results:
                messagebox.showinfo("Search Result", f"Username: {results[0]}\nPassword: {results[1]}\nURL: {results[2]}\nApp/Website: {results[3]}")
            else:
                messagebox.showinfo("Search Result", "No matching credentials found")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")


###########################MAIN###########################################################################################################
if __name__ == '__main__':
    root = Tk()
    root.geometry("600x400")  # Optional: set the size of the window
    app = AdminWindow(master=root)
    root.mainloop()  # This starts the GUI loop
