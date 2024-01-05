# import tkinter as tk

# class MyGUI:
#     def __init__(self, master):
#         self.master = master
#         master.title("My GUI")

#         self.label = tk.Label(master, text="Hello, Tkinter!")
#         self.label.pack()

#         self.button = tk.Button(master, text="Click Me", command=self.on_button_click)
#         self.button.pack()

#     def on_button_click(self):
#         print("Button clicked!")

# # Create the main window
# root = tk.Tk()

# # Instantiate the MyGUI class
# my_gui = MyGUI(root)

# # Start the Tkinter event loop
# root.mainloop()







####################################
# back and forward
# from tkinter import *

# class Page:
#     def __init__(self, master, name):
#         self.master = master
#         self.frame = Frame(master)
#         self.name = name
#         self.label = Label(self.frame, text=name)
#         self.label.pack(pady=10)

#     def show(self):
#         self.frame.pack(fill="both", expand=True)

#     def hide(self):
#         self.frame.pack_forget()

# class MyApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title('Navigation Example')

#         self.pages = []
#         self.current_page_index = 0

#         self.page1 = Page(master, "Page 1")
#         self.pages.append(self.page1)

#         self.page2 = Page(master, "Page 2")
#         self.pages.append(self.page2)

#         self.page3 = Page(master, "Page 3")
#         self.pages.append(self.page3)

#         self.forward_button = Button(master, text="Forward", command=self.show_next_page)
#         self.forward_button.pack(side=RIGHT)

#         self.backward_button = Button(master, text="Backward", command=self.show_previous_page)
#         self.backward_button.pack(side=LEFT)

#         self.show_current_page()

#     def show_next_page(self):
#         if self.current_page_index < len(self.pages) - 1:
#             self.pages[self.current_page_index].hide()
#             self.current_page_index += 1
#             self.show_current_page()

#     def show_previous_page(self):
#         if self.current_page_index > 0:
#             self.pages[self.current_page_index].hide()
#             self.current_page_index -= 1
#             self.show_current_page()

#     def show_current_page(self):
#         self.pages[self.current_page_index].show()

# if __name__ == "__main__":
#     root = Tk()
#     app = MyApp(root)
#     root.mainloop()


