from tkinter import *
from PIL import ImageTk,Image
from tkinter import PhotoImage
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import messagebox
from tktimepicker import AnalogPicker, AnalogThemes, constants 
import mysql.connector
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    port = 3306,
    password = "Harshita@2023",
    database= "fitfolio"
)

mycur = db.cursor()

root = Tk()
root.title("FitFolio Login")
icon_image = PhotoImage(file="images/heart.png")
root.iconphoto(True, icon_image) 
root.geometry("300x200")
root.resizable(0, 0) #fixed size of the window
# configuring the rows and columns of the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)


# sleep page
class Sleep:
    back_img = PhotoImage(file=r"images\back_arrow.png")
    resize_back = back_img.subsample(2,2)

    def __init__(self, master):
        
        global bed_in_entry
        global bed_out_entry

        root.withdraw()
        self.sleep_window = master
        self.sleep_window.title("Sleep")
        self.sleep_window.geometry("450x550")
        self.sleep_window.resizable(0, 0)
        self.sleep_window.columnconfigure(0, weight=1)
        self.sleep_window.columnconfigure(1, weight=1)

        self.back_btn = Button(self.sleep_window,image=self.resize_back,padx=10,pady=10,relief="flat", borderwidth=0,command=lambda:[top.deiconify(),self.sleep_window.destroy()])
        self.back_btn.grid(row=0, column=0, padx=5,sticky=NW)

        self.act_heading = Label(self.sleep_window,text="Sleep Tracking",font=("Helvetica", 25))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        # dropdown for timeperiod
        self.options = ["Daily","Weekly","Monthly","Yearly"]
        self.clicked = StringVar()
        self.clicked.set(self.options[0])
        self.drop = OptionMenu(self.sleep_window,self.clicked,*self.options)
        self.drop.grid(row=2,column=0,columnspan=2)

        #graph section
        self.frame_graph = LabelFrame(self.sleep_window,padx=200,pady=100)
        self.frame_graph.grid(row=3,column=0,columnspan=2,pady=(10,0))

        self.label_graph = Label(self.frame_graph,text="Graph")
        self.label_graph.grid(row=3,column=0,)

        self.act_heading = Label(self.sleep_window, text="Enter your sleep data for the day (24Hrs)",font=("Verdana", 13))
        self.act_heading.grid(row=4, column=0, columnspan=2, pady=(10,0))

        #bed in
        self.bed_in = Label(self.sleep_window,text="Bed in:",font=("Verdana", 10))
        self.bed_in.grid(row=5,column=0,pady=(15,0),padx=(20,5))
        self.bed_in_entry = Button(self.sleep_window, text="Get Time",relief=GROOVE,width=20 ,command=lambda:self.get_time(self.bed_in_entry))
        self.bed_in_entry.grid(row=5,column=1, padx=(0,80), pady=(15,0), sticky=W)

        #bed out
        self.bed_out = Label(self.sleep_window,text="Bed out:",font=("Verdana", 10))
        self.bed_out.grid(row=6,column=0,pady=(10,0),padx=(20,5))
        self.bed_out_entry = Button(self.sleep_window, text="Get Time",relief=GROOVE,width=20 ,command=lambda:self.get_time(self.bed_out_entry))
        self.bed_out_entry.grid(row=6,column=1, padx=(0,80), pady=(15,0), sticky=W)

        
        self.add_btn = Button(self.sleep_window, text="ADD", padx=40, pady=3,font=("Verdana", 10), command=self.add_sleep_data)
        self.add_btn.grid(row=7, column=0, sticky=W,pady=(20, 0), padx=(70, 5))

        self.show_acc = Button(self.sleep_window, text="Show record", pady=3, padx=30,font=("Verdana", 10),command=self.sleep_show_record)
        self.show_acc.grid(row=7, column=1,sticky=W, pady=(20, 0), padx=(5, 0)) 

    def add_sleep_data(self):
        bed_in_str = self.bed_in_entry.cget("text")
        bed_out_str = self.bed_out_entry.cget("text")

        if bed_in_str != "Get Time" and bed_out_str != "Get Time":
            bed_in_time = datetime.strptime(bed_in_str, "%H:%M")
            bed_out_time = datetime.strptime(bed_out_str, "%H:%M")

            # Check if bed_out_time is earlier than bed_in_time
            if bed_out_time < bed_in_time:
                bed_out_time += timedelta(days=1)  # Assuming sleep crosses midnight

            sleep_duration = bed_out_time - bed_in_time

            total_hours, remainder = divmod(sleep_duration.total_seconds(), 3600)
            total_minutes = remainder // 60

            # Format the total hours and minutes
            total_hrs = f"{int(total_hours):02}:{int(total_minutes):02}"

            sql = "INSERT INTO sleep (username, bed_in, bed_out, total_hrs, date) VALUES (%s, %s, %s, %s, CURDATE())"
            val = (username_login, bed_in_str, bed_out_str, total_hrs)
            mycur.execute(sql, val)
            db.commit()

            messagebox.showinfo("Record", "Record is added successfully!")

            self.bed_in_entry.configure(text="Get Time")  # Reset the button text
            self.bed_out_entry.configure(text="Get Time")  # Reset the button text

        else:
            messagebox.showerror("Incorrect time", "Please enter both bed_in and bed_out times")

    def populate_treeview_sleep(self, username):

        sql = "SELECT id,date, bed_in, bed_out, total_hrs FROM sleep WHERE username = %s"
        val = (username,)
        mycur.execute(sql, val)
        rows = mycur.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def sleep_show_record(self):
        self.sleep_window.withdraw()
        self.record_sleep_window = Toplevel()
        self.record_sleep_window.title("Sleep")
        self.record_sleep_window.geometry("350x450")
        self.record_sleep_window.resizable(0, 0)
        self.record_sleep_window.grid_rowconfigure(0, weight=1)
        self.record_sleep_window.grid_columnconfigure(0, weight=1)

        self.back_btn = Button(self.record_sleep_window,image=self.resize_back,command=lambda: [self.record_sleep_window.destroy(),self.sleep_window.deiconify()],padx=10,pady=5,relief="flat", borderwidth=0)
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.record_sleep_window,text="Sleep Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,20))
    
        self.data = LabelFrame(self.record_sleep_window,padx=20,pady=15)
        self.data.grid(row=2,column=0,columnspan=3)
        
        self.tree = ttk.Treeview(self.data, columns=("ID","date", "Bed In", "Bed Out","Total hrs"), height=13)
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("date", text="date")
        self.tree.heading("Bed In", text="Bed In")
        self.tree.heading("Bed Out", text="Bed Out")
        self.tree.heading("Total hrs", text="Total hrs")

        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("ID", width=20)
        self.tree.column("date", width=100)
        self.tree.column("Bed In", width=100)
        self.tree.column("Bed Out", width=100)
        self.tree.column("Total hrs", width=100)
        
        vsb = ttk.Scrollbar(self.data, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill=BOTH)
        vsb.pack(side="right", fill=Y)

        self.populate_treeview_sleep(username_login)

        self.update_btn = Button(self.record_sleep_window,text="Update", padx=30, pady=3,font=("Verdana", 10),command=self.update_record_sleep)
        self.update_btn.grid(row=3,column=0, pady=(10, 15), padx=(0,20),sticky=E)

        self.delete_btn = Button(self.record_sleep_window,text="Delete", pady=3, padx=30,font=("Verdana", 10),command=self.delete_record_sleep)
        self.delete_btn.grid(row=3,column=1,sticky=W, pady=(10, 15), padx=(0,60))
 
        self.record_sleep_window.mainloop()

    def update_sleep_sql(self):
        self.bed_in = self.bed_in_entry.cget("text")
        self.bed_out = self.bed_out_entry.cget("text")
        self.id_value = self.id_entry.get()


        if self.bed_in != "Get Time" and self.bed_out != "Get Time":
            bed_in_time = datetime.strptime(self.bed_in, "%H:%M")
            bed_out_time = datetime.strptime(self.bed_out, "%H:%M")

            if bed_out_time < bed_in_time:
                bed_out_time += timedelta(days=1)  

                sleep_duration = bed_out_time - bed_in_time

                total_hours, remainder = divmod(sleep_duration.total_seconds(), 3600)
                total_minutes = remainder // 60

                total_hrs = f"{int(total_hours):02}:{int(total_minutes):02}"
               
                self.update_query = """
                UPDATE sleep
                SET bed_in = %s, bed_out = %s, total_hrs=%s
                WHERE id = %s
                """
                mycur.execute(self.update_query, (self.bed_in, self.bed_out,total_hrs,self.id_value))

                messagebox.showinfo("Update Record","Record is Updated Succesfully!")
                self.update_sleep_window.withdraw()
                db.commit()

                self.bed_in_entry.configure(text="Get Time")  
                self.bed_out_entry.configure(text="Get Time")  


        else:
            messagebox.showerror("Incorrect time", "Please enter both bed_in and bed_out times")
            self.bed_in_entry.configure(text="Get Time")  
            self.bed_out_entry.configure(text="Get Time")  

    def update_record_sleep(self):
        global id_entry
        global bed_in_entry
        global bed_out_entry
        self.update_sleep_window = Toplevel()
        self.update_sleep_window.title("Update")
        self.update_sleep_window.geometry("300x250")
        self.update_sleep_window.resizable(0, 0)

        self.update_sleep_window.columnconfigure(0, weight=1)
        self.update_sleep_window.columnconfigure(1, weight=1)

        # self.back_btn = Button(self.update_sleep_window,image=self.resize_back,command=lambda:self.update_sleep_window.destroy(),padx=10,pady=5,relief="flat", borderwidth=0)
        # self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.update_sleep_window,text="Update Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        self.id = Label(self.update_sleep_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.update_sleep_window,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        #bed in
        self.bed_in = Label(self.update_sleep_window,text="Bed in:",font=("Verdana", 10))
        self.bed_in.grid(row=3,column=0,pady=(15,0),padx=(20,5))
        self.bed_in_entry = Button(self.update_sleep_window, text="Get Time",relief=GROOVE,width=18 ,command=lambda:self.get_time(self.bed_in_entry))
        self.bed_in_entry.grid(row=3,column=1, padx=(0,40), pady=(15,0))

        #bed out
        self.bed_out = Label(self.update_sleep_window,text="Bed out:",font=("Verdana", 10))
        self.bed_out.grid(row=4,column=0,pady=(10,0),padx=(20,5))
        self.bed_out_entry = Button(self.update_sleep_window, text="Get Time",relief=GROOVE,width=18 ,command=lambda:self.get_time(self.bed_out_entry))
        self.bed_out_entry.grid(row=4,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.update_sleep_window, text="Update", padx=20, pady=3,font=("Verdana", 10),command=self.update_sleep_sql)
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.update_sleep_window.mainloop()

    def delete_sleep_db(self):
        self.ans = messagebox.askyesno("Delete Record", "Are you sure you want to Delete Your Record?? ")
        if self.ans: 
            self.sql = "DELETE FROM sleep WHERE username = %s AND id = %s"
            self.val = (username_login, self.id_entry.get())

            try:
                mycur.execute(self.sql, self.val)
                affected_rows = mycur.rowcount

                if affected_rows > 0:
                    db.commit()
                    messagebox.showinfo("Delete Record", "Successfully Deleted the Record!")
                    self.id_entry.delete(0, END)
                    self.delete_sleep_window.withdraw()
                else:
                    messagebox.showinfo("Delete Record", "Record with the specified ID not found!")

            except mysql.connector.Error as err:
                messagebox.showinfo("Delete Record", f"Error: {err}")

        else:
            self.delete_sleep_window.withdraw()

    def delete_record_sleep(self):
        global id_entry
        global delete_sleep_window

        self.delete_sleep_window = Toplevel()
        self.delete_sleep_window.title("Update")
        self.delete_sleep_window.geometry("220x200")
        self.delete_sleep_window.resizable(0, 0)

        self.delete_sleep_window.columnconfigure(0, weight=1)
        self.delete_sleep_window.columnconfigure(1, weight=1)

        # self.back_btn = Button(self.delete_sleep_window,image=self.resize_back,command=lambda:self.delete_sleep_window.destroy(),padx=10,pady=5,relief="flat", borderwidth=0)
        # self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.delete_sleep_window,text="Delete Record",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

        self.id = Label(self.delete_sleep_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.delete_sleep_window,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.delete_btn = Button(self.delete_sleep_window, text="Delete", padx=20, bg="#ff8383",fg="white",pady=3,font=("Verdana", 10),command=self.delete_sleep_db)
        self.delete_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.delete_sleep_window.mainloop()

    #update time button
    def updateTime(self,time,btn,top):
        top.destroy()
        btn.configure(text="{}:{}".format(*time)) 

    #clock functionality
    def get_time(self,btn):

        self.top = Toplevel()

        self.time_picker = AnalogPicker(self.top, type=constants.HOURS24)
        self.time_picker.pack(expand=True, fill="both")

        self.theme = AnalogThemes(self.time_picker)
            # theme.setDracula()
        self.theme.setNavyBlue()
            #theme.setPurple()
        self.ok_btn = Button(self.top, text="ok", command=lambda: self.updateTime(self.time_picker.time(),btn, self.top))
        self.ok_btn.pack()
        
def sleep_page():
    top.withdraw()
    sleep_window = Toplevel(root)
    app = Sleep(sleep_window)


#Body measurements
class Body_Measurement:

    def __init__(self, master):
        top.withdraw()
        self.bodym_window = master
        self.bodym_window.title("Body Measurements")
        self.bodym_window.geometry("450x610")
        self.bodym_window.resizable(0, 0)
        self.bodym_window.columnconfigure(0, weight=1)
        self.bodym_window.columnconfigure(1, weight=1)

        self.back_img = PhotoImage(file=r"images\back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.bodym_window,image=self.resize_back,padx=10,pady=10,relief="flat", borderwidth=0,command=lambda:[top.deiconify(),self.bodym_window.destroy()])
        self.back_btn.grid(row=0, column=0, padx=5,sticky=NW)

        self.act_heading = Label(self.bodym_window,text="Body Measurements",font=("Helvetica", 25))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        # dropdown for timeperiod
        self.options = ["3-Days","Weekly","Month","Yearly"]
        self.clicked = StringVar()
        self.clicked.set(self.options[0])
        self.drop = OptionMenu(self.bodym_window,self.clicked,*self.options)
        self.drop.grid(row=2,column=0,columnspan=2)

        #graph section
        self.frame_graph = LabelFrame(self.bodym_window,padx=200,pady=100)
        self.frame_graph.grid(row=3,column=0,columnspan=2,pady=(10,0))

        self.label_graph = Label(self.frame_graph,text="Graph")
        self.label_graph.grid(row=3,column=0,)


        self.label_calc = Label(self.bodym_window,text="Calculate your BMI now!!",font=("Verdana", 13),fg="red")
        self.label_calc.grid(row=4,column=0,columnspan=2,pady=(10,2))

        
        self.category_text = "BMI Categories:\nUnderweight = <18.5\nNormal weight = 18.5 to 24.9\nOverweight = 25 to 29.9\nObesity = BMI of 30 or greater"
        self.category_label = Label(self.bodym_window, text=self.category_text, font=("Verdana", 10), anchor=W, justify=LEFT)
        self.category_label.grid(row=5, column=0, columnspan=2)

        #height
        self.height = Label(self.bodym_window,text="Height (feet): ",font=("Verdana", 10))
        self.height.grid(row=6,column=0,pady=(15,0),padx=(20,5))
        self.height_entry = Entry(self.bodym_window,width=35)
        self.height_entry.grid(row=6,column=1, padx=(0,40), pady=(15,0))

        #weight
        self.weight = Label(self.bodym_window,text="Weight (Kg): ",font=("Verdana", 10))
        self.weight.grid(row=7,column=0,pady=(10,0),padx=(20,5))
        self.weight_entry = Entry(self.bodym_window,width=35)
        self.weight_entry.grid(row=7,column=1, padx=(0,40), pady=(15,0))

        #add button
        self.calc_btn = Button(self.bodym_window, text="Calculate", padx=40, pady=3,font=("Verdana", 10),command=self.bmi_popup)
        self.calc_btn.grid(row=8, column=0, sticky=W,pady=(20, 0), padx=(70, 5)) 

        #show record btn
        self.show_acc = Button(self.bodym_window, text="Show record", pady=3, padx=30,font=("Verdana", 10),command=self.body_show_record)
        self.show_acc.grid(row=8, column=1,sticky=W, pady=(20, 0), padx=(5, 0)) 

        self.bodym_window.mainloop()
    
    def bmi_popup(self):

        self.height = (float(self.height_entry.get()))*0.3048
        self.weight = float(self.weight_entry.get())

        if(self.height_entry.get()!="" and self.weight_entry.get()!="" and 
            float(self.height_entry.get()) and float(self.weight_entry.get()) and
            float(self.height_entry.get()) > 0 and float(self.weight_entry.get()) > 0):
            
            self.bmi = self.weight/(self.height**2)

            if self.bmi < 18.5:
                self.status = "Underweight"
            elif  self.bmi >= 18.5 and self.bmi <= 25:
                self.status = "Normal weight"
            elif  self.bmi > 25 and self.bmi <= 30:
                self.status = "Overweight"
            else:
                self.status = "Obesity"
            
            self.add = messagebox.askquestion("BMI",f'{self.status} !!\nYour BMI is {"%.2f"%self.bmi}.\nDo you want to add this data?')

            if self.add == 'yes':
                sql = "INSERT INTO bmi (username,height,weight,bmi,status,date) VALUES (%s,%s, %s, %s,%s,CURDATE())"
                val = (username_login,self.height,self.weight,self.bmi,self.status)
                mycur.execute(sql, val)
                messagebox.showinfo("Record","Record is added Succesfully!")
                db.commit()
                self.height_entry.delete(0, 'end')
                self.weight_entry.delete(0,'end')
        else:
            messagebox.showerror("Invalid value","Please enter valid height and weight")
            self.height_entry.delete(0, 'end')
            self.weight_entry.delete(0,'end')
        

    def populate_treeview_mind(self, username):
        sql = "SELECT id, date, height, weight,bmi,status FROM bmi WHERE username = %s"
        val = (username,)
        mycur.execute(sql, val)
        rows = mycur.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

    
    def body_show_record(self):

        self.bodym_window.withdraw()
        self.record_body_window = Toplevel()
        self.record_body_window.title("BMI Records")
        self.record_body_window.geometry("350x450")
        self.record_body_window.resizable(0, 0)
        self.record_body_window.grid_rowconfigure(0, weight=1)
        self.record_body_window.grid_columnconfigure(0, weight=1)

        self.back_btn = Button(self.record_body_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0,command=lambda:[self.bodym_window.deiconify(),self.record_body_window.destroy()])
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.record_body_window,text="BMI Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,20))
    
        self.data = LabelFrame(self.record_body_window,padx=20,pady=15)
        self.data.grid(row=2,column=0,columnspan=3)
        
        # Create a Treeview widget
        self.tree = ttk.Treeview(self.data, columns=("ID", "Date", "height","weight","bmi","status"), height=13)
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("height", text="height")
        self.tree.heading("weight", text="weight")
        self.tree.heading("bmi", text="bmi")
        self.tree.heading("status", text="status")

        # Set column widths
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=70)
        self.tree.column("height", width=70)
        self.tree.column("weight", width=70)
        self.tree.column("bmi", width=70)
        self.tree.column("status", width=100)
        
        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(self.data, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill=BOTH)
        vsb.pack(side="right", fill=Y)

        # Call the populate_treeview method
        self.populate_treeview_mind(username_login)
        self.update_btn = Button(self.record_body_window,text="Update", padx=30, pady=3,font=("Verdana", 10),command=self.update_record_body)
        self.update_btn.grid(row=3,column=0, pady=(10, 15), padx=(0,20),sticky=E)

        self.delete_btn = Button(self.record_body_window,text="Delete", pady=3, padx=30,font=("Verdana", 10),command=self.delete_record_body)
        self.delete_btn.grid(row=3,column=1,sticky=W, pady=(10, 15), padx=(0,60))
 
        self.record_body_window.mainloop()


    def update_sql_body(self):

        self.height = (float(self.height_entry_update.get()))*0.3048
        self.id_value = self.id_entry_update.get()
        self.weight = float(self.weight_entry_update.get())
    

        if (self.height!="" and self.weight!="" and self.id_value!="" and float(self.height) > 0 and float(self.weight) > 0):
                
            self.bmi = self.weight/(self.height**2)

            if self.bmi < 18.5:
                self.status = "Underweight"
            elif  self.bmi >= 18.5 and self.bmi <= 25:
                self.status = "Normal weight"
            elif  self.bmi > 25 and self.bmi <= 30:
                self.status = "Overweight"
            else:
                self.status = "Obesity"
            
            self.update_query = """
            UPDATE bmi
            SET height = %s, weight = %s, bmi=%s, status=%s
            WHERE id = %s
            """
        
            mycur.execute(self.update_query, (self.height, self.weight,self.bmi,self.status,self.id_value))

            messagebox.showinfo("Update Record","Record is Updated Succesfully!")
            self.update_body_window.withdraw()
            db.commit()

            self.height_entry_update.delete(0,END)
            self.weight_entry_update.delete(0,END)
            self.id_entry_update.delete(0,END)


        else:
            messagebox.showerror("Invalid value","Please enter valid height and weight")
            self.height_entry_update.delete(0,END)
            self.weight_entry_update.delete(0,END)
            self.id_entry_update.delete(0,END)


    def update_record_body(self):

        global height_entry_update
        global id_entry_update
        global weight_entry_update
        global update_body_window

        self.update_body_window = Toplevel()
        self.update_body_window.title("Update")
        self.update_body_window.geometry("300x250")
        self.update_body_window.resizable(0, 0)

        self.update_body_window.columnconfigure(0, weight=1)
        self.update_body_window.columnconfigure(1, weight=1)

        # self.back_btn = Button(self.update_body_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        # self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.update_body_window,text="Update Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

        self.id = Label(self.update_body_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry_update = Entry(self.update_body_window,width=22)
        self.id_entry_update.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.height = Label(self.update_body_window,text="Height (feet): ",font=("Verdana", 10))
        self.height.grid(row=3,column=0,pady=(15,0),padx=(20,5))
        self.height_entry_update = Entry(self.update_body_window,width=22)
        self.height_entry_update.grid(row=3,column=1, padx=(0,40), pady=(15,0))

        self.weight = Label(self.update_body_window,text="Weight (Kg): ",font=("Verdana", 10))
        self.weight.grid(row=4,column=0,pady=(10,0),padx=(20,5))
        self.weight_entry_update = Entry(self.update_body_window,width=22)
        self.weight_entry_update.grid(row=4,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.update_body_window, text="Update", padx=20, pady=3,font=("Verdana", 10),command=self.update_sql_body)
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.update_body_window.mainloop()

    
    def delete_sql_bmi(self):
        self.ans = messagebox.askyesno("Delete Record", "Are you sure you want to Delete Your Record?? ")
        if self.ans: 
            self.sql = "DELETE FROM bmi WHERE username = %s AND id = %s"
            self.val = (username_login, self.id_entry.get())

            try:
                mycur.execute(self.sql, self.val)
                affected_rows = mycur.rowcount

                if affected_rows > 0:
                    db.commit()
                    messagebox.showinfo("Delete Record", "Successfully Deleted the Record!")
                    self.id_entry.delete(0, END)
                    self.delete_body_window.withdraw()
                else:
                    messagebox.showinfo("Delete Record", "Record with the specified ID not found!")

            except mysql.connector.Error as err:
                messagebox.showinfo("Delete Record", f"Error: {err}")

        else:
            self.delete_body_window.withdraw()

    def delete_record_body(self):

        global id_entry
        global delete_body_window

        self.delete_body_window = Toplevel()
        self.delete_body_window.title("Update")
        self.delete_body_window.geometry("220x200")
        self.delete_body_window.resizable(0, 0)

        self.delete_body_window.columnconfigure(0, weight=1)
        self.delete_body_window.columnconfigure(1, weight=1)

        # self.back_btn = Button(self.delete_body_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0)
        # self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.delete_body_window,text="Delete Record",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

        self.id = Label(self.delete_body_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.delete_body_window,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.delete_body_window, text="Delete", padx=20, bg="#ff8383",fg="white",pady=3,font=("Verdana", 10),command=self.delete_sql_bmi)
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.delete_body_window.mainloop()

def body_page():
    top.withdraw()
    body_window = Toplevel(root)
    app = Body_Measurement(body_window)

class Mindfulness:
    
    def __init__(self,master):

        global clicked  
        global time_entry_mind 

        top.withdraw()

        self.master = master
        self.master.title('Mindfulness')
        self.master.geometry("450x530")
        self.master.resizable(0, 0)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        #back button
        self.back_img_mind = PhotoImage(file="images/back_arrow.png")
        self.resize_back_mind = self.back_img_mind.subsample(2,2)

        self.back_btn_mind = Button(self.master,image=self.resize_back_mind,padx=10,pady=10,relief="flat", borderwidth=0,command=lambda:[top.deiconify(),self.master.destroy()])
        self.back_btn_mind.grid(row=0, column=0, padx=5,sticky=NW)

        #title
        self.mind_heading = Label(master,text="Mindfulness",font=("Helvetica", 25))
        self.mind_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        #drop down for graph
        self.options = ["3-Days","Weekly","Month","Yearly"]
        self.clicked = StringVar()
        self.clicked.set(self.options[0])
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
        self.time_entry_mind = Entry(master,width=22)
        self.time_entry_mind.grid(row=6,column=1,padx=(0,100), pady=(10,0),sticky=W)
        
        #add btn
        add_btn = Button(master, text="Add", padx=40, pady=3,font=("Verdana", 10),command=self.add_btn_mind)
        add_btn.grid(row=7, column=0, pady=(15, 0), sticky=E, padx=(70, 20)) 

        #show record btn
        show_acc = Button(master, text="Show record", pady=3, padx=30,font=("Verdana", 10),command=self.show_btn_mind)
        show_acc.grid(row=7, column=1, sticky=W, pady=(15, 0)) 
        
    def add_btn_mind(self):
        act = self.clicked.get()
        time = self.time_entry_mind.get()

        if (act!="" and time!="" and act!=int and float(time) > 0):
            time = float(self.time_entry_mind.get())

            sql = "INSERT INTO mindfulness (username,date,time,activity) VALUES (%s,CURDATE(),%s, %s)"
            val = (username_login,time,act)
            mycur.execute(sql, val)
            messagebox.showinfo("Record","Record is added Succesfully!")
            db.commit()

            self.time_entry_mind.delete(0,END)
            self.clicked.set(self.options[0])

        else:
            messagebox.showerror("Invalid value","Please enter valid data")
            self.time_entry_mind.delete(0,END)
            self.clicked.set(self.options[0])

    def populate_treeview_mind(self, username):
        sql = "SELECT id, date, time, activity FROM mindfulness WHERE username = %s"
        val = (username,)
        mycur.execute(sql, val)
        rows = mycur.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def show_btn_mind(self):
        self.master.withdraw()
        global record_mind_window 
        self.record_mind_window = Toplevel()
        self.record_mind_window.title("Records")
        self.record_mind_window.geometry("350x450")
        self.record_mind_window.resizable(0, 0)
        self.record_mind_window.grid_rowconfigure(0, weight=1)
        self.record_mind_window.grid_columnconfigure(0, weight=1)

        self.back_img = PhotoImage(file=r"images\back_arrow.png")
        self.resize_back = self.back_img.subsample(2,2)
        self.back_btn = Button(self.record_mind_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0,command=lambda:[self.record_mind_window.destroy(),self.master.deiconify()])
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.record_mind_window,text="Mindfulness Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,20))
    
        self.data = LabelFrame(self.record_mind_window,padx=20,pady=15)
        self.data.grid(row=2,column=0,columnspan=3)
        
        # Create a Treeview widget
        self.tree = ttk.Treeview(self.data, columns=("ID", "Date", "Time","Activity"), height=13)
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Activity", text="Activity")

        # Set column widths
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Time", width=100)
        self.tree.column("Activity", width=100)
        
        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(self.data, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill=BOTH)
        vsb.pack(side="right", fill=Y)

        # Call the populate_treeview method
        self.populate_treeview_mind(username_login)

        #update btn
        self.update_btn = Button(self.record_mind_window,text="Update", padx=30, pady=3,font=("Verdana", 10),command=self.update_record_mind)
        self.update_btn.grid(row=3,column=0, pady=(10, 15), padx=(0,20),sticky=E)

        #delete btn
        self.delete_btn = Button(self.record_mind_window,text="Delete", pady=3, padx=30,font=("Verdana", 10),command=self.delete_record_mind)
        self.delete_btn.grid(row=3,column=1,sticky=W, pady=(10, 15), padx=(0,60))
 
        self.record_mind_window.mainloop()
    
    def delete_sql_mind(self):
        self.ans = messagebox.askyesno("Delete Record", "Are you sure you want to Delete Your Record?? ")
        if self.ans: 
            self.sql = "DELETE FROM mindfulness WHERE username = %s AND id = %s"
            self.val = (username_login, self.id_entry.get())

            try:
                mycur.execute(self.sql, self.val)
                affected_rows = mycur.rowcount

                if affected_rows > 0:
                    db.commit()
                    messagebox.showinfo("Delete Record", "Successfully Deleted the Record!")
                    self.id_entry.delete(0, END)
                    self.delete_mind.withdraw()
                else:
                    messagebox.showinfo("Delete Record", "Record with the specified ID not found!")

            except mysql.connector.Error as err:
                messagebox.showinfo("Delete Record", f"Error: {err}")

        else:
            self.delete_mind.withdraw()

    def delete_record_mind(self):

        global id_entry
        global delete_mind

        self.delete_mind = Toplevel()
        self.delete_mind.title("Delete")
        self.delete_mind.geometry("220x200")
        self.delete_mind.resizable(0, 0)
        self.delete_mind.columnconfigure(0, weight=1)
        self.delete_mind.columnconfigure(1, weight=1)

        self.act_heading = Label(self.delete_mind,text="Delete Record",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

        self.id = Label(self.delete_mind,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.delete_mind,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.delete_mind, text="Delete", padx=20, bg="#ff8383",fg="white",pady=3,font=("Verdana", 10),command=self.delete_sql_mind)
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.delete_mind.mainloop()
    
    def update_sql_mind(self):
        self.act = self.clicked.get()
        self.time = self.time_entry.get()
        self.id_value = self.id_entry.get()


        if (self.act!="" and self.time!="" and self.act!=int and float(self.time) > 0):
            self.time = float(self.time_entry.get())

            self.update_query = """
            UPDATE mindfulness
            SET activity = %s, time = %s
            WHERE id = %s
            """
        
            mycur.execute(self.update_query, (self.act, self.time,self.id_value))

            messagebox.showinfo("Update Record","Record is Updated Succesfully!")
            self.update_walk.withdraw()

            db.commit()

            self.id_entry.delete(0,END)
            self.time_entry.delete(0,END)
            self.clicked.set(self.options[0])


        else:
            messagebox.showerror("Invalid value","Please enter valid data")
            self.id_entry.delete(0,END)
            self.time_entry.delete(0,END)
            self.clicked.set(self.options[0])

    def update_record_mind(self):
        global update_walk
        global id_entry
        global clicked
        global time_entry
        self.update_walk = Toplevel()
        self.update_walk.title("Update")
        self.update_walk.geometry("300x250")
        self.update_walk.resizable(0, 0)
        self.update_walk.columnconfigure(0, weight=1)
        self.update_walk.columnconfigure(1, weight=1)

        self.act_heading = Label(self.update_walk,text="Update Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

        self.id = Label(self.update_walk,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5),sticky=E)
        self.id_entry = Entry(self.update_walk,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0),sticky=W)

        # type entry
        self.type = Label(self.update_walk,text="Activity: ",font=("Verdana", 10))
        self.type.grid(row=3,column=0,pady=(10,0),padx=(20,5),sticky=E)
        self.options = ["Journal","Yoga","Breathing","Gardening","Music Therapy","Other"]
        self.clicked = StringVar()
        self.clicked.set(self.options[0])
        self.drop = OptionMenu(self.update_walk,self.clicked,*self.options)
        self.drop.config(width=15,height=1)
        self.drop.grid(row=3,column=1,columnspan=2, pady=(20, 0),sticky=W)

        self.time = Label(self.update_walk,text="Time (Hr): ",font=("Verdana", 10))
        self.time.grid(row=4,column=0,pady=(10,0),padx=(20,5),sticky=E)
        self.time_entry = Entry(self.update_walk,width=22)
        self.time_entry.grid(row=4,column=1, padx=(0,40), pady=(15,0),sticky=W)

        self.update_btn = Button(self.update_walk, text="Update", padx=20, pady=3,font=("Verdana", 10),command=self.update_sql_mind)
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.update_walk.mainloop()

def mindful_page():
    top.withdraw()
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

        self.back_btn = Button(self.master,image=self.resize_back,padx=10,pady=10,relief="flat", borderwidth=0,command=lambda:[top.deiconify(),self.master.destroy()])
        self.back_btn.grid(row=0, column=0, padx=5,sticky=NW)

        self.act_heading = Label(self.master,text="Activity",font=("Helvetica", 25))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        #forward
        self.img_fwd = PhotoImage(file=r"images/forward.png")
        self.resize_img_fwd = self.img_fwd.subsample(3,3)
 

        self.master_frame = Frame(self.master)
        self.master_frame.grid(row=2, column=0, columnspan=2)

        self.activity_list = [["Cardio ", self.step_click],["Cycling", self.cycle_click]]

        for self.activity in self.activity_list:

            self.frame = LabelFrame(self.master_frame, padx=30, pady=10)
            self.frame.pack(side=TOP, fill=BOTH, expand=1)

            self.img_activity = PhotoImage(file=rf"images\activity\{self.activity[0]}.png")
            self.img_activity_resize = self.img_activity.subsample(2,2)

            self.activity_lable = Label(self.frame, image=self.img_activity_resize, text=self.activity[0], compound=LEFT, font=("Verdana", 13), borderwidth=0)

            self.activity_lable.grid(row=0, column=0, padx=(0,110))
            self.activity_lable.image = self.img_activity_resize

            self.label_fwd = Label(self.frame, image=self.resize_img_fwd, padx=20, pady=10, borderwidth=0)
            self.label_fwd.grid(row=0, column=1, sticky=E)

            #bind to button
            self.activity_lable.bind('<Button-1>', self.activity[1])
            self.label_fwd.bind('<Button-1>', self.activity[1])
            self.frame.bind('<Button-1>', self.activity[1])

############# walking functons #############

    def step_click(self, event):
        self.master.withdraw()
        self.step_window = Toplevel()
        self.step_window.title("Cardio")
        self.step_window.geometry("450x550")
        self.step_window.resizable(0, 0)
        global distance_entry
        global time_entry
        global weight_entry

        self.step_window.columnconfigure(0, weight=1)
        self.step_window.columnconfigure(1, weight=1)


        self.back_btn = Button(self.step_window,image=self.resize_back,padx=10,pady=10,relief="flat", borderwidth=0,command=lambda:[self.master.deiconify(),self.step_window.destroy()])
        self.back_btn.grid(row=0, column=0, padx=5,sticky=NW)

        self.act_heading = Label(self.step_window,text="Cardio",font=("Helvetica", 25))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        # dropdown for timeperiod
        self.options = ["3-Days","Weekly","Monthly","Yearly"]
        self.clicked = StringVar()
        self.clicked.set(self.options[0])
        self.drop = OptionMenu(self.step_window,self.clicked,*self.options)
        self.drop.grid(row=2,column=0,columnspan=2)

        #graph section
        self.frame_step = LabelFrame(self.step_window,padx=200,pady=100)
        self.frame_step.grid(row=3,column=0,columnspan=2,pady=(10,0))

        self.label_step = Label(self.frame_step,text="Graph")
        self.label_step.grid(row=3,column=0)

        self.label_step = Label(self.step_window,text="Track Calories you Burnt Today!!",font=("Verdana", 13),fg="red")
        self.label_step.grid(row=4,column=0,columnspan=2,pady=(5,2))
        #distance
        self.distance = Label(self.step_window,text="Distance (Km): ",font=("Verdana", 10))
        self.distance.grid(row=5,column=0,pady=(15,0),padx=(20,5),sticky=E)
        self.distance_entry = Entry(self.step_window,width=35)
        self.distance_entry.grid(row=5,column=1, padx=(0,40), pady=(15,0))
        #time
        self.time = Label(self.step_window,text="Time (Hr): ",font=("Verdana", 10))
        self.time.grid(row=6,column=0,pady=(10,0),padx=(20,5),sticky=E)
        self.time_entry = Entry(self.step_window,width=35)
        self.time_entry.grid(row=6,column=1, padx=(0,40), pady=(15,0))
        #weight
        self.weight = Label(self.step_window,text="Weight (Kg): ",font=("Verdana", 10))
        self.weight.grid(row=7,column=0,pady=(10,0),padx=(20,5),sticky=E)
        self.weight_entry = Entry(self.step_window,width=35)
        self.weight_entry.grid(row=7,column=1, padx=(0,40), pady=(15,0))
        #add button
        self.add_btn = Button(self.step_window, text="Track", padx=40, pady=3,font=("Verdana", 10),command=self.add_steps_calories_popup)
        self.add_btn.grid(row=8, column=0, pady=(20, 0), sticky=E, padx=(70, 5)) 
        #show record btn
        self.show_acc = Button(self.step_window, text="Show record", pady=3, padx=30,font=("Verdana", 10),command=self.walking_show_record)
        self.show_acc.grid(row=8, column=1, sticky=W, pady=(20, 0), padx=(5, 0)) 

        self.step_window.mainloop()     

    def add_steps_calories_popup(self):
        
        dist = self.distance_entry.get()
        time = self.time_entry.get()
        weight = self.weight_entry.get()

        if (dist!="" and time!="" and weight!="" and float(dist) > 0 and float(time) > 0 and float(weight) > 0):
            dist = float(self.distance_entry.get())
            time = float(self.time_entry.get())
            weight = float(self.weight_entry.get())
            
            speed = dist/time
            if speed < 3.2:
                met = 2
            elif 3.2<speed<5.6:
                met = 3.9
            else:
                met=5
            
            cal = (met * weight * time)*10/2
            calories = messagebox.askyesno("Calories Burnt",f"HURRAY!! You burnt {cal} Calories, Would you like to record this?")

            if calories:
                sql = "INSERT INTO cardio (username,distance,date,time,calories,weight) VALUES (%s, %s, CURDATE(),%s, %s,%s)"
                val = (username_login,dist,time,cal,weight)
                mycur.execute(sql, val)
                messagebox.showinfo("Record","Record is added Succesfully!")

                db.commit()

            self.weight_entry.delete(0,END)
            self.time_entry.delete(0,END)
            self.distance_entry.delete(0,END)


        else:
            
            messagebox.showerror("Invalid value","Please enter valid distance,time and weight")
            
            self.weight_entry.delete(0,END)
            self.time_entry.delete(0,END)
            self.distance_entry.delete(0,END)

    def walking_show_record(self):

        self.step_window.withdraw()
        self.record_walk_window = Toplevel()
        self.record_walk_window.title("Walking Records")
        self.record_walk_window.geometry("350x450")
        self.record_walk_window.resizable(0, 0)
        self.record_walk_window.grid_rowconfigure(0, weight=1)
        self.record_walk_window.grid_columnconfigure(0, weight=1)

        
        self.back_btn = Button(self.record_walk_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0,command=lambda:[self.step_window.deiconify(),self.record_walk_window.destroy()])
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.record_walk_window,text="Walking Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2)
    
        self.data = LabelFrame(self.record_walk_window,padx=20,pady=5)
        self.data.grid(row=2,column=0,columnspan=3)
        
        # Create a Treeview widget
        self.tree = ttk.Treeview(self.data, columns=("ID", "Date", "Distance", "Time", "Calories", "Weight"), height=14)
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Distance", text="Distance")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Calories", text="Calories")
        self.tree.heading("Weight", text="Weight")

        # Set column widths
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Distance", width=100)
        self.tree.column("Time", width=100)
        self.tree.column("Calories", width=100)
        self.tree.column("Weight", width=100)
        
        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(self.data, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill=BOTH)
        vsb.pack(side="right", fill=Y)

        # Call the populate_treeview method
        self.populate_treeview(username_login)

        self.update_btn = Button(self.record_walk_window,text="Update", padx=30, pady=3,font=("Verdana", 10),command=self.update_record_walk)
        self.update_btn.grid(row=3,column=0, pady=(10, 15), padx=(0,20),sticky=E)

        self.delete_btn = Button(self.record_walk_window,text="Delete", pady=3, padx=30,font=("Verdana", 10),command=self.delete_record_walk)
        self.delete_btn.grid(row=3,column=1,sticky=W, pady=(10, 15), padx=(0,60))
 
        self.record_walk_window.mainloop()

    def populate_treeview(self, username):
        sql = "SELECT id, date, distance, time, calories, weight FROM cardio WHERE username = %s"
        val = (username,)
        mycur.execute(sql, val)
        rows = mycur.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def delete_sql(self):
        self.ans = messagebox.askyesno("Delete Record","Are you sure you want to Delete Your Record?? ")
        if self.ans: 
            self.sql = "DELETE FROM cardio WHERE username = %s AND id = %s"
            self.val = (username_login, self.id_entry.get())

            try:
                mycur.execute(self.sql, self.val)
                affected_rows = mycur.rowcount

                if affected_rows > 0:
                    db.commit()
                    messagebox.showinfo("Delete Record", "Successfully Deleted the Record!")
                    self.id_entry.delete(0, END)
                    self.delete_walk_window.withdraw()
                else:
                    messagebox.showinfo("Delete Record", "Record with the specified ID not found!")

            except mysql.connector.Error as err:
                messagebox.showinfo("Delete Record","Enter Right ID!")
    

        else:
            delete_walk_window.withdraw()

    def delete_record_walk(self):
        global delete_walk_window
        global id_entry

        self.delete_walk_window = Toplevel()
        self.delete_walk_window.title("Delete")
        self.delete_walk_window.geometry("220x200")
        self.delete_walk_window.resizable(0, 0)

        self.step_window.columnconfigure(0, weight=1)
        self.step_window.columnconfigure(1, weight=1)

        self.act_heading = Label(self.delete_walk_window,text="Delete Record",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

        self.id = Label(self.delete_walk_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.delete_walk_window,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.delete_btn = Button(self.delete_walk_window, text="Delete", padx=20, bg="#ff8383",fg="white",pady=3,font=("Verdana", 10),command=self.delete_sql)
        self.delete_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

    def update_sql(self):
        self.id_value = int(self.id_entry.get())
        self.dist = float(self.distance_entry.get())
        self.time = float(self.time_entry.get())
        self.weight = float(self.weight_entry.get())

        if (self.dist!="" and self.time!="" and self.weight!="" and float(self.dist) > 0 and float(self.time) > 0 and float(self.weight) > 0):
            self.speed = self.dist/self.time
            if self.speed < 3.2:
                met = 2
            elif 3.2<self.speed<5.6:
                met = 3.9
            else:
                met=5
            
            self.cal = (met * self.weight * self.time)*10/2

            self.update_query = """
            UPDATE cardio
            SET distance = %s, time = %s, weight = %s,calories = %s
            WHERE id = %s
            """
        
            mycur.execute(self.update_query, (self.dist, self.time, self.weight,self.cal, self.id_value))

            messagebox.showinfo("Update Record","Record is Updated Succesfully!")
            self.update_walk_window.withdraw()

            db.commit()

            self.id_entry.delete(0,END)
            self.weight_entry.delete(0,END)
            self.time_entry.delete(0,END)
            self.distance_entry.delete(0,END)

        else:
                messagebox.showerror("Invalid value","Please enter valid data")
                
                self.id_entry.delete(0,END)
                self.weight_entry.delete(0,END)
                self.time_entry.delete(0,END)
                self.distance_entry.delete(0,END)

    def update_record_walk(self):

        global id_entry
        global distance_entry
        global time_entry
        global weight_entry
        global update_walk_window

        self.update_walk_window = Toplevel()
        self.update_walk_window.title("Update")
        self.update_walk_window.geometry("300x300")
        self.update_walk_window.resizable(0, 0)
        
        self.update_walk_window.columnconfigure(0, weight=1)
        self.update_walk_window.columnconfigure(1, weight=1)

        self.act_heading = Label(self.update_walk_window,text="Update Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

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

        self.weight = Label(self.update_walk_window,text="Weight (Kg): ",font=("Verdana", 10))
        self.weight.grid(row=5,column=0,pady=(10,0),padx=(20,5))
        self.weight_entry = Entry(self.update_walk_window,width=22)
        self.weight_entry.grid(row=5,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.update_walk_window, text="Update", padx=20, pady=3,font=("Verdana", 10),command=self.update_sql)
        self.update_btn.grid(row=6, column=0,columnspan=2, pady=(20, 0)) 

        self.update_walk_window.mainloop()
    
############# cycling functons #############
    def cycle_click(self, event):
        self.master.withdraw()
        self.cycle_window = Toplevel()
        self.cycle_window.title("Cycling")
        self.cycle_window.geometry("450x550")
        self.cycle_window.resizable(0, 0)

        self.cycle_window.columnconfigure(0, weight=1)
        self.cycle_window.columnconfigure(1, weight=1)

        self.back_btn = Button(self.cycle_window,image=self.resize_back,padx=10,pady=10,relief="flat", borderwidth=0,command=lambda:[self.master.deiconify(),self.cycle_window.destroy()])
        self.back_btn.grid(row=0, column=0, padx=5,sticky=NW)

        self.act_heading = Label(self.cycle_window,text="Cycling",font=("Helvetica", 25))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,10))

        # dropdown for timeperiod
        self.options = ["3-Days","Weekly","Month","Yearly"]
        self.clicked = StringVar()
        self.clicked.set(self.options[0])
        self.drop = OptionMenu(self.cycle_window,self.clicked,*self.options)
        self.drop.grid(row=2,column=0,columnspan=2)

        #graph section
        self.frame_step = LabelFrame(self.cycle_window,padx=200,pady=100)
        self.frame_step.grid(row=3,column=0,columnspan=2,pady=(10,0))

        self.label_step = Label(self.frame_step,text="Graph")
        self.label_step.grid(row=3,column=0,)


        self.label_step = Label(self.cycle_window,text="Track Calories you Burnt Today!!",font=("Verdana", 13),fg="red")
        self.label_step.grid(row=4,column=0,columnspan=2,pady=(10,2))

        #distance
        self.distance = Label(self.cycle_window,text="Distance (Km): ",font=("Verdana", 10))
        self.distance.grid(row=5,column=0,pady=(15,0),padx=(20,5),sticky=E)
        self.distance_entry = Entry(self.cycle_window,width=35)
        self.distance_entry.grid(row=5,column=1, padx=(0,40), pady=(15,0))

        #time
        self.time = Label(self.cycle_window,text="Time (Hr): ",font=("Verdana", 10))
        self.time.grid(row=6,column=0,pady=(10,0),padx=(20,5),sticky=E)
        self.time_entry = Entry(self.cycle_window,width=35)
        self.time_entry.grid(row=6,column=1, padx=(0,40), pady=(15,0))

        #weight
        self.weight = Label(self.cycle_window,text="Weight (Kg): ",font=("Verdana", 10))
        self.weight.grid(row=7,column=0,pady=(10,0),padx=(20,5),sticky=E)
        self.weight_entry = Entry(self.cycle_window,width=35)
        self.weight_entry.grid(row=7,column=1, padx=(0,40), pady=(15,0))

        #add button
        self.add_btn = Button(self.cycle_window, text="Add", padx=40, pady=3,font=("Verdana", 10),command=self.add_cycle_calories_popup)
        self.add_btn.grid(row=8, column=0, pady=(20, 0), sticky=E, padx=(70, 5)) 

        #show record btn
        self.show_acc = Button(self.cycle_window, text="Show record", pady=3, padx=30,font=("Verdana", 10),command=self.cycle_show_record)
        self.show_acc.grid(row=8, column=1, sticky=W, pady=(20, 0), padx=(5, 0)) 

        self.cycle_window.mainloop()
    
    def add_cycle_calories_popup(self):

        dist = self.distance_entry.get()
        time = self.time_entry.get()
        weight = self.weight_entry.get()

        if (dist!="" and time!="" and weight!="" and float(dist) > 0 and float(time) > 0 and float(weight) > 0):
              
            dist = float(self.distance_entry.get())
            time = float(self.time_entry.get())
            weight = float(self.weight_entry.get())

            speed = dist/time
            if 2.7 <speed < 3.3:
                met = 4
            elif 3.3<speed<3.8:
                met = 6
            else:
                met=8
            
            cal = (met * weight * time)*10/2
            calories = messagebox.askyesno("Calories Burnt",f"HURRAY!! You burnt {cal} Calories, Would you like to record this?")

            if calories:
                sql = "INSERT INTO cycling (username,distance,date,time,calories,weight) VALUES (%s, %s, CURDATE(),%s, %s,%s)"
                val = (username_login,dist,time,cal,weight)
                mycur.execute(sql, val)
                messagebox.showinfo("Record","Record is added Succesfully!")
            
                db.commit()

            self.weight_entry.delete(0,END)
            self.time_entry.delete(0,END)
            self.distance_entry.delete(0,END)


        else:
            messagebox.showerror("Invalid value","Please enter valid distance,time and weight")
            
            self.weight_entry.delete(0,END)
            self.time_entry.delete(0,END)
            self.distance_entry.delete(0,END)

    def populate_treeview_cycle(self, username):
        sql = "SELECT id, date, distance, time, calories, weight FROM cycling WHERE username = %s"
        val = (username,)
        mycur.execute(sql, val)
        rows = mycur.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def cycle_show_record(self):

        self.cycle_window.withdraw()
        self.record_cycle_window = Toplevel()
        self.record_cycle_window.title("Cycling Records")
        self.record_cycle_window.geometry("350x450")
        self.record_cycle_window.resizable(0, 0)
        self.record_cycle_window.grid_rowconfigure(0, weight=1)
        self.record_cycle_window.grid_columnconfigure(0, weight=1)

        
        self.back_btn = Button(self.record_cycle_window,image=self.resize_back,padx=10,pady=5,relief="flat", borderwidth=0,command=lambda:[self.cycle_window.deiconify(),self.record_cycle_window.destroy()])
        self.back_btn.grid(row=0, column=0,columnspan=2, padx=5,sticky=NW)

        self.act_heading = Label(self.record_cycle_window,text="Cycling Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(0,20))
    
        self.data = LabelFrame(self.record_cycle_window,padx=20,pady=15)
        self.data.grid(row=2,column=0,columnspan=3)
        
        # Create a Treeview widget
        self.tree = ttk.Treeview(self.data, columns=("ID", "Date", "Distance", "Time", "Calories", "Weight"), height=13)
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Distance", text="Distance")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Calories", text="Calories")
        self.tree.heading("Weight", text="Weight")

        # Set column widths
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Distance", width=100)
        self.tree.column("Time", width=100)
        self.tree.column("Calories", width=100)
        self.tree.column("Weight", width=100)
        
        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(self.data, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill=BOTH)
        vsb.pack(side="right", fill=Y)

        # Call the populate_treeview method
        self.populate_treeview_cycle(username_login)

        self.update_btn = Button(self.record_cycle_window,text="Update", padx=30, pady=3,font=("Verdana", 10),command=self.update_record_cycle)
        self.update_btn.grid(row=3,column=0, pady=(10, 15), padx=(0,20),sticky=E)

        self.delete_btn = Button(self.record_cycle_window,text="Delete", pady=3, padx=30,font=("Verdana", 10),command=self.delete_record_cycle)
        self.delete_btn.grid(row=3,column=1,sticky=W, pady=(10, 15), padx=(0,60))
 
        self.record_cycle_window.mainloop()

    def delete_sql_cycle(self):
        self.ans = messagebox.askyesno("Delete Record","Are you sure you want to Delete Your Record?? ")
        if self.ans: 
            self.sql = "DELETE FROM cycling WHERE username = %s AND id = %s"
            self.val = (username_login, self.id_entry.get())

            try:
                mycur.execute(self.sql, self.val)
                affected_rows = mycur.rowcount

                if affected_rows > 0:
                    db.commit()
                    messagebox.showinfo("Delete Record", "Successfully Deleted the Record!")
                    self.id_entry.delete(0, END)
                    self.delete_cycle_window.withdraw()
                else:
                    messagebox.showinfo("Delete Record", "Record with the specified ID not found!")

            except mysql.connector.Error as err:
                messagebox.showinfo("Delete Record","Enter Right ID!")
    

        else:
            self.delete_cycle_window.withdraw()

    def delete_record_cycle(self):

        global delete_cycle_window
        global id_entry
        self.delete_cycle_window = Toplevel()
        self.delete_cycle_window.title("Update")
        self.delete_cycle_window.geometry("220x200")
        self.delete_cycle_window.resizable(0, 0)

        self.delete_cycle_window.columnconfigure(0, weight=1)
        self.delete_cycle_window.columnconfigure(1, weight=1)

        self.act_heading = Label(self.delete_cycle_window,text="Delete Record",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

        self.id = Label(self.delete_cycle_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.delete_cycle_window,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.delete_cycle_window, text="Delete", padx=20, bg="#ff8383",fg="white",pady=3,font=("Verdana", 10),command=self.delete_sql_cycle)
        self.update_btn.grid(row=5, column=0,columnspan=2, pady=(20, 0)) 

        self.delete_cycle_window.mainloop()

    def update_sql_cycle(self):

        self.id_value = self.id_entry.get()
        self.dist = self.distance_entry.get()
        self.time = self.time_entry.get()
        self.weight = self.weight_entry.get()

        if (self.dist!="" and self.time!="" and self.weight!="" and float(self.dist) > 0 and float(self.time) > 0 and float(self.weight) > 0):

            self.id_value = int(self.id_entry.get())
            self.dist = float(self.distance_entry.get())
            self.time = float(self.time_entry.get())
            self.weight = float(self.weight_entry.get())

            self.speed = self.dist/self.time

            if self.speed < 3.2:
                met = 2
            elif 3.2<self.speed<5.6:
                met = 3.9
            else:
                met=5
            
            self.cal = (met * self.weight * self.time)*10/2

            self.update_query = """
            UPDATE cycling
            SET distance = %s, time = %s, weight = %s,calories = %s
            WHERE id = %s
            """
        
            mycur.execute(self.update_query, (self.dist, self.time, self.weight,self.cal, self.id_value))

            messagebox.showinfo("Update Record","Record is Updated Succesfully!")
            self.update_cycle_window.withdraw()

            db.commit()

            self.id_entry.delete(0,END)
            self.weight_entry.delete(0,END)
            self.time_entry.delete(0,END)
            self.distance_entry.delete(0,END)

        else:
                messagebox.showerror("Invalid value","Please enter valid data")
                
                self.id_entry.delete(0,END)
                self.weight_entry.delete(0,END)
                self.time_entry.delete(0,END)
                self.distance_entry.delete(0,END)

    def update_record_cycle(self):

        global id_entry
        global distance_entry
        global time_entry
        global weight_entry
        global update_cycle_window

        self.update_cycle_window = Toplevel()
        self.update_cycle_window.title("Update")
        self.update_cycle_window.geometry("300x300")
        self.update_cycle_window.resizable(0, 0)
        
        self.update_cycle_window.columnconfigure(0, weight=1)
        self.update_cycle_window.columnconfigure(1, weight=1)

        self.act_heading = Label(self.update_cycle_window,text="Update Records",font=("Helvetica", 15))
        self.act_heading.grid(row=1,column=0,columnspan=2,pady=(20,10))

        self.id = Label(self.update_cycle_window,text="Id: ",font=("Verdana", 10))
        self.id.grid(row=2,column=0,pady=(15,0),padx=(20,5))
        self.id_entry = Entry(self.update_cycle_window,width=22)
        self.id_entry.grid(row=2,column=1, padx=(0,40), pady=(15,0))

        self.distance = Label(self.update_cycle_window,text="Distance (Km): ",font=("Verdana", 10))
        self.distance.grid(row=3,column=0,pady=(15,0),padx=(20,5))
        self.distance_entry = Entry(self.update_cycle_window,width=22)
        self.distance_entry.grid(row=3,column=1, padx=(0,40), pady=(15,0))

        self.time = Label(self.update_cycle_window,text="Time (Hr): ",font=("Verdana", 10))
        self.time.grid(row=4,column=0,pady=(10,0),padx=(20,5))
        self.time_entry = Entry(self.update_cycle_window,width=22)
        self.time_entry.grid(row=4,column=1, padx=(0,40), pady=(15,0))

        self.weight = Label(self.update_cycle_window,text="Weight (Kg): ",font=("Verdana", 10))
        self.weight.grid(row=5,column=0,pady=(10,0),padx=(20,5))
        self.weight_entry = Entry(self.update_cycle_window,width=22)
        self.weight_entry.grid(row=5,column=1, padx=(0,40), pady=(15,0))

        self.update_btn = Button(self.update_cycle_window, text="Update", padx=20, pady=3,font=("Verdana", 10),command=self.update_sql_cycle)
        self.update_btn.grid(row=6, column=0,columnspan=2, pady=(20, 0)) 

        self.update_cycle_window.mainloop()

def activity_page():
    top.withdraw()
    activity_window = Toplevel(root)
    app = Activity(activity_window)


def login_verify():
    global username_login 
    global password
    global top
    username_login= username_entry.get()
    password = password_entry.get()
    sql = "select * from users where username = %s and password = %s"
    mycur.execute(sql,[(username_login),(password)])
    results = mycur.fetchall()
    if results:
        for i in results:
            messagebox.showinfo("Logged in", f"Welcome {username_login}!")
            root.withdraw()
            home_page()
            break
    else:
        root.deiconify()
        messagebox.showerror("Error","Please fill out both fields correctly.")

def home_page():

    global top
    top = Toplevel()
    top.title("Home")
    top.geometry("450x330")
    top.resizable(0, 0)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)

    image = Image.open("images/user.png")  
    photo = ImageTk.PhotoImage(image)
    user_btn = Button(top,image=photo,relief="flat", borderwidth=0,command=delete_or_logout)
    user_btn.grid(row=0,column=1, sticky=E, padx=5, pady=5,ipadx=10,ipady=10)
    user_btn.image = photo # Setting the image as a reference to prevent it from being garbage collected

    label = Label(top,text="Track Yourself Now!!", font=("Helvetica", 20),pady=10)
    label.grid(row=1,column=0,columnspan=2)

    # activity button
    activity_image = PhotoImage(file='images/activity.png')
    resized_image = activity_image.subsample(2, 2)
    activity_btn = Button(top, text=" Activity ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5,command=activity_page)
    activity_btn.image = resized_image
    activity_btn.grid(row=3,column=0, pady=(20,10),ipadx=15)

    # mindfullness button
    mindful_image = PhotoImage(file='images/mindfulness.png')
    resized_image = mindful_image.subsample(2, 2)
    mindful_btn = Button(top, text=" Mindfulness ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5,command=mindful_page)
    mindful_btn.image = resized_image
    mindful_btn.grid(row=3,column=1,pady=(20, 15))

    # body button
    body_image = PhotoImage(file='images/body.png')
    resized_image = body_image.subsample(2, 2)
    body_btn = Button(top, text=" Body ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5,command=body_page)
    body_btn.image = resized_image
    body_btn.grid(row=4,column=0,pady=(10, 15),ipadx=25)


    sleep_image = PhotoImage(file='images/sleep.png')
    resized_image = sleep_image.subsample(2, 2)
    sleep_btn = Button(top, text=" Sleep ", image=resized_image,compound=LEFT, font=("Verdana", 12),padx=5,pady=5,command=sleep_page) 
    sleep_btn.image = resized_image
    sleep_btn.grid(row=4,column=1,pady=(10, 15),ipadx=25)

def create_user():
    name_info = fullname_entry.get()
    birthday_info = dob_entry.get()
    username_info = username_entry.get()
    password_info = password_entry.get()
    gender_info = clicked.get()

    if (name_info or birthday_info or username_info or password_info or gender_info) == "":
        messagebox.showwarning("Empty Fields", "All fields are required...")

    else: 
        mycur.execute('''
            INSERT INTO users (fullname, dob, username, password, gender)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name_info,birthday_info,username_info,password_info,gender_info))
        db.commit()
        create_acc_window.withdraw()
        messagebox.showinfo("Account Created", "Your account has been created successfully.")
    
    home_page()

def create_acc_click():
    root.withdraw()
    global create_acc_window
    create_acc_window = Toplevel()
    create_acc_window.title("Sign Up")
    create_acc_window.geometry("400x280")
    create_acc_window.resizable(0, 0)
    create_acc_window.columnconfigure(0, weight=1)
    create_acc_window.columnconfigure(1, weight=1)
    global fullname_entry
    global dob_entry
    global username_entry
    global password_entry
    global clicked

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
    
    signup_btn = Button(create_acc_window,text="Sign up",padx=10,pady=5,command=create_user)
    signup_btn.grid(row=8,column=0,columnspan=2, padx=5, pady=10)

def delete_acc():
    result = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
    
    if result:
        
        mycur.execute('DELETE FROM users WHERE username = %s',(username,))
        db.commit()
        messagebox.showinfo("Account Deleted", "Your account has been deleted.")
        acc.withdraw()  
        top.withdraw()
        root.deiconify()
        username_entry.delete(0,END)
        password_entry.delete(0,END)

    else:
        acc.withdraw()

def logout_acc():
    acc.withdraw()
    top.withdraw()
    root.deiconify()
    username_entry.delete(0,END)
    password_entry.delete(0,END)
      
def delete_or_logout():
    # username = username_entry.get()
    global acc
    acc = Toplevel()
    acc.title("Delete or Logout")
    acc.geometry("300x170")
    acc.resizable(0, 0)
    acc.columnconfigure(0, weight=1)
    acc.columnconfigure(1, weight=1)

    label = Label(acc,text="Do you want to DELETE or",font=("Verdana", 12))
    label.grid(row=0,column=0,columnspan=2,pady=(20,5))

    label2 = Label(acc,text="LOGOUT from your Account? ",font=("Verdana", 12))
    label2.grid(row=1,column=0,columnspan=2,pady=(0,20))

    btn_delete = Button(acc,text="Delete Account",bg="red",fg="white",padx=10,pady=3,command=delete_acc)
    btn_delete.grid(row=2,column=0,columnspan=2)

    btn_logout = Button(acc,text="Logout",padx=10,relief="flat", borderwidth=0,pady=3,command=logout_acc)
    btn_logout.grid(row=3,column=0,columnspan=2)


label_root = Label(root,text="Welcome to FitFolio!!",font=("Helvetica", 15),pady=20)
label_root.grid(row=1,column=0,columnspan=2)

#username
username = Label(root,text="Username: ")
username.grid(row=2,column=0)
username_entry = Entry(root,width=30)
username_entry.grid(row=2,column=1,sticky=W, padx=5, pady=5)

#password
password = Label(root,text="Password: ")
password.grid(row=3,column=0)
password_entry = Entry(root,width=30, show='*')
password_entry.grid(row=3,column=1,sticky=W, padx=5, pady=5)

#login button
login_btn = Button(root,text="Login",padx=10,pady=3,command=login_verify)
login_btn.grid(row=4,column=0,columnspan=2,pady=(10,0),padx=20)

#create button
create_acc_text = "Create Account"
create_acc = Button(root,text=create_acc_text,pady=3,relief="flat", borderwidth=0,underline=len(create_acc_text),command=create_acc_click)
create_acc.grid(row=5,columnspan=2,column=0)

root.mainloop()