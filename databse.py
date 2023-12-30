#database to store login info

conn = sqlite3.connect('fitfolio.db')
cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE accounts (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         fullname TEXT,
#         dob TEXT,
#         username TEXT UNIQUE,
#         password TEXT,
#         gender TEXT
#     )
# ''')
conn.commit()


def create_account():
    try:
        fullname_val = fullname_entry.get()
        dob_val = dob_entry.get_date()
        username_val = username_entry.get()
        password_val = password_entry.get()
        gender_val = clicked.get()

        cursor.execute('''
            INSERT INTO accounts (fullname, dob, username, password, gender)
            VALUES (?, ?, ?, ?, ?)
        ''', (fullname_val, dob_val, username_val, password_val, gender_val))

        conn.commit()

        # account created message
        messagebox.showinfo("Account Created", "Your account has been created successfully.")

        # to handle error

    except Exception as e:
        print("Error:", e)
        
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



def delete_account():
    result = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
    
    if result:
        
        cursor.execute('DELETE FROM accounts WHERE username = ?', (username_entry.get(),))
        conn.commit()
        messagebox.showinfo("Account Deleted", "Your account has been deleted.")
        top.destroy()  


root.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), root.destroy()))

conn.commit()



root.mainloop()