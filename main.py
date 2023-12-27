from tkinter import *
from PIL import ImageTk,Image
from tkinter import PhotoImage

root = Tk()
root.title("FitFolio")
icon_image = PhotoImage(file="images/heart.png")
root.iconphoto(True, icon_image) 
root.geometry("450x300")
root.resizable(0, 0) #fixed size of the window

# configuring the rows and columns of the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

image = Image.open("images/user.png")  
photo = ImageTk.PhotoImage(image)
user_btn = Button(root,image=photo)
user_btn.grid(row=0,column=1, sticky=E, padx=5, pady=5,ipadx=10,ipady=10)
user_btn.image = photo # Setting the image as a reference to prevent it from being garbage collected

class ImageButton(Button):
    def __init__(self, master=None, **kwargs):
        Button.__init__(self, master, compound="left", **kwargs)
        self.image = kwargs.get('image', None)
        self.text = kwargs.get('text', None)

        if self.image and self.text:
            self.update_text_image()

    def update_text_image(self):
        if self.image and self.text:
            self.config(text=self.text, image=self.image, compound="left")

label = Label(root,text="Track Yourself Now!!", font=("Helvetica", 20))
label.grid(row=1,column=0,columnspan=2)


# activity button
activity_image = PhotoImage(file='images/activity.png')
resized_image = activity_image.subsample(2, 2)
activity_btn = ImageButton(root, text=" Activity ", image=resized_image, font=("Verdana", 12),padx=5,pady=5)
activity_btn.grid(row=3,column=0, pady=(20,10),ipadx=15)

# mindfullness button
mindful_image = PhotoImage(file='images/mindfulness.png')
resized_image = mindful_image.subsample(2, 2)
mindful_btn = ImageButton(root, text=" Mindfulness ", image=resized_image, font=("Verdana", 12),padx=5,pady=5)
mindful_btn.grid(row=3,column=1,pady=(20, 15))

# body button
body_image = PhotoImage(file='images/body.png')
resized_image = body_image.subsample(2, 2)
body_btn = ImageButton(root, text=" Body ", image=resized_image, font=("Verdana", 12),padx=5,pady=5)
body_btn.grid(row=4,column=0,pady=(10, 15),ipadx=25)

# sleep button
sleep_image = PhotoImage(file='images/sleep.png')
resized_image = sleep_image.subsample(2, 2)
sleep_btn = ImageButton(root, text=" Sleep ", image=resized_image, font=("Verdana", 12),padx=5,pady=5)
sleep_btn.grid(row=4,column=1,pady=(10, 15),ipadx=25)


root.mainloop()



