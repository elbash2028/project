from tkinter import *
from tkinter import ttk  # For Treeview widget
from fpdf import FPDF
from tkinter import filedialog as fd
import tkinter.messagebox as msbx
import os
import logging
import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

# If your `employees` app has custom context processors or templatetags
try:
    import employees.context_processors
    import employees.templatetags
except ImportError:
    pass

# Adjust the path to your Django project directory
sys.path.append(os.path.abspath(r'C:\Users\EL-BASH\Desktop\project\EmployeeManagementSystem'))
# Django setup with MySQL
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'employee_management',  # Replace with your actual database name
            'USER': 'admin',
            'PASSWORD': '12345',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'employees',  # Replace 'employees' with your app name
    ],
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    ROOT_URLCONF='EmployeeManagementSystem.urls',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    WSGI_APPLICATION='EmployeeManagementSystem.application',
)

django.setup()  # Initialize Django settings

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

# Log a debug message before calling command
logging.debug('Calling makemigrations')

# Apply migrations
from django.core.management import call_command

try:
    # Running Django's makemigrations command without redirecting stdout and stderr
    call_command('makemigrations', stdout=None, stderr=None)
    call_command('migrate', stdout=None, stderr=None)  # You might also need to run migrate
except Exception as e:
    print(f"An error occurred: {e}")

#import Django Models
from employees.models import Employee, Department, Event, Internship

# Function for the login screen
def login_screen():
    global screen
    global usernameEntry
    global passwordEntry
    global img

    # GUI WINDOW
    screen = Tk()
    screen.title("Employee - Management System")
    screen.geometry("600x700")

    # Load Image
    img = PhotoImage(file="logo1.png")
    c_canvas = Canvas(screen, height=900, width=600)
    c_canvas.pack(side=TOP, padx=10)
    c_canvas.create_image(0, 0, anchor=NW, image=img)

    # Username and Password (label & entry)
    userlabel = Label(screen, text="Username: ", font=("Times", 11, "bold"), fg="#696969")
    passlabel = Label(screen, text="Password: ", font=("Times", 11, "bold"), fg="#696969")
    usernameEntry = Entry(screen, bd=4)
    passwordEntry = Entry(screen, show="*", bd=4)

    # Place label and entry widgets for username and password
    userlabel.place(x=60, y=340)
    usernameEntry.place(x=140, y=340)
    passlabel.place(x=60, y=370)
    passwordEntry.place(x=140, y=370)

    # Buttons
    submit = Button(screen, text="Submit", command=submit_action)
    submit.pack()
    submit.place(x=130, y=410)
    
    reset = Button(screen, text="Reset", command=reset_action)
    reset.pack()
    reset.place(x=190, y=410)
    
    quit_a = Button(screen, text="Exit", command=quit_action)
    quit_a.pack()
    quit_a.place(x=240, y=410)

    # Run the main loop of the window
    screen.mainloop()

# Submit function for login details
def submit_action():
    username = usernameEntry.get()
    password = passwordEntry.get()

    try:
        if username != 'admin' or password != '12345':
            raise ValueError()
    except ValueError:
        msbx.showinfo("Login Error", "Username or password Incorrect")
    else:
        screen.withdraw()  # Hide the login screen instead of destroying it
        home_screen()  # Open the home screen

