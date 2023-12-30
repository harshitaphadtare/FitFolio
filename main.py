from tkinter import *
from PIL import ImageTk,Image
from tkinter import PhotoImage
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import messagebox


root = Tk()
root.title("FitFolio")
icon_image = PhotoImage(file="images/heart.png")
root.iconphoto(True, icon_image) 
root.geometry("450x330")
root.resizable(0, 0) #fixed size of the window
# configuring the rows and columns of the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)


class Mindfulness:
    def __init__(self,master):
        # root.withdraw()
        self.master = master
        self.master.title('Mindfulness')
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
        self.record_walk.title("Records")
        self.record_walk.geometry("350x450")
        self.record_walk.resizable(0, 0)
        self.record_walk.grid_rowconfigure(0, weight=1)
        self.record_walk.grid_columnconfigure(0, weight=1)

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.record_walk,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.record_walk,text="Mindfulness Records",font=("Helvetica", 15))
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

def mindful_page():
    root.withdraw()
    mindful_window = Toplevel(root)
    app = Mindfulness(mindful_window) 

# Activity class
class Activity:
    def __init__(self, master):
        self.master = master
        self.master.title('Activity')
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        self.back_img = PhotoImage(file="images/back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)

        self.back_btn = Button(self.master,image=self.resize_back,padx=10,pady=10,relief="flat", borderwidth=0)
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

        self.step_window.withdraw()
        
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

def activity_page():
    root.withdraw()
    activity_window = Toplevel(root)
    app = Activity(activity_window)
#signup page
def create_acc_click():
    top.withdraw()
    create_acc_window = Toplevel()
    create_acc_window.title("Sign Up")
    create_acc_window.geometry("400x280")
    create_acc_window.resizable(0, 0)
    create_acc_window.columnconfigure(0, weight=1)
    create_acc_window.columnconfigure(1, weight=1)

    # Add content to the new window
    label = Label(create_acc_window,text="Start your Journey with",font=("Helvetica", 10))
    label.grid(row=1,column=0,columnspan=2,pady=(5,0))
    label1 = Label(create_acc_window,text="FitFolio!!",font=("Helvetica", 15))
    label1.grid(row=2,column=0,columnspan=2,pady=(0,10))
    
    #fullname
    fullname = Label(create_acc_window,text="Fullname: ")
    fullname.grid(row=3,column=0)
    fullname_entry = Entry(create_acc_window,width=30)
    fullname_entry.grid(row=3,column=1,sticky=W, padx=5, pady=5)

    #dob
    dob = Label(create_acc_window,text="DOB: ")
    dob.grid(row=4,column=0)  # to get value in dob_entry: dob_entry.get_date()
    dob_entry = DateEntry(create_acc_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    dob_entry.grid(row=4,column=1,sticky=W, padx=5, pady=5)

    #username
    username = Label(create_acc_window,text="Username: ")
    username.grid(row=5,column=0)
    username_entry = Entry(create_acc_window,width=30)
    username_entry.grid(row=5,column=1,sticky=W, padx=5, pady=5)

    #password
    password = Label(create_acc_window,text="Password: ")
    password.grid(row=6,column=0)
    password_entry = Entry(create_acc_window,width=30, show='*')
    password_entry.grid(row=6,column=1,sticky=W, padx=5, pady=5)

    #gender
    gender_dalo = Label(create_acc_window,text="Gender: ")
    gender_dalo.grid(row=7,column=0)

    gender_frame = Frame(create_acc_window)
    gender_frame.grid(row=7, column=1, columnspan=2, sticky=W, pady=5)
    
    options= [["Male","M"],["Female","F"],["Other","Oth"]]
    clicked = StringVar()
    clicked.set("None")

    for option in options:
        r = Radiobutton(gender_frame, text=option[0], value=option[1], variable=clicked).pack(side='left', padx=5)
    
    signup_btn = Button(create_acc_window,text="Sign up",padx=10,pady=5)
    signup_btn.grid(row=8,column=0,columnspan=2, padx=5, pady=10)

# login page opens when user button is clicked
def user_click():
   global top
   top = Toplevel()
   top.title("Login")
   top.geometry("300x200")
   top.resizable(0, 0)
   top.columnconfigure(0, weight=1)
   top.columnconfigure(1, weight=1)

   label_top = Label(top,text="Welcome to FitFolio!!",font=("Helvetica", 15),pady=20)
   label_top.grid(row=1,column=0,columnspan=2)

   #username
   username = Label(top,text="Username: ")
   username.grid(row=2,column=0)
   username_entry = Entry(top,width=30)
   username_entry.grid(row=2,column=1,sticky=W, padx=5, pady=5)

   #password
   password = Label(top,text="Password: ")
   password.grid(row=3,column=0)
   password_entry = Entry(top,width=30, show='*')
   password_entry.grid(row=3,column=1,sticky=W, padx=5, pady=5)

   #login button
   login_btn = Button(top,text="Login",command=top.destroy,padx=10,pady=3)
   login_btn.grid(row=4,column=0,columnspan=2,pady=(10,0),padx=20)

   #create button
   create_acc_text = "Create Account"
   create_acc = Button(top,text=create_acc_text,pady=3,relief="flat", borderwidth=0,underline=len(create_acc_text),command=create_acc_click)
   create_acc.grid(row=5,columnspan=2,column=0)


########## main page
#user button
image = Image.open("images/user.png")  
photo = ImageTk.PhotoImage(image)
user_btn = Button(root,image=photo,command=user_click,relief="flat", borderwidth=0)
user_btn.grid(row=0,column=1, sticky=E, padx=5, pady=5,ipadx=10,ipady=10)
user_btn.image = photo # Setting the image as a reference to prevent it from being garbage collected

label = Label(root,text="Track Yourself Now!!", font=("Helvetica", 20),pady=10)
label.grid(row=1,column=0,columnspan=2)


# activity button
activity_image = PhotoImage(file='images/activity.png')
resized_image = activity_image.subsample(2, 2)
activity_btn = Button(root, text=" Activity ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5,command=activity_page)
activity_btn.image = resized_image
activity_btn.grid(row=3,column=0, pady=(20,10),ipadx=15)

# mindfullness button
mindful_image = PhotoImage(file='images/mindfulness.png')
resized_image = mindful_image.subsample(2, 2)
mindful_btn = Button(root, text=" Mindfulness ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5,command=mindful_page)
mindful_btn.image = resized_image
mindful_btn.grid(row=3,column=1,pady=(20, 15))

# body button
body_image = PhotoImage(file='images/body.png')
resized_image = body_image.subsample(2, 2)
body_btn = Button(root, text=" Body ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5)
body_btn.image = resized_image
body_btn.grid(row=4,column=0,pady=(10, 15),ipadx=25)


sleep_image = PhotoImage(file='images/sleep.png')
resized_image = sleep_image.subsample(2, 2)
sleep_btn = Button(root, text=" Sleep ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5) 
sleep_btn.image = resized_image
sleep_btn.grid(row=4,column=1,pady=(10, 15),ipadx=25)


root.mainloop()



