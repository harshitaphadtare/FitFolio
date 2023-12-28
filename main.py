from tkinter import *
from PIL import ImageTk,Image
from tkinter import PhotoImage
from ttkthemes import ThemedTk
from tkcalendar import DateEntry

root = Tk()
root.title("FitFolio")
icon_image = PhotoImage(file="images/heart.png")
root.iconphoto(True, icon_image) 
root.geometry("450x330")
root.resizable(0, 0) #fixed size of the window

# configuring the rows and columns of the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

def activity_page():
    page1 = Toplevel()
    page1.title("Activity")
    page1.geometry("300x300")
    page1.resizable(0, 0)
    page1.columnconfigure(0, weight=1)
    page1.columnconfigure(1, weight=1)

    act_heading = Label(page1,text="Activity",font=("Helvetica", 25))
    act_heading.grid(row=0,column=0,columnspan=2,pady=(10,0))

    steps_img = PhotoImage(file="images\walk.png")
    resize_steps = steps_img.subsample(1,1)
    steps_btn = Button(page1,image=resize_steps,padx=10,pady=10,relief="flat", borderwidth=0)
    steps_btn.grid(row=3, column=0, padx=10, pady=(20,10))

    cycle_img = PhotoImage(file="images\cycle.png")
    resize_cycle = cycle_img.subsample(1,1)
    cycle_btn = Button(page1,image=resize_cycle,padx=10,pady=10,relief="flat", borderwidth=0)
    cycle_btn.grid(row=3, column=1, padx=10, pady=(20,10))

    run_img = PhotoImage(file="images/run.png")
    resize_run = run_img.subsample(1,1)
    run_btn = Button(page1,image=resize_run,padx=10,pady=10,relief="flat", borderwidth=0)
    run_btn.grid(row=4, column=0, padx=10, pady=10)

    workout_img = PhotoImage(file="images/workout.png")
    resize_workout = workout_img.subsample(1,1)
    workout_btn = Button(page1,image=resize_steps,padx=10,pady=10,relief="flat", borderwidth=0)
    workout_btn.grid(row=4, column=1, padx=10, pady=10)

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
user_btn = Button(root,image=photo,command=user_click)
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

# sleep button
sleep_image = PhotoImage(file='images/sleep.png')
resized_image = sleep_image.subsample(2, 2)
sleep_btn = Button(root, text=" Sleep ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5)
sleep_btn.image = resized_image
sleep_btn.grid(row=4,column=1,pady=(10, 15),ipadx=25)


root.mainloop()