# Home screen function
def home_screen():
    global screen_home
    global tree_employee
    global tree_department
    global tree_internship
    global tree_event
    
    screen_home = Toplevel(screen)  # Create a new window
    screen_home.title('Employee Management System - Home page')  # Add title to window
    screen_home.geometry("800x600+300+100")  # Set the window size and position

    # Create a Notebook widget for tabs
    notebook = ttk.Notebook(screen_home)
    notebook.pack(fill=BOTH, expand=True)

    # Create tabs
    tab_employee = Frame(notebook)
    tab_department = Frame(notebook)
    tab_internship = Frame(notebook)
    tab_event = Frame(notebook)
    notebook.add(tab_employee, text="Employee")
    notebook.add(tab_department, text="Departments")
    notebook.add(tab_internship, text="Internships")
    notebook.add(tab_event, text="Events")

     # Create Treeview for Employees
    columns_employee = ("First Name", "Last Name", "Gender", "Age", "Address", "Contact", "Department", "Employment Date", "Nationality", "Marital Status")
    tree_employee = ttk.Treeview(tab_employee, columns=columns_employee, show="headings")
    for col in columns_employee:
        tree_employee.heading(col, text=col)
    tree_employee.pack(fill=BOTH, expand=True)

    # Add horizontal scrollbar for Employees Treeview
    scrollbar_employee_x = Scrollbar(tab_employee, orient=HORIZONTAL, command=tree_employee.xview)
    tree_employee.configure(xscrollcommand=scrollbar_employee_x.set)
    scrollbar_employee_x.pack(side=BOTTOM, fill=X)
    
    # Create Treeview for Departments
    columns_department = ("ID", "Name", "Manager", "Established Date")
    tree_department = ttk.Treeview(tab_department, columns=columns_department, show="headings")
    for col in columns_department:
        tree_department.heading(col, text=col)
    tree_department.pack(fill=BOTH, expand=True)

    # Add horizontal scrollbar for Departments Treeview
    scrollbar_department_x = Scrollbar(tab_department, orient=HORIZONTAL, command=tree_department.xview)
    tree_department.configure(xscrollcommand=scrollbar_department_x.set)
    scrollbar_department_x.pack(side=BOTTOM, fill=X)

    # Create Treeview for Internships
    columns_internship = ("ID", "Title", "Description", "Start Date", "End Date")
    tree_internship = ttk.Treeview(tab_internship, columns=columns_internship, show="headings")
    for col in columns_internship:
        tree_internship.heading(col, text=col)
    tree_internship.pack(fill=BOTH, expand=True)

    # Add horizontal scrollbar for Internships Treeview
    scrollbar_internship_x = Scrollbar(tab_internship, orient=HORIZONTAL, command=tree_internship.xview)
    tree_internship.configure(xscrollcommand=scrollbar_internship_x.set)
    scrollbar_internship_x.pack(side=BOTTOM, fill=X)

    # Create Treeview for Events
    columns_event = ("ID", "Title", "Date", "Location", "Description")
    tree_event = ttk.Treeview(tab_event, columns=columns_event, show="headings")
    for col in columns_event:
        tree_event.heading(col, text=col)
    tree_event.pack(fill=BOTH, expand=True)

    # Add horizontal scrollbar for Events Treeview
    scrollbar_event_x = Scrollbar(tab_event, orient=HORIZONTAL, command=tree_event.xview)
    tree_event.configure(xscrollcommand=scrollbar_event_x.set)
    scrollbar_event_x.pack(side=BOTTOM, fill=X)
    
    # Create submenu for File menu with Save and Exit
    firstlist = Menu(screen_home, tearoff=0)
    firstlist.add_command(label='Save', command=save_file)
    firstlist.add_command(label='Exit', command=screen_home.destroy)

    # Create submenu for Create menu
    createlist = Menu(screen_home, tearoff=0)
    createlist.add_command(label='Add Employee', command=add_employee)
    createlist.add_command(label='Add Department', command=add_department)
    createlist.add_command(label='Add Internship', command=add_internship)
    createlist.add_command(label='Add Event', command=add_event)

    # Create submenu for Edit menu
    editlist = Menu(screen_home, tearoff=0)
    editlist.add_command(label='Edit Employee', command=edit_employee)
    editlist.add_command(label='Edit Interns', command=edit_interns)
    editlist.add_command(label='Edit Departments', command=edit_departments)
    editlist.add_command(label='Edit Schedule', command=edit_schedule)

    # Create submenu for View menu
    viewlist = Menu(screen_home, tearoff=0)
    viewlist.add_command(label='View Employees', command=view_employees)
    viewlist.add_command(label='View Departments', command=view_departments)
    viewlist.add_command(label='View Interns', command=view_interns)
    viewlist.add_command(label='View Events', command=view_events)

    # Create submenu for Help menu
    helplist = Menu(screen_home, tearoff=0)
    helplist.add_command(label='Help', command=show_help)

    # Create the main menu bar
    myMenu = Menu(screen_home)
    myMenu.add_cascade(label="File", menu=firstlist)
    myMenu.add_cascade(label="Create", menu=createlist)
    myMenu.add_cascade(label="Edit", menu=editlist)
    myMenu.add_cascade(label="View", menu=viewlist)
    myMenu.add_cascade(label="Help", menu=helplist)
    myMenu.add_cascade(label="Log out", command=log_out)

    screen_home.config(menu=myMenu)
    #load data into the treeview
    load_data()
