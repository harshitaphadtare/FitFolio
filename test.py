from tkinter import *

root=Tk()
root.title("Dropdown boxes")
root.geometry("400x400")

def show():
    label = Label(root,text=clicked.get()).pack()

options = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(root,clicked,*options).pack()

btn = Button(root,text="Show Selection",command=show).pack()

root.mainloop()