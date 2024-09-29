# Password Manager GUI Application

## Overview

I built this project as a **Password Manager** using Python, with **Tkinter** for the graphical user interface (GUI), **SQLite** for the database, and additional libraries for functionality like password hashing and clipboard management. The application provides an admin interface that allows users to securely manage login credentials, including storing, retrieving, and deleting credentials for various websites or applications. 

## Features

### 1. **User Authentication**
- **Login System**: I implemented a login system that allows users to log in using their username and password. The passwords are securely hashed using the **SHA-256** algorithm before being stored in the database.
- **Create New Users**: Administrators can create new users by entering a username and password. The password is hashed and stored securely in the `table_users` database.

### 2. **Password Management**
- **Add Credentials**: Users can store credentials (username, password, URL, and app/website name) for different websites and applications.
- **Search Functionality**: I added a search feature that allows users to filter saved credentials based on username, website/app name, or URL.
- **Copy to Clipboard**: Users can copy usernames or passwords to their clipboard with the click of a button, using the **pyperclip** library.
- **Delete Credentials**: Users can delete saved credentials directly from the search results window, giving them full control over their stored data.

### 3. **Password Visibility Toggle**
- When entering passwords, users have the option to toggle between hidden (masked) and plain text, which enhances both usability and security.

### 4. **Foreign Character Support**
- The login form supports special foreign characters like `ñ`, `Ñ`, `ü`, and `Ü` via specific key combinations, which improves accessibility.

### 5. **Graphical User Interface (GUI)**
- I used the **Tkinter** library to create the GUI. The design is simple yet functional, featuring buttons, text entry boxes, labels, and popup dialogs for user interactions.

### 6. **SQLite Database**
- Credentials are stored securely in an **SQLite** database (`password_database.db`). The database includes tables for user management (`table_users`) and stored credentials (`accounts`).
- The schema ensures that user passwords are hashed before storage, and credentials are stored securely, with efficient search capabilities built in.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/HufsaHaq/password-manager.git
    ```

2. Install dependencies:
    ```bash
    pip install pyperclip
    ```

3. Run the application:
    ```bash
    python password_manager.py
    ```

## Usage

- **Login**: Use your username and password to log in. If you're a new user, click "Create New User" to set up an account.
- **Add Credentials**: After logging in, you can add new credentials for websites or applications by clicking "Create New Credentials."
- **Search Credentials**: Use the search feature to find stored credentials by username, app/website name, or URL.
- **Copy to Clipboard**: Once you find a credential, select it and copy either the username or password to your clipboard.
- **Delete Credentials**: You can delete stored credentials directly from the search results if needed.