def load_data():
    try:
        employees = Employee.objects.all()
        for emp in employees:
            tree_employee.insert("", "end", values=(emp.firstname, emp.lastname, emp.gender, emp.age, emp.address,emp.contact,emp.department,emp.employment_date,emp.nationality,emp.marital_status))

        departments = Department.objects.all()
        for dept in departments:
            tree_department.insert("", "end", values=(dept.id, dept.name, dept.manager, dept.established_date))

        internships = Internship.objects.all()
        for intern in internships:
            tree_internship.insert("", "end", values=(intern.id, intern.title, intern.description, intern.start_date, intern.end_date))

        events = Event.objects.all()
        for event in events:
            tree_event.insert("", "end", values=(event.id, event.title, event.date, event.location, event.description))
    except Exception as e:
        msbx.showerror("Load Data", f"Error loading data: {e}")

def save_file():
    try:
        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=10)  # Reduced font size for more content fitting

        def add_section(title, tree, fields):
            pdf.set_font("Helvetica", size=12)
            pdf.cell(0, 10, text=title, new_x='LMARGIN', new_y='NEXT', align='L')
            pdf.ln(5)
            pdf.set_font("Helvetica", size=10)

            for item in tree.get_children():
                values = tree.item(item)['values']
                text = ', '.join(f"{fields[i]}: {values[i]}" for i in range(len(values)))
                pdf.multi_cell(0, 10, text, align='L')
                pdf.ln(2)  # Space between entries

        # Add Employee Data
        employee_fields = ["First Name", "Last Name", "Gender", "Age", "Address", "Contact", "Department", "Employment Date", "Nationality", "Marital Status"]
        add_section("Employees", tree_employee, employee_fields)

        # Add Department Data
        department_fields = ["ID", "Name", "Manager", "Established Date"]
        add_section("Departments", tree_department, department_fields)

        # Add Internship Data
        internship_fields = ["ID", "Title", "Description", "Start Date", "End Date"]
        add_section("Internships", tree_internship, internship_fields)

        # Add Event Data
        event_fields = ["ID", "Title", "Date", "Location", "Description"]
        add_section("Events", tree_event, event_fields)

        # Save the PDF to a file
        file_path = fd.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            msbx.showinfo("Save File", "Content saved to PDF successfully!")
        else:
            msbx.showwarning("Save File", "Save operation cancelled")

    except Exception as e:
        msbx.showerror("Save File", f"Error saving content: {e}")
# Function to handle logout
def log_out():
    mess_quit = msbx.askyesno(title='Exit', message='Are you sure to quit?')
    if mess_quit:
        screen_home.destroy()
        screen.deiconify()  # Show the login screen again

# Reset function
def reset_action():
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)

# Quit login page function
def quit_action():
    mess_quit = msbx.askyesno(title='Exit', message='Are you sure you want to quit?')
    if mess_quit == 1:
        screen.destroy()

