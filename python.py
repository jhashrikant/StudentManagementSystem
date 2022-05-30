import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry       # pip install tkcalendar
import sqlite3

#creating universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ("Garamond" ,12)

#connecting  to the Database where all information will be stored 
connector = sqlite3.connect("SchoolManagement.db")
cursor = connector.cursor()
connector.execute(
    "CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT(STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT ,GENDER TEXT,DOB TEXT,STREAM TEXT)"
    )

#Creating the functions 
def add_record():
    global name_Of_user ,Contact_Of_user,email_Of_user,gender_Of_user,stream_Of_user,dob
    name = name_Of_user.get()
    email = email_Of_user.get()
    contact = Contact_Of_user.get()
    gender = gender_Of_user.get()
    DOB = dob.get_date()
    stream = stream_Of_user.get()
    

    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            connector.execute(
                'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)', (name, email, contact, gender, DOB, stream)
            )
            mb.askquestion("Confirm","Are you sure?")
            connector.commit()
            mb.showinfo('Record added', f"Record of {name} was successfully added")
            reset_fields()
            display_records()
        except :
            mb.showerror('Wrong type', 'The type of the values entered is not accurate')



def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values.get("values")
        mb.showwarning("confirm","Are you sure you want to delete?")
        tree.delete(current_item)
        connector.execute('DELETE FROM SCHOOL MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()
        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

        display_records()



def reset_fields():
    global name_Of_user, Contact_Of_user, email_Of_user, gender_Of_user, stream_Of_user, dob
    for items in ['name_Of_user','Contact_Of_user','email_Of_user','gender_Of_user','stream_Of_user']:
        exec(f"{items}.set(' ')")
    dob.set_date(datetime.datetime.now().date())



def reset_form():
    global tree
    tree.delete(*tree.get_children())
    reset_fields()


def display_records():
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
    data = curr.fetchall()
    for records in data:
        tree.insert('',END,values=records)
        

def view_record():
    global name_Of_user, Contact_Of_user, email_Of_user, gender_Of_user, stream_Of_user, dob

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))

    name_Of_user.set(selection[1]); email_Of_user.set(selection[2])
    Contact_Of_user.set(selection[3]); gender_Of_user.set(selection[4])
    dob.set_date(date); stream_Of_user.set(selection[6]);Remaining_fees_Of_user.set(selection[7])

 
#Initializing the GUI window
main = Tk()
main.title('Carmel English High SChool')
main.geometry('1200x700')
main.resizable(True , True)

#creating the background and foreground color variables 
left_bg = 'MediumSpringGreen'    #bg color for left frame
center_frame_bg = 'PaleGreen'   #bg color for center frame

#creating the StringVar or IntVar variables 
name_Of_user = StringVar()
Contact_Of_user = StringVar()
email_Of_user = StringVar()
gender_Of_user = StringVar()
stream_Of_user = StringVar()


#Placing the components in the main GUI window 
Label(main,text="SCHOOL MANAGEMENT SYSTEM",font=headlabelfont,bg='SpringGreen').pack(side=TOP,fill=X)  # Label widget is a standard Tkinter widget used to display a text or image on the screen. 

left_frame = Frame(main,bg=left_bg)
left_frame.place(x=0,y=30, relheight=1,relwidth=0.2)

center_frame = Frame(main,bg=center_frame_bg)
center_frame.place(relx=0.2 , y=30 , relheight=1,relwidth=0.2)

right_frame = Frame(main,bg="Gray35")
right_frame.place(relx=0.4 , y=30, relheight=1,relwidth=0.6)

#placing components in the left frame 
Label(left_frame, text="Name", font=labelfont, bg=left_bg).place(relx=0.375, rely=0.05)
Label(left_frame, text="Contact Number", font=labelfont, bg=left_bg).place(relx=0.175, rely=0.18)
Label(left_frame, text="Email Address", font=labelfont, bg=left_bg).place(relx=0.2, rely=0.31)
Label(left_frame, text="Gender", font=labelfont, bg=left_bg).place(relx=0.3, rely=0.44)
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=left_bg).place(relx=0.1, rely=0.57)
Label(left_frame, text="Stream", font=labelfont, bg=left_bg).place(relx=0.3, rely=0.7)


#Taking user input by Entry widgets
Entry(left_frame, width=19, textvariable=name_Of_user, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=Contact_Of_user, font=entryfont).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=email_Of_user, font=entryfont).place(x=20, rely=0.36)
Entry(left_frame, width=19, textvariable=stream_Of_user, font=entryfont).place(x=20, rely=0.75)

OptionMenu(left_frame,gender_Of_user, "Male" ,"Female").place(x=45, rely=0.49,relwidth=0.5)
dob = DateEntry(left_frame,font=("Arial",12), width=15)
dob.place(x=20,rely =0.62)

Button(left_frame,text="Submit and Add Record",font=labelfont,command=add_record,width=18).place(relx=0.025, rely=0.85)

#placing components in the center frame 
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)

#placing components in the right frame 
Label(right_frame, text="Students Records",font=headlabelfont,bg="DarkGreen",fg="LightCyan").pack(side=TOP,fill=X)

#making treeview structure for columns 
tree = ttk.Treeview(right_frame,height=100,selectmode=BROWSE,
columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender","Date of Birth", "Stream"))

X_scroller = Scrollbar(tree,orient=HORIZONTAL,command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)


X_scroller.pack(side=BOTTOM,fill=X)
Y_scroller.pack(side=RIGHT,fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)



tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=50, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)


tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

#Finalizing the GUI window
main.update()
main.mainloop()

