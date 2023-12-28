from tkinter import *
from PIL import ImageTk,Image
from tkinter import PhotoImage
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from tkinter import ttk


root = Tk()
root.title("FitFolio")
icon_image = PhotoImage(file="images/heart.png")
root.iconphoto(True, icon_image) 
root.geometry("450x330")
root.resizable(0, 0) #fixed size of the window

# configuring the rows and columns of the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# on clicking walking button 
def step_click():
    page1.withdraw()
    steps = Toplevel()
    steps.title("Steps")
    steps.geometry("450x530")
    steps.resizable(0, 0)
    steps.columnconfigure(0, weight=1)
    steps.columnconfigure(1, weight=1)

    back_img = PhotoImage(file="images/back_arrow.png")
    resize_back = back_img.subsample(2,2)
    back_btn = Button(steps,image=resize_back,padx=10,pady=10,relief="flat", borderwidth=0)
    back_btn.grid(row=0, column=0, padx=5,sticky=NW)

    act_heading = Label(steps,text="Walking",font=("Helvetica", 25))
    act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

    # dropdown for timeperiod
    options = ["3-Days","Weekly","Month","Yearly"]
    clicked = StringVar()
    clicked.set("Select Timeperiod")
    drop = OptionMenu(steps,clicked,*options)
    drop.grid(row=2,column=0,columnspan=2)

    #graph section
    frame_step = LabelFrame(steps,padx=200,pady=100)
    frame_step.grid(row=3,column=0,columnspan=2,pady=(10,0))

    label_step = Label(frame_step,text="Graph")
    label_step.grid(row=3,column=0,)

    label_step = Label(steps,text="Track Calories you Burnt Today!!",font=("Verdana", 13),fg="red")
    label_step.grid(row=4,column=0,columnspan=2,pady=(10,2))

    #distance
    distance = Label(steps,text="Distance (Km): ",font=("Verdana", 10))
    distance.grid(row=5,column=0,pady=(15,0),padx=(20,5))
    distance_entry = Entry(steps,width=35)
    distance_entry.grid(row=5,column=1, padx=(0,40), pady=(15,0))

    #time
    time = Label(steps,text="Time (Hr): ",font=("Verdana", 10))
    time.grid(row=6,column=0,pady=(10,0),padx=(20,5))
    time_entry = Entry(steps,width=35)
    time_entry.grid(row=6,column=1, padx=(0,40), pady=(15,0))

    #add button
    add_btn = Button(steps, text="Add", padx=40, pady=3,font=("Verdana", 10))
    add_btn.grid(row=7, column=0, pady=(20, 0), sticky=E, padx=(70, 5)) 

    #show record btn
    show_acc = Button(steps, text="Show record", pady=3, padx=30,font=("Verdana", 10))
    show_acc.grid(row=7, column=1, sticky=W, pady=(20, 0), padx=(5, 0)) 


    steps.mainloop()

def activity_page():
    global page1
    page1 = Toplevel()

    page1.title("Activity")
    # page1.geometry("350x350")
    page1.resizable(0, 0)
    page1.columnconfigure(0, weight=1)
    page1.columnconfigure(1, weight=1)

    #back to main page
    back_img = PhotoImage(file="images/back_arrow.png")
    resize_back = back_img.subsample(2,2)
    back_btn = Button(page1,image=resize_back,padx=10,pady=10,relief="flat", borderwidth=0)
    back_btn.grid(row=0, column=0, padx=5,sticky=NW)

    act_heading = Label(page1,text="Activity",font=("Helvetica", 25))
    act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

    # walking 
    frame = LabelFrame(page1,padx=20,pady=10)
    frame.grid(row=2,column=0)

    img = PhotoImage(file="images/walk.png")
    resize = img.subsample(2,2)
    btn = Button(frame,image=resize,text="  Walking ",pady=5,compound=LEFT, font=("Verdana", 13),relief="flat",borderwidth=0,command=step_click)
    btn.grid(row=0,column=0,sticky=W,padx=(0,112))

    img1 = PhotoImage(file="images/forward.png")
    resize1 = img1.subsample(3,3)
    btn_walk = Button(frame,image=resize1,padx=20,pady=10,compound=RIGHT,relief="flat",borderwidth=0,command=step_click)
    btn_walk.grid(row=0,column=1, sticky=E)


    #cycling 
    frame = LabelFrame(page1,padx=20,pady=10)
    frame.grid(row=3,column=0)

    img_cycle = PhotoImage(file="images\cycle.png")
    resize_cycle = img_cycle.subsample(2,2)
    btn = Button(frame,image=resize_cycle,text="  Cycling ",pady=5,compound=LEFT, font=("Verdana", 13),relief="flat",borderwidth=0)
    btn.grid(row=0,column=0,sticky=W,padx=(0,120))

    btn = Button(frame,image=resize1,padx=15,pady=10,compound=RIGHT,relief="flat",borderwidth=0)
    btn.grid(row=0,column=1, sticky=E)

    #workout
    frame = LabelFrame(page1,padx=20,pady=10)
    frame.grid(row=4,column=0)

    img_workout= PhotoImage(file="images\workout.png")
    resize_workout = img_workout.subsample(2,2)
    btn = Button(frame,image=resize_workout,text="  Workout ",pady=5,compound=LEFT, font=("Verdana", 13),relief="flat",borderwidth=0)
    btn.grid(row=0,column=0,sticky=W,padx=(0,109))

    btn = Button(frame,image=resize1,padx=20,pady=10,compound=RIGHT,relief="flat",borderwidth=0)
    btn.grid(row=0,column=1, sticky=E)

    #running
    frame = LabelFrame(page1,padx=20,pady=10)
    frame.grid(row=5,column=0)

    img_running= PhotoImage(file="images/run.png")
    resize_running = img_running.subsample(2,2)
    btn = Button(frame,image=resize_running,text="  Running ",pady=5,compound=LEFT, font=("Verdana", 13),relief="flat",borderwidth=0)
    btn.grid(row=0,column=0,sticky=W,padx=(0,109))

    btn = Button(frame,image=resize1,padx=20,pady=10,compound=RIGHT,relief="flat",borderwidth=0)
    btn.grid(row=0,column=1, sticky=E)

    page1.mainloop()


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
mindful_btn = Button(root, text=" Mindfulness ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5)
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