# Function to add a new employee
def add_employee():
    global NewWindow
    global FIRSTNAME
    global LASTNAME
    global GENDER
    global AGE
    global ADDRESS
    global CONTACT
    global DEPARTMENT
    global EMPLOYMENT_DATE
    global NATIONALITY
    global MARITAL_STATUS

    # Create Variables to store Entry data
    FIRSTNAME = StringVar()
    LASTNAME = StringVar()
    GENDER = StringVar()
    AGE = StringVar()
    ADDRESS = StringVar()
    CONTACT = StringVar()
    DEPARTMENT = StringVar()
    EMPLOYMENT_DATE = StringVar()
    NATIONALITY = StringVar()
    MARITAL_STATUS = StringVar()

    NewWindow = Toplevel(screen_home)
    NewWindow.title("Add Employee")
    width = 400
    height = 500
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = ((screen_width / 2) - 455) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # Frames
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    RadioGroup2 = Frame(ContactForm)

    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    Single = Radiobutton(RadioGroup2, text="Single", variable=MARITAL_STATUS, value="Single", font=('arial', 14)).pack(side=LEFT)
    Married = Radiobutton(RadioGroup2, text="Married", variable=MARITAL_STATUS, value="Married", font=('arial', 14)).pack(side=LEFT)
    Divorced = Radiobutton(RadioGroup2, text="Divorced", variable=MARITAL_STATUS, value="Divorced", font=('arial', 14)).pack(side=LEFT)

    # Add Employee Label
    Label(FormTitle, text="Add New Employee", font=('arial', 15, 'bold')).pack()

    # Add Employee Form
    Label(ContactForm, text="First Name", font=('arial', 12, 'bold')).grid(row=0, column=0)
    Entry(ContactForm, textvariable=FIRSTNAME, width=30).grid(row=0, column=1)

    Label(ContactForm, text="Last Name", font=('arial', 12, 'bold')).grid(row=1, column=0)
    Entry(ContactForm, textvariable=LASTNAME, width=30).grid(row=1, column=1)

    Label(ContactForm, text="Gender", font=('arial', 12, 'bold')).grid(row=2, column=0)
    RadioGroup.grid(row=2, column=1)
    
    Label(ContactForm, text="Age", font=('arial', 12, 'bold')).grid(row=3, column=0)
    Entry(ContactForm, textvariable=AGE, width=30).grid(row=3, column=1)

    Label(ContactForm, text="Address", font=('arial', 12, 'bold')).grid(row=4, column=0)
    Entry(ContactForm, textvariable=ADDRESS, width=30).grid(row=4, column=1)

    Label(ContactForm, text="Contact No.", font=('arial', 12, 'bold')).grid(row=5, column=0)
    Entry(ContactForm, textvariable=CONTACT, width=30).grid(row=5, column=1)

    Label(ContactForm, text="Department", font=('arial', 12, 'bold')).grid(row=6, column=0)
    Entry(ContactForm, textvariable=DEPARTMENT, width=30).grid(row=6, column=1)

    Label(ContactForm, text="Employment Date", font=('arial', 12, 'bold')).grid(row=7, column=0)
    Entry(ContactForm, textvariable=EMPLOYMENT_DATE, width=30).grid(row=7, column=1)

    Label(ContactForm, text="Nationality", font=('arial', 12, 'bold')).grid(row=8, column=0)
    Entry(ContactForm, textvariable=NATIONALITY, width=30).grid(row=8, column=1)

    Label(ContactForm, text="Marital Status", font=('arial', 12, 'bold')).grid(row=9, column=0)
    RadioGroup2.grid(row=9, column=1)

    # Save and Cancel Buttons
    Button(ContactForm, text="Save", command=save_employee).grid(row=10, column=0, pady=10)
    Button(ContactForm, text="Cancel", command=NewWindow.destroy).grid(row=10, column=1, pady=10)

def save_employee():
    Employee.objects.create(
        firstname=FIRSTNAME.get(),
        lastname=LASTNAME.get(),
        gender=GENDER.get(),
        age=AGE.get(),
        address=ADDRESS.get(),
        contact=CONTACT.get(),
        department=DEPARTMENT.get(),
        employment_date=EMPLOYMENT_DATE.get(),
        nationality=NATIONALITY.get(),
        marital_status=MARITAL_STATUS.get()
    )
    msbx.showinfo("Save Employee", "Employee saved successfully!")
    NewWindow.destroy()

# Placeholder functions
def add_department():
    def save_department():
        try:
            name = department_name_entry.get()
            manager = department_manager_entry.get()
            established_date = department_established_date_entry.get()

            Department.objects.create(
                name=name,
                manager=manager,
                established_date=established_date
            )
            msbx.showinfo("Add Department", "Department added successfully!")
            add_department_window.destroy()
        except Exception as e:
            msbx.showerror("Add Department", f"Error adding department: {e}")

    add_department_window = Toplevel(screen_home)
    add_department_window.title("Add Department")

    Label(add_department_window, text="Name:").pack(pady=5)
    department_name_entry = Entry(add_department_window)
    department_name_entry.pack(pady=5)

    Label(add_department_window, text="Manager:").pack(pady=5)
    department_manager_entry = Entry(add_department_window)
    department_manager_entry.pack(pady=5)

    Label(add_department_window, text="Established Date (YYYY-MM-DD):").pack(pady=5)
    department_established_date_entry = Entry(add_department_window)
    department_established_date_entry.pack(pady=5)

    Button(add_department_window, text="Save", command=save_department).pack(pady=5)
    Button(add_department_window, text="Cancel", command=add_department_window.destroy).pack(pady=5)

