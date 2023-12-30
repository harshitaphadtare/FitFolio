from tkinter import *
from PIL import ImageTk,Image
from tkinter import PhotoImage
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import messagebox

class Activity:
    def __init__(self, master):
        self.master = master
        self.master.title('Activity')
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)

        self.back_btn = Button(self.master,image=self.resize_back,command=root.deiconify() ,padx=10,pady=10,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0, padx=5,sticky=NW)

        self.act_heading = Label(self.master,text="Activity",font=("Helvetica", 25))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        # walking
        self.frame = LabelFrame(self.master,padx=20,pady=10)
        self.frame.grid(row=2,column=0)

        self.img = PhotoImage(file="images/walk.png")
        self.resize = self.img.subsample(2,2)

        self.btn = Button(self.frame,image=self.resize,text="  Walking ",pady=5,compound=LEFT, font=("Verdana", 13),relief="flat",borderwidth=0,command=self.step_click)

        self.btn.grid(row=0,column=0,sticky=W,padx=(0,112))

        #walking forward
        self.img1 = PhotoImage(file="images/forward.png")
        self.resize1 = self.img1.subsample(3,3)

        self.btn_walk = Button(self.frame,image=self.resize1,padx=20,pady=10,compound=RIGHT,relief="flat",borderwidth=0,command=self.step_click)

        self.btn_walk.grid(row=0,column=1, sticky=E)

        #Cycling
        self.frame = LabelFrame(self.master,padx=20,pady=10)
        self.frame.grid(row=3,column=0)

        self.img_cycle = PhotoImage(file="images/cycle.png")
        self.resize_cycle = self.img_cycle.subsample(2,2)

        self.btn = Button(self.frame,image=self.resize_cycle,text="  Cycling ",pady=5, compound=LEFT, font=("Verdana", 13),relief="flat",borderwidth=0)
        self.btn.grid(row=0,column=0,sticky=W,padx=(0,120))

        #Cycling forward
        self.btn = Button(self.frame,image=self.resize1,padx=15,pady=10,compound=RIGHT,    relief="flat",borderwidth=0)
        self.btn.grid(row=0,column=1, sticky=E)

        #workout
        self.frame = LabelFrame(self.master,padx=20,pady=10)
        self.frame.grid(row=4,column=0)

        self.img_workout= PhotoImage(file="images/workout.png")
        self.resize_workout = self.img_workout.subsample(2,2)

        self.btn = Button(self.frame,image=self.resize_workout,text="  Workout ",pady=5,   compound=LEFT, font=("Verdana", 13),relief="flat",borderwidth=0)
        self.btn.grid(row=0,column=0,sticky=W,padx=(0,109))

        #workout forward
        self.btn = Button(self.frame,image=self.resize1,padx=20,pady=10,compound=RIGHT,    relief="flat",borderwidth=0)
        self.btn.grid(row=0,column=1, sticky=E)

        #running
        self.frame = LabelFrame(self.master,padx=20,pady=10)
        self.frame.grid(row=5,column=0)

        self.img_running= PhotoImage(file="images/run.png")
        self.resize_running = self.img_running.subsample(2,2)

        self.btn = Button(self.frame,image=self.resize_running,text="  Running ",pady=5,   compound=LEFT, font=("Verdana", 13),relief="flat",borderwidth=0)
        self.btn.grid(row=0,column=0,sticky=W,padx=(0,109))

        #running forward
        self.btn = Button(self.frame,image=self.resize1,padx=20,pady=10,compound=RIGHT,    relief="flat",borderwidth=0)
        self.btn.grid(row=0,column=1, sticky=E)

    def step_click(self):
        self.master.withdraw()
        self.step_window = Toplevel()
        self.step_window.title("Steps")
        self.step_window.geometry("450x530")
        self.step_window.resizable(0, 0)
        self.step_window.columnconfigure(0, weight=1)
        self.step_window.columnconfigure(1, weight=1)
        global step_window

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.step_window,image=self.resize_back,padx=10,pady=10,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0, padx=5,sticky=NW)

        self.act_heading = Label(self.step_window,text="Walking",font=("Helvetica", 25))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        # dropdown for timeperiod
        self.options = ["3-Days","Weekly","Month","Yearly"]
        self.clicked = StringVar()
        self.clicked.set("Select Timeperiod")
        self.drop = OptionMenu(self.step_window,self.clicked,*self.options)
        self.drop.grid(row=2,column=0,columnspan=2)

        #graph section
        self.frame_step = LabelFrame(self.step_window,padx=200,pady=100)
        self.frame_step.grid(row=3,column=0,columnspan=2,pady=(10,0))

        self.label_step = Label(self.frame_step,text="Graph")
        self.label_step.grid(row=3,column=0,)


        self.label_step = Label(self.step_window,text="Track Calories you Burnt Today!!",font=("Verdana", 13),fg="red")
        self.label_step.grid(row=4,column=0,columnspan=2,pady=(10,2))

        #distance
        self.distance = Label(self.step_window,text="Distance (Km): ",font=("Verdana", 10))
        self.distance.grid(row=5,column=0,pady=(15,0),padx=(20,5))
        self.distance_entry = Entry(self.step_window,width=35)
        self.distance_entry.grid(row=5,column=1, padx=(0,40), pady=(15,0))

        #time
        self.time = Label(self.step_window,text="Time (Hr): ",font=("Verdana", 10))
        self.time.grid(row=6,column=0,pady=(10,0),padx=(20,5))
        self.time_entry = Entry(self.step_window,width=35)
        self.time_entry.grid(row=6,column=1, padx=(0,40), pady=(15,0))

        #add button
        self.add_btn = Button(self.step_window, text="Add", padx=40, pady=3,font=("Verdana", 10),command=self.add_steps_calories_popup)
        self.add_btn.grid(row=7, column=0, pady=(20, 0), sticky=E, padx=(70, 5)) 

        #show record btn
        self.show_acc = Button(self.step_window, text="Show record", pady=3, padx=30,font=("Verdana", 10),command=self.walking_show_record)
        self.show_acc.grid(row=7, column=1, sticky=W, pady=(20, 0), padx=(5, 0)) 

        self.step_window.mainloop()
    
    def add_steps_calories_popup(self):
        '''when distance and time are entered and add btn is clicked only then:
        1) the data from the form disappers 
        2) message box opens showing calories burnt'''

        try:
            if(self.distance_entry.get()!="" and self.time_entry.get()!="" and 
                   float(self.distance_entry.get()) and float(self.time_entry.get()) and
                   float(self.distance_entry.get()) > 0 and float(self.time_entry.get()) > 0):
                
                #result = fomula
                messagebox.showinfo("Calories Burnt","HURRAY!! You burnt result Calories")
            else:
                messagebox.showerror("Invalid value","Please enter valid distance and time")
        except:
                messagebox.showerror("Invalid value","Please enter valid distance and time")

        self.distance_entry.delete(0, 'end')
        self.time_entry.delete(0,'end')
           
    def walking_show_record(self):

        #step_window.withdraw()
        self.record_walk_window = Toplevel()
        self.record_walk_window.title("Walking Records")
        self.record_walk_window.geometry("350x450")
        self.record_walk_window.resizable(0, 0)
        self.record_walk_window.grid_rowconfigure(0, weight=1)
        self.record_walk_window.grid_columnconfigure(0, weight=1)

        self.back_img = PhotoImage(file=r"images\back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.record_walk_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.record_walk_window,text="Walking Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,20))
    
        self.data = LabelFrame(self.record_walk_window,padx=20,pady=15)
        self.data.grid(row=2,column=0,columnspan=3)
        
        # Create a Canvas widget
        self.canvas = Canvas(self.data)
        self.canvas.grid(row=0, column=0, columnspan=3, sticky= NSEW)

        self.vertical_scrollbar = ttk.Scrollbar(self.data, orient=VERTICAL, command=self.canvas.yview)
        self.vertical_scrollbar.grid(row=0, column=2, sticky=NS)

        self.horizontal_scrollbar = ttk.Scrollbar(self.data, orient=HORIZONTAL, command=self.canvas.xview)
        self.horizontal_scrollbar.grid(row=1, column=0, columnspan=3, sticky=EW)

        self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)

        self.frame = ttk.Frame(self.canvas, height=200, width=100)
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)

        for i in range(20):
            ttk.Label(self.frame, text=f"Label {i}").pack(pady=5)

        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        #update btn
        self.update_btn = Button(self.record_walk_window,text="Update", padx=30, pady=3,font=("Verdana", 10),command=self.update_record_walk)
        self.update_btn.grid(row=3,column=0, pady=(10, 15), padx=(0,20),sticky=E)

        #delete btn
        self.delete_btn = Button(self.record_walk_window,text="Delete", pady=3, padx=30,font=("Verdana", 10),command=self.delete_record_walk)
        self.delete_btn.grid(row=3,column=1,sticky=W, pady=(10, 15), padx=(0,60))
 
        self.record_walk_window.mainloop()

    def delete_record_walk(self):
        self.delete_walk_window = Toplevel()
        self.delete_walk_window.title("Update")
        self.delete_walk_window.geometry("220x200")
        self.delete_walk_window.resizable(0, 0)
        self.step_window.columnconfigure(0, weight=1)
        self.step_window.columnconfigure(1, weight=1)

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.delete_walk_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.delete_walk_window,text="Delete Record",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        self.id = Label(self.delete_walk_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.delete_walk_window,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.delete_walk_window, text="Delete", padx=20, bg="#ff8383",fg="white",pady=3,font=("Verdana", 10))
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.delete_walk_window.mainloop()

    def update_record_walk(self):
        self.update_walk_window = Toplevel()
        self.update_walk_window.title("Update")
        self.update_walk_window.geometry("300x250")
        self.update_walk_window.resizable(0, 0)
        self.step_window.columnconfigure(0, weight=1)
        self.step_window.columnconfigure(1, weight=1)

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.update_walk_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.update_walk_window,text="Update Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        self.id = Label(self.update_walk_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.update_walk_window,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.distance = Label(self.update_walk_window,text="Distance (Km): ",font=("Verdana", 10))
        self.distance.grid(row=3,column=0,pady=(15,0),padx=(20,5))
        self.distance_entry = Entry(self.update_walk_window,width=22)
        self.distance_entry.grid(row=3,column=1, padx=(0,40), pady=(15,0))

        self.time = Label(self.update_walk_window,text="Time (Hr): ",font=("Verdana", 10))
        self.time.grid(row=4,column=0,pady=(10,0),padx=(20,5))
        self.time_entry = Entry(self.update_walk_window,width=22)
        self.time_entry.grid(row=4,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.update_walk_window, text="Update", padx=20, pady=3,font=("Verdana", 10))
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.update_walk_window.mainloop()

root = Tk()
my_gui = Activity(root)
root.mainloop()

