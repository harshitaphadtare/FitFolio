################################
#dont add this in main page
from tkinter import *
from PIL import ImageTk,Image
from tkinter import PhotoImage
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import messagebox
################################


class Mindfulness:
    def __init__(self,master):
        # root.withdraw()
        self.master = master
        self.master.title('Activity')
        self.master.geometry("450x530")
        self.master.resizable(0, 0)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        #back button
        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.master,image=self.resize_back ,padx=10,pady=10,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0, padx=5,sticky=NW)

        #title
        self.mind_heading = Label(master,text="Mindfulness",font=("Helvetica", 25))
        self.mind_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        #drop down for graph
        self.options = ["3-Days","Weekly","Month","Yearly"]
        self.clicked = StringVar()
        self.clicked.set("Select Timeperiod")
        self.drop = OptionMenu(master,self.clicked,*self.options)
        self.drop.grid(row=2,column=0,columnspan=2)

        #graph section
        self.frame = LabelFrame(master,padx=220,pady=100)
        self.frame.grid(row=3,column=0,columnspan=2,pady=(10,0))

        self.label = Label(self.frame,text="Graph")
        self.label.grid(row=3,column=0,)

        # track label
        self.label = Label(master,text="Track minutes of Mindfulness Now!!",font=("Verdana", 13),fg="red")
        self.label.grid(row=4,column=0,columnspan=2,pady=(10,15))

        # type entry
        self.type = Label(master,text="Mindfulness Type: ",font=("Verdana", 10))
        self.type.grid(row=5,column=0,padx=(30,0),sticky=E)
        self.options = ["Journal","Yoga","Breathing","Gardening","Music Therapy","Other"]
        self.clicked = StringVar()
        self.clicked.set(self.options[0])
        self.drop = OptionMenu(master,self.clicked,*self.options)
        self.drop.config(width=15,height=1)
        self.drop.grid(row=5,column=1,columnspan=2,padx=(0,100),sticky=W)

        #time entry
        self.time = Label(master,text="Time (Hr): ",font=("Verdana", 10))
        self.time.grid(row=6,column=0,pady=(10,0),padx=(80,0),sticky=E)
        self.time_entry = Entry(master,width=22)
        self.time_entry.grid(row=6,column=1,padx=(0,100), pady=(10,0),sticky=W)
        
        #add btn
        add_btn = Button(master, text="Add", padx=40, pady=3,font=("Verdana", 10),command=self.add_btn_mind)
        add_btn.grid(row=7, column=0, pady=(10, 0), sticky=E, padx=(70, 20)) 

        #show record btn
        show_acc = Button(master, text="Show record", pady=3, padx=30,font=("Verdana", 10),command=self.show_btn_mind)
        show_acc.grid(row=7, column=1, sticky=W, pady=(10, 0)) 
        
    def add_btn_mind(self):
        '''when distance and time are entered and add btn is clicked only then:
        1) the data from the form disappers '''
        self.response = messagebox.showinfo("Add","Record Added Successfully!")
    
    def show_btn_mind(self):

        def on_vertical_scroll(*args):
            self.canvas.yview(*args)

        def on_horizontal_scroll(*args):
            self.canvas.xview(*args)

        self.master.withdraw()
        self.record_walk = Toplevel()
        self.record_walk.title("Walking Records")
        self.record_walk.geometry("350x450")
        self.record_walk.resizable(0, 0)
        self.record_walk.grid_rowconfigure(0, weight=1)
        self.record_walk.grid_columnconfigure(0, weight=1)

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.record_walk,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.record_walk,text="Walking Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,20))
        
        self.data = LabelFrame(self.record_walk,padx=20,pady=15)
        self.data.grid(row=2,column=0,columnspan=3)
            
        # Create a Canvas widget
        self.canvas = Canvas(self.data)
        self.canvas.grid(row=0, column=0, columnspan=3, sticky=NSEW)

        self.vertical_scrollbar = ttk.Scrollbar(self.data, orient=VERTICAL, command=on_vertical_scroll)
        self.vertical_scrollbar.grid(row=0, column=2, sticky=NS)

        self.horizontal_scrollbar = ttk.Scrollbar(self.data, orient=HORIZONTAL, command=on_horizontal_scroll)
        self.horizontal_scrollbar.grid(row=1, column=0, columnspan=3, sticky=EW)

        self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)

        for i in range(20):
            ttk.Label(self.frame, text=f"Label {i}").pack(pady=5)

        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        self.vertical_scrollbar.config(command=on_vertical_scroll)
        self.horizontal_scrollbar.config(command=on_horizontal_scroll)

        #update btn
        self.update_btn = Button(self.record_walk,text="Update", padx=30, pady=3,font=("Verdana", 10),command=self.update_record_walk)
        self.update_btn.grid(row=3,column=0, pady=(10, 15), padx=(0,20),sticky=E)

        #delete btn
        self.delete_btn = Button(self.record_walk,text="Delete", pady=3, padx=30,font=("Verdana", 10),command=self.delete_record_walk)
        self.delete_btn.grid(row=3,column=1,sticky=W, pady=(10, 15), padx=(0,60))
    
        self.record_walk.mainloop()

    def delete_record_walk(self):

        self.delete_walk = Toplevel()
        self.delete_walk.title("Delete")
        self.delete_walk.geometry("220x200")
        self.delete_walk.resizable(0, 0)
        self.delete_walk .columnconfigure(0, weight=1)
        self.delete_walk .columnconfigure(1, weight=1)

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.delete_walk,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.delete_walk,text="Delete Record",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        self.id = Label(self.delete_walk,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.delete_walk,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.delete_walk, text="Delete", padx=20, bg="#ff8383",fg="white",pady=3,font=("Verdana", 10))
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.delete_walk.mainloop()
    
    def update_record_walk(self):
        self.update_walk = Toplevel()
        self.update_walk.title("Update")
        self.update_walk.geometry("300x250")
        self.update_walk.resizable(0, 0)
        self.update_walk.columnconfigure(0, weight=1)
        self.update_walk.columnconfigure(1, weight=1)

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.update_walk,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.update_walk,text="Update Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        self.id = Label(self.update_walk,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.update_walk,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.distance = Label(self.update_walk,text="Distance (Km): ",font=("Verdana", 10))
        self.distance.grid(row=3,column=0,pady=(15,0),padx=(20,5))
        self.distance_entry = Entry(self.update_walk,width=22)
        self.distance_entry.grid(row=3,column=1, padx=(0,40), pady=(15,0))

        self.time = Label(self.update_walk,text="Time (Hr): ",font=("Verdana", 10))
        self.time.grid(row=4,column=0,pady=(10,0),padx=(20,5))
        self.time_entry = Entry(self.update_walk,width=22)
        self.time_entry.grid(row=4,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.update_walk, text="Update", padx=20, pady=3,font=("Verdana", 10))
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.update_walk.mainloop()


################################
#dont add this in main page
root = Tk()
my_gui = Mindfulness(root)
root.mainloop()
################################