def add_internship():
    def save_internship():
        try:
            title = internship_title_entry.get()
            description = internship_description_entry.get()
            start_date = internship_start_date_entry.get()
            end_date = internship_end_date_entry.get()

            # Assuming you have validation and date parsing logic
            Internship.objects.create(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date
            )
            msbx.showinfo("Add Internship", "Internship added successfully!")
            add_internship_window.destroy()
        except Exception as e:
            msbx.showerror("Add Internship", f"Error adding internship: {e}")

    add_internship_window = Toplevel(screen_home)
    add_internship_window.title("Add Internship")

    Label(add_internship_window, text="Title:").pack(pady=5)
    internship_title_entry = Entry(add_internship_window)
    internship_title_entry.pack(pady=5)

    Label(add_internship_window, text="Description:").pack(pady=5)
    internship_description_entry = Entry(add_internship_window)
    internship_description_entry.pack(pady=5)

    Label(add_internship_window, text="Start Date (YYYY-MM-DD):").pack(pady=5)
    internship_start_date_entry = Entry(add_internship_window)
    internship_start_date_entry.pack(pady=5)

    Label(add_internship_window, text="End Date (YYYY-MM-DD):").pack(pady=5)
    internship_end_date_entry = Entry(add_internship_window)
    internship_end_date_entry.pack(pady=5)

    Button(add_internship_window, text="Save", command=save_internship).pack(pady=5)
    Button(add_internship_window, text="Cancel", command=add_internship_window.destroy).pack(pady=5)

def add_event():
    def save_event():
        try:
            title = event_title_entry.get()
            date = event_date_entry.get()
            location = event_location_entry.get()
            description = event_description_entry.get()

            Event.objects.create(
                title=title,
                date=date,
                location=location,
                description=description
            )
            msbx.showinfo("Add Event", "Event added successfully!")
            add_event_window.destroy()
        except Exception as e:
            msbx.showerror("Add Event", f"Error adding event: {e}")

    add_event_window = Toplevel(screen_home)
    add_event_window.title("Add Event")

    Label(add_event_window, text="Title:").pack(pady=5)
    event_title_entry = Entry(add_event_window)
    event_title_entry.pack(pady=5)

    Label(add_event_window, text="Date (YYYY-MM-DD):").pack(pady=5)
    event_date_entry = Entry(add_event_window)
    event_date_entry.pack(pady=5)

    Label(add_event_window, text="Location:").pack(pady=5)
    event_location_entry = Entry(add_event_window)
    event_location_entry.pack(pady=5)

    Label(add_event_window, text="Description:").pack(pady=5)
    event_description_entry = Entry(add_event_window)
    event_description_entry.pack(pady=5)

    Button(add_event_window, text="Save", command=save_event).pack(pady=5)
    Button(add_event_window, text="Cancel", command=add_event_window.destroy).pack(pady=5)

