import tkinter as tk
from tkinter import ttk
import mysql.connector

# Assuming db and mycur are previously defined database connection and cursor objects
# For example:
# db = mysql.connector.connect(host="your_host", user="your_username", password="your_password", database="your_database")
# mycur = db.cursor()


# db = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     port = 3306,
#     password = "Harshita@2023",
#     database= "fitfolio"
# )

# mycur = db.cursor()

import tkinter as tk
from tkinter import ttk
import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Table")
        self.root.geometry("400x400")

        # Create a Treeview widget
        self.tree = ttk.Treeview(self.root, columns=("Date", "Distance", "Time", "Calories", "Weight"), height=10)
        self.tree.heading("Date", text="Date")
        self.tree.heading("Distance", text="Distance")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Calories", text="Calories")
        self.tree.heading("Weight", text="Weight")

        # Set column widths
        self.tree.column("Date", width=80)
        self.tree.column("Distance", width=70)
        self.tree.column("Time", width=70)
        self.tree.column("Calories", width=80)
        self.tree.column("Weight", width=70)

        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)
        vsb.pack(side="right", fill=tk.Y)

        # Call the populate_treeview method
        self.populate_treeview("harshita123")

    def populate_treeview(self, username):
        sql = "SELECT date, distance, time, calories, weight FROM cardio WHERE username = %s"
        val = (username,)
        mycur.execute(sql, val)
        rows = mycur.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