def edit_employee():
    def fetch_employee():
        try:
            first_name = firstname_entry.get()
            last_name = lastname_entry.get()
            # Query by first name and last name
            employee = Employee.objects.get(firstname=first_name, lastname=last_name)
            FIRSTNAME.set(employee.firstname)
            LASTNAME.set(employee.lastname)
            GENDER.set(employee.gender)
            AGE.set(employee.age)
            ADDRESS.set(employee.address)
            CONTACT.set(employee.contact)
            DEPARTMENT.set(employee.department)
            EMPLOYMENT_DATE.set(employee.employment_date)
            NATIONALITY.set(employee.nationality)
            MARITAL_STATUS.set(employee.marital_status)
        except Employee.DoesNotExist:
            msbx.showerror("Edit Employee", "Employee not found!")
        except Exception as e:
            msbx.showerror("Edit Employee", f"Error fetching employee: {e}")

    def save_employee():
        try:
            first_name = firstname_entry.get()
            last_name = lastname_entry.get()
            employee = Employee.objects.get(firstname=first_name, lastname=last_name)
            employee.firstname = FIRSTNAME.get()
            employee.lastname = LASTNAME.get()
            employee.gender = GENDER.get()
            employee.age = AGE.get()
            employee.address = ADDRESS.get()
            employee.contact = CONTACT.get()
            employee.department = DEPARTMENT.get()
            employee.employment_date = EMPLOYMENT_DATE.get()
            employee.nationality = NATIONALITY.get()
            employee.marital_status = MARITAL_STATUS.get()
            employee.save()
            msbx.showinfo("Edit Employee", "Employee updated successfully!")
            edit_employee_window.destroy()
        except Employee.DoesNotExist:
            msbx.showerror("Edit Employee", "Employee not found!")
        except Exception as e:
            msbx.showerror("Edit Employee", f"Error updating employee: {e}")

    edit_employee_window = Toplevel(screen_home)
    edit_employee_window.title("Edit Employee")
    edit_employee_window.geometry("600x400")  # Set a reasonable initial size

    # Initialize StringVar() variables
    FIRSTNAME = StringVar()
    LASTNAME = StringVar()
    AGE = StringVar()
    ADDRESS = StringVar()
    CONTACT = StringVar()
    DEPARTMENT = StringVar()
    EMPLOYMENT_DATE = StringVar()
    NATIONALITY = StringVar()
    GENDER = StringVar()
    MARITAL_STATUS = StringVar()

    # Use grid layout
    Label(edit_employee_window, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    firstname_entry = Entry(edit_employee_window)
    firstname_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Last Name:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    lastname_entry = Entry(edit_employee_window)
    lastname_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to fetch employee details
    Button(edit_employee_window, text="Fetch", command=fetch_employee).grid(row=2, column=0, columnspan=2, pady=10)

    # Rest of the form fields
    Label(edit_employee_window, text="First Name").grid(row=3, column=0, padx=10, pady=5, sticky=W)
    Entry(edit_employee_window, textvariable=FIRSTNAME).grid(row=3, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Last Name").grid(row=4, column=0, padx=10, pady=5, sticky=W)
    Entry(edit_employee_window, textvariable=LASTNAME).grid(row=4, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Age").grid(row=5, column=0, padx=10, pady=5, sticky=W)
    Entry(edit_employee_window, textvariable=AGE).grid(row=5, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Address").grid(row=6, column=0, padx=10, pady=5, sticky=W)
    Entry(edit_employee_window, textvariable=ADDRESS).grid(row=6, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Contact No.").grid(row=7, column=0, padx=10, pady=5, sticky=W)
    Entry(edit_employee_window, textvariable=CONTACT).grid(row=7, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Department").grid(row=8, column=0, padx=10, pady=5, sticky=W)
    Entry(edit_employee_window, textvariable=DEPARTMENT).grid(row=8, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Employment Date").grid(row=9, column=0, padx=10, pady=5, sticky=W)
    Entry(edit_employee_window, textvariable=EMPLOYMENT_DATE).grid(row=9, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Nationality").grid(row=10, column=0, padx=10, pady=5, sticky=W)
    Entry(edit_employee_window, textvariable=NATIONALITY).grid(row=10, column=1, padx=10, pady=5)

    Label(edit_employee_window, text="Gender").grid(row=11, column=0, padx=10, pady=5, sticky=W)
    RadioGroup = Frame(edit_employee_window)
    RadioGroup.grid(row=11, column=1, padx=10, pady=5, sticky=W)
    Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male").pack(side=LEFT, padx=5)
    Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female").pack(side=LEFT, padx=5)

    Label(edit_employee_window, text="Marital Status").grid(row=12, column=0, padx=10, pady=5, sticky=W)
    RadioGroup2 = Frame(edit_employee_window)
    RadioGroup2.grid(row=12, column=1, padx=10, pady=5, sticky=W)
    Radiobutton(RadioGroup2, text="Single", variable=MARITAL_STATUS, value="Single").pack(side=LEFT, padx=5)
    Radiobutton(RadioGroup2, text="Married", variable=MARITAL_STATUS, value="Married").pack(side=LEFT, padx=5)
    Radiobutton(RadioGroup2, text="Divorced", variable=MARITAL_STATUS, value="Divorced").pack(side=LEFT, padx=5)

    # Button to save changes
    Button(edit_employee_window, text="Save", command=save_employee).grid(row=13, column=0, columnspan=2, pady=20)

def edit_interns():
    def fetch_intern():
        try:
            intern = Intern.objects.get(id=intern_id_entry.get())
            if intern:
                name_entry.delete(0, END)
                name_entry.insert(0, intern.name)
                # Populate other fields as needed
        except Intern.DoesNotExist:
            msbx.showwarning("Edit Intern", "Intern not found")

    def save_changes():
        try:
            intern = Intern.objects.get(id=intern_id_entry.get())
            intern.name = name_entry.get()
            # Update other fields as needed
            intern.save()
            msbx.showinfo("Edit Intern", "Intern updated successfully!")
            edit_intern_window.destroy()
        except Intern.DoesNotExist:
            msbx.showwarning("Edit Intern", "Intern not found")

    edit_intern_window = Toplevel(screen_home)
    edit_intern_window.title("Edit Intern")

    Label(edit_intern_window, text="Intern ID:").pack(pady=5)
    intern_id_entry = Entry(edit_intern_window)
    intern_id_entry.pack(pady=5)

    Button(edit_intern_window, text="Fetch", command=fetch_intern).pack(pady=5)

    Label(edit_intern_window, text="Name:").pack(pady=5)
    name_entry = Entry(edit_intern_window)
    name_entry.pack(pady=5)

    # Add other fields as needed

    Button(edit_intern_window, text="Save", command=save_changes).pack(pady=5)
    Button(edit_intern_window, text="Cancel", command=edit_intern_window.destroy).pack(pady=5)

def edit_departments():
    def fetch_department():
        try:
            department = Department.objects.get(id=department_id_entry.get())
            if department:
                name_entry.delete(0, END)
                name_entry.insert(0, department.name)
        except Department.DoesNotExist:
            msbx.showwarning("Edit Department", "Department not found")

    def save_changes():
        try:
            department = Department.objects.get(id=department_id_entry.get())
            department.name = name_entry.get()
            department.save()
            msbx.showinfo("Edit Department", "Department updated successfully!")
            edit_department_window.destroy()
        except Department.DoesNotExist:
            msbx.showwarning("Edit Department", "Department not found")

    edit_department_window = Toplevel(screen_home)
    edit_department_window.title("Edit Department")

    Label(edit_department_window, text="Department ID:").pack(pady=5)
    department_id_entry = Entry(edit_department_window)
    department_id_entry.pack(pady=5)

    Button(edit_department_window, text="Fetch", command=fetch_department).pack(pady=5)

    Label(edit_department_window, text="Name:").pack(pady=5)
    name_entry = Entry(edit_department_window)
    name_entry.pack(pady=5)

    Button(edit_department_window, text="Save", command=save_changes).pack(pady=5)
    Button(edit_department_window, text="Cancel", command=edit_department_window.destroy).pack(pady=5)

def edit_schedule():
    def fetch_schedule():
        try:
            schedule = Schedule.objects.get(id=schedule_id_entry.get())
            if schedule:
                details_entry.delete(0, END)
                details_entry.insert(0, schedule.details)
                # Populate other fields as needed
        except Schedule.DoesNotExist:
            msbx.showwarning("Edit Schedule", "Schedule not found")

    def save_changes():
        try:
            schedule = Schedule.objects.get(id=schedule_id_entry.get())
            schedule.details = details_entry.get()
            # Update other fields as needed
            schedule.save()
            msbx.showinfo("Edit Schedule", "Schedule updated successfully!")
            edit_schedule_window.destroy()
        except Schedule.DoesNotExist:
            msbx.showwarning("Edit Schedule", "Schedule not found")

    edit_schedule_window = Toplevel(screen_home)
    edit_schedule_window.title("Edit Schedule")

    Label(edit_schedule_window, text="Schedule ID:").pack(pady=5)
    schedule_id_entry = Entry(edit_schedule_window)
    schedule_id_entry.pack(pady=5)

    Button(edit_schedule_window, text="Fetch", command=fetch_schedule).pack(pady=5)

    Label(edit_schedule_window, text="Details:").pack(pady=5)
    details_entry = Entry(edit_schedule_window)
    details_entry.pack(pady=5)

    Button(edit_schedule_window, text="Save", command=save_changes).pack(pady=5)
    Button(edit_schedule_window, text="Cancel", command=edit_schedule_window.destroy).pack(pady=5)

def view_employees():
    global view_employees_window
    
    view_employees_window = Toplevel(screen_home)
    view_employees_window.title("View Employees")
    view_employees_window.geometry("800x600")

    # Create a Treeview widget to display employee data
    columns_employee = ("First Name", "Last Name", "Gender", "Age", "Address", "Contact", "Department", "Employment Date", "Nationality", "Marital Status")
    tree_employee_view = ttk.Treeview(view_employees_window, columns=columns_employee, show="headings")
    column_widths = {
    "First Name": 100,
    "Last Name": 100,
    "Gender": 100,
    "Age": 50,
    "Address": 200,
    "Contact": 100,
    "Department": 100,
    "Employment Date": 120,
    "Nationality": 100,
    "Marital Status": 100 }    
    # Define column headings
    for col in columns_employee:
        tree_employee_view.heading(col, text=col)
        tree_employee_view.column(col, width=column_widths.get(col, 100))  # Default width 100
    tree_employee_view.pack(fill=BOTH, expand=True)
    scrollbar = Scrollbar(view_employees_window, orient=HORIZONTAL, command=tree_employee_view.xview)
    scrollbar.pack(side=BOTTOM, fill=X)
    tree_employee_view.configure(xscrollcommand=scrollbar.set)

    # Load data into the Treeview
    try:
        employees = Employee.objects.all()
        for emp in employees:
            tree_employee_view.insert("", "end", values=(emp.firstname, emp.lastname, emp.gender, emp.age, emp.address, emp.contact, emp.department, emp.employment_date, emp.nationality, emp.marital_status))
    except Exception as e:
        msbx.showerror("View Employees", f"Error loading data: {e}")

def view_departments():
    view_window = Toplevel(screen_home)
    view_window.title("View Departments")
    view_window.geometry("600x400+300+100")

    # Create Treeview to display departments
    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Manager", "Established Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Manager", text="Manager")
    tree.heading("Established Date", text="Established Date")
    tree.pack(fill=BOTH, expand=True)

    # Create horizontal scrollbar
    scrollbar = Scrollbar(view_window, orient=HORIZONTAL, command=tree.xview)
    scrollbar.pack(side=BOTTOM, fill=X)

    # Configure the Treeview to use the scrollbar
    tree.configure(xscrollcommand=scrollbar.set)

    # Fetch and insert department data
    for department in Department.objects.all():
        tree.insert('', 'end', values=(department.id, department.name, department.manager, department.established_date))

def view_interns():
    view_window = Toplevel(screen_home)
    view_window.title("View Interns")
    view_window.geometry("600x400+300+100")

    # Create Treeview to display interns
    tree = ttk.Treeview(view_window, columns=("ID", "Title", "Description", "Start Date", "End Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Description", text="Description")
    tree.heading("Start Date", text="Start Date")
    tree.heading("End Date", text="End Date")
    tree.pack(fill=BOTH, expand=True)

    # Create horizontal scrollbar
    scrollbar = Scrollbar(view_window, orient=HORIZONTAL, command=tree.xview)
    scrollbar.pack(side=BOTTOM, fill=X)

    # Configure the Treeview to use the scrollbar
    tree.configure(xscrollcommand=scrollbar.set)

    # Fetch and insert intern data
    for intern in Internship.objects.all():
        tree.insert('', 'end', values=(intern.id, intern.title, intern.description, intern.start_date, intern.end_date))

def view_events():
    view_window = Toplevel(screen_home)
    view_window.title("View Events")
    view_window.geometry("600x400+300+100")

    # Create Treeview to display events
    tree = ttk.Treeview(view_window, columns=("ID", "Title", "Date", "Location", "Description"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Date", text="Date")
    tree.heading("Location", text="Location")
    tree.heading("Description", text="Description")
    tree.pack(fill=BOTH, expand=True)

    # Create horizontal scrollbar
    scrollbar = Scrollbar(view_window, orient=HORIZONTAL, command=tree.xview)
    scrollbar.pack(side=BOTTOM, fill=X)

    # Configure the Treeview to use the scrollbar
    tree.configure(xscrollcommand=scrollbar.set)

    # Fetch and insert event data
    for event in Event.objects.all():
        tree.insert('', 'end', values=(event.id, event.title, event.date, event.location, event.description))

def show_help():
    msbx.showinfo("Date Format Help", "Please enter the date in the format: yyyy-mm-dd.")

# Main program starts here
if __name__ == "__main__":
    login_screen()
