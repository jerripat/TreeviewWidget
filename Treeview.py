from tkinter import *
from tkinter import ttk, messagebox
import logic


# --------------------------------
# Main Window
# --------------------------------

root = Tk()
root.title("User Records")
root.geometry("850x550")
root.minsize(750, 450)


# Stores the database ID of the user
# currently loaded into the main form.
selected_user_id = None


# --------------------------------
# Insert Treeview Row
# --------------------------------

def insert_tree_row(values):
    row_number = len(tree.get_children())

    if row_number % 2 == 0:
        row_tag = "evenrow"
    else:
        row_tag = "oddrow"

    tree.insert(
        "",
        END,
        values=values,
        tags=(row_tag,)
    )


# --------------------------------
# Refresh Alternating Row Colors
# --------------------------------

def refresh_row_colors():
    rows = tree.get_children()

    for index, item in enumerate(rows):
        if index % 2 == 0:
            tree.item(
                item,
                tags=("evenrow",)
            )
        else:
            tree.item(
                item,
                tags=("oddrow",)
            )


# --------------------------------
# Clear User Form
# --------------------------------

def clear_form():
    global selected_user_id

    selected_user_id = None

    entryName.delete(0, END)
    entryAge.delete(0, END)

    gender_var.set("Male")

    btnUpdate.config(
        state=DISABLED
    )

    tree.selection_remove(
        tree.selection()
    )

    entryName.focus()


# --------------------------------
# Validate User Form
# --------------------------------

def validate_user_form():
    name = entryName.get().strip()
    gender = gender_var.get().strip()
    age_text = entryAge.get().strip()

    if not name or not gender or not age_text:
        messagebox.showerror(
            "Missing Information",
            "Please enter a name, gender, and age."
        )
        return None

    try:
        age = int(age_text)

        if age <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Age",
            "Age must be a positive whole number."
        )

        entryAge.focus()
        return None

    return name, gender, age


# --------------------------------
# Add User
# --------------------------------

def add_user():
    user_data = validate_user_form()

    if user_data is None:
        return

    name, gender, age = user_data

    try:
        user_id = logic.add_to_database(
            name,
            gender,
            age
        )

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to save the user.\n\n{error}"
        )
        return

    insert_tree_row(
        (
            user_id,
            name,
            gender,
            age
        )
    )

    clear_form()


# --------------------------------
# Update Selected User
# --------------------------------

def update_selected_user():
    global selected_user_id

    if selected_user_id is None:
        messagebox.showerror(
            "No User Selected",
            "Please select a user to update."
        )
        return

    user_data = validate_user_form()

    if user_data is None:
        return

    name, gender, age = user_data

    try:
        logic.update_user(
            selected_user_id,
            name,
            gender,
            age
        )

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to update the user.\n\n{error}"
        )
        return

    load_users()
    clear_form()

    messagebox.showinfo(
        "User Updated",
        "The user was updated successfully."
    )


# --------------------------------
# Fill Form From Selected Row
# --------------------------------

def fill_form_from_tree(event=None):
    global selected_user_id

    selected_items = tree.selection()

    if not selected_items:
        return

    selected_item = selected_items[0]

    row_data = tree.item(
        selected_item,
        "values"
    )

    if not row_data:
        return

    selected_user_id = int(row_data[0])

    name = row_data[1]
    gender = row_data[2]
    age = row_data[3]

    entryName.delete(0, END)
    entryName.insert(0, name)

    gender_var.set(gender)

    entryAge.delete(0, END)
    entryAge.insert(0, age)

    btnUpdate.config(
        state=NORMAL
    )


# --------------------------------
# Load Users From Database
# --------------------------------

def load_users():
    for item in tree.get_children():
        tree.delete(item)

    try:
        users = logic.getData()

        for user in users:
            insert_tree_row(user)

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to load users.\n\n{error}"
        )


# --------------------------------
# Save Charge
# --------------------------------

def save_charge(
    user_id,
    charge_entry,
    description_entry,
    charges_tree,
    charges_window
):
    charge_text = charge_entry.get().strip()
    description = description_entry.get().strip()

    if not charge_text or not description:
        messagebox.showerror(
            "Missing Information",
            "Please enter a charge and description.",
            parent=charges_window
        )
        return

    try:
        charge = float(charge_text)

        if charge <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Charge",
            "The charge must be a positive number.",
            parent=charges_window
        )

        charge_entry.focus()
        return

    try:
        logic.add_charge(
            user_id,
            charge,
            description
        )

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to save the charge.\n\n{error}",
            parent=charges_window
        )
        return

    load_charges(
        user_id,
        charges_tree,
        charges_window
    )

    charge_entry.delete(0, END)
    description_entry.delete(0, END)

    charge_entry.focus()


# --------------------------------
# Load Charges for Selected User
# --------------------------------

def load_charges(
    user_id,
    charges_tree,
    charges_window
):
    for item in charges_tree.get_children():
        charges_tree.delete(item)

    try:
        charges = logic.get_charges(
            user_id
        )

        for index, charge in enumerate(charges):
            charge_id = charge[0]
            amount = charge[1]
            description = charge[2]

            if index % 2 == 0:
                row_tag = "evenrow"
            else:
                row_tag = "oddrow"

            charges_tree.insert(
                "",
                END,
                values=(
                    charge_id,
                    f"${float(amount):.2f}",
                    description
                ),
                tags=(row_tag,)
            )

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to load charges.\n\n{error}",
            parent=charges_window
        )


# --------------------------------
# Show Total Charges
# --------------------------------

def show_total_charges(
    user_id,
    charges_window
):
    try:
        total = logic.get_total_charges(
            user_id
        )

        messagebox.showinfo(
            "Total Charges",
            f"Total charges: ${total:.2f}",
            parent=charges_window
        )

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to calculate total charges.\n\n{error}",
            parent=charges_window
        )


# --------------------------------
# Open Charges Window
# --------------------------------

def open_charges(user_id, name):
    charges_window = Toplevel(root)

    charges_window.title(
        f"Charges - {name}"
    )

    charges_window.geometry(
        "650x500"
    )

    charges_window.minsize(
        550,
        400
    )

    charges_window.transient(root)


    # --------------------------------
    # Selected User Information
    # --------------------------------

    user_frame = Frame(
        charges_window
    )

    user_frame.pack(
        fill=X,
        padx=20,
        pady=(20, 10)
    )

    lblSelectedUser = Label(
        user_frame,
        text=f"User ID: {user_id}    Name: {name}",
        font=("Arial", 13, "bold")
    )

    lblSelectedUser.pack(
        anchor=W
    )


    # --------------------------------
    # Charge Entry Form
    # --------------------------------

    charge_form = Frame(
        charges_window
    )

    charge_form.pack(
        fill=X,
        padx=20,
        pady=10
    )

    charge_form.columnconfigure(
        1,
        weight=1
    )


    # Charge
    lblCharge = Label(
        charge_form,
        text="Charge:"
    )

    lblCharge.grid(
        row=0,
        column=0,
        padx=(0, 10),
        pady=5,
        sticky=E
    )

    entryCharge = Entry(
        charge_form
    )

    entryCharge.grid(
        row=0,
        column=1,
        padx=(0, 15),
        pady=5,
        sticky=EW
    )


    # Description
    lblDescription = Label(
        charge_form,
        text="Description:"
    )

    lblDescription.grid(
        row=1,
        column=0,
        padx=(0, 10),
        pady=5,
        sticky=E
    )

    entryDescription = Entry(
        charge_form
    )

    entryDescription.grid(
        row=1,
        column=1,
        padx=(0, 15),
        pady=5,
        sticky=EW
    )


    # --------------------------------
    # Charges Treeview Frame
    # --------------------------------

    charges_tree_frame = Frame(
        charges_window
    )

    charges_tree_frame.pack(
        fill=BOTH,
        expand=True,
        padx=20,
        pady=10
    )


    charges_scrollbar = Scrollbar(
        charges_tree_frame,
        orient=VERTICAL
    )

    charges_scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    charges_tree = ttk.Treeview(
        charges_tree_frame,
        columns=(
            "ID",
            "Charge",
            "Description"
        ),
        show="headings",
        selectmode="browse",
        yscrollcommand=charges_scrollbar.set
    )

    charges_scrollbar.config(
        command=charges_tree.yview
    )


    # Charges headings
    charges_tree.heading(
        "ID",
        text="ID"
    )

    charges_tree.heading(
        "Charge",
        text="Charge"
    )

    charges_tree.heading(
        "Description",
        text="Description"
    )


    # Charges columns
    charges_tree.column(
        "ID",
        width=60,
        minwidth=50,
        anchor=CENTER,
        stretch=False
    )

    charges_tree.column(
        "Charge",
        width=100,
        minwidth=80,
        anchor=CENTER,
        stretch=False
    )

    charges_tree.column(
        "Description",
        width=350,
        minwidth=150,
        anchor=W,
        stretch=True
    )

    charges_tree.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )


    # Alternating charge row colors
    charges_tree.tag_configure(
        "evenrow",
        background="#E8E8E8"
    )

    charges_tree.tag_configure(
        "oddrow",
        background="#FFFFFF"
    )


    # --------------------------------
    # Charge Buttons
    # --------------------------------

    button_frame = Frame(
        charges_window
    )

    button_frame.pack(
        pady=(0, 20)
    )


    btnSaveCharge = Button(
        button_frame,
        text="Save Charge",
        width=14,
        command=lambda: save_charge(
            user_id,
            entryCharge,
            entryDescription,
            charges_tree,
            charges_window
        )
    )

    btnSaveCharge.pack(
        side=LEFT,
        padx=5
    )


    btnShowTotalCharges = Button(
        button_frame,
        text="Show Total Charges",
        width=18,
        command=lambda: show_total_charges(
            user_id,
            charges_window
        )
    )

    btnShowTotalCharges.pack(
        side=LEFT,
        padx=5
    )


    btnClose = Button(
        button_frame,
        text="Close",
        width=14,
        command=charges_window.destroy
    )

    btnClose.pack(
        side=LEFT,
        padx=5
    )


    # Press Enter from description
    # to save the charge.
    entryDescription.bind(
        "<Return>",
        lambda event: save_charge(
            user_id,
            entryCharge,
            entryDescription,
            charges_tree,
            charges_window
        )
    )


    load_charges(
        user_id,
        charges_tree,
        charges_window
    )

    entryCharge.focus()


    # Wait until the window is visible
    # before making it modal.
    charges_window.update_idletasks()
    charges_window.wait_visibility()
    charges_window.grab_set()


# --------------------------------
# Open Charges From Double-Click
# --------------------------------

def open_selected_user_charges(event=None):
    selected_item = tree.identify_row(
        event.y
    )

    if not selected_item:
        return

    tree.selection_set(
        selected_item
    )

    tree.focus(
        selected_item
    )

    row_data = tree.item(
        selected_item,
        "values"
    )

    if not row_data:
        return

    user_id = int(row_data[0])
    name = row_data[1]

    open_charges(
        user_id,
        name
    )


# --------------------------------
# Open Charges From Selected Row
# --------------------------------

def add_charge():
    selected_items = tree.selection()

    if not selected_items:
        messagebox.showerror(
            "No User Selected",
            "Please select a user to add a charge."
        )
        return

    selected_item = selected_items[0]

    row_data = tree.item(
        selected_item,
        "values"
    )

    if not row_data:
        messagebox.showerror(
            "No User Selected",
            "Please select a user to add a charge."
        )
        return

    user_id = int(row_data[0])
    name = row_data[1]

    open_charges(
        user_id,
        name
    )


# --------------------------------
# Input Form
# --------------------------------

form_frame = Frame(root)

form_frame.pack(
    fill=X,
    padx=20,
    pady=20
)

form_frame.columnconfigure(
    1,
    weight=1
)


# Name
lblName = Label(
    form_frame,
    text="Name:"
)

lblName.grid(
    row=0,
    column=0,
    padx=(0, 5),
    pady=5,
    sticky=E
)

entryName = Entry(
    form_frame,
    width=20
)

entryName.grid(
    row=0,
    column=1,
    padx=(0, 15),
    pady=5,
    sticky=EW
)


# Gender
lblGender = Label(
    form_frame,
    text="Gender:"
)

lblGender.grid(
    row=0,
    column=2,
    padx=(0, 5),
    pady=5,
    sticky=E
)

gender_var = StringVar(
    value="Male"
)

comboGender = ttk.Combobox(
    form_frame,
    textvariable=gender_var,
    values=(
        "Male",
        "Female",
        "Other"
    ),
    state="readonly",
    width=12
)

comboGender.grid(
    row=0,
    column=3,
    padx=(0, 15),
    pady=5
)


# Age
lblAge = Label(
    form_frame,
    text="Age:"
)

lblAge.grid(
    row=0,
    column=4,
    padx=(0, 5),
    pady=5,
    sticky=E
)

entryAge = Entry(
    form_frame,
    width=8
)

entryAge.grid(
    row=0,
    column=5,
    padx=(0, 15),
    pady=5
)


# --------------------------------
# Main Form Buttons
# --------------------------------

button_form_frame = Frame(
    root
)

button_form_frame.pack(
    fill=X,
    padx=20,
    pady=(0, 15)
)


btnSubmit = Button(
    button_form_frame,
    text="Add User",
    width=14,
    command=add_user
)

btnSubmit.pack(
    side=LEFT,
    padx=(0, 5)
)


btnUpdate = Button(
    button_form_frame,
    text="Update User",
    width=14,
    command=update_selected_user,
    state=DISABLED
)

btnUpdate.pack(
    side=LEFT,
    padx=5
)


btnClear = Button(
    button_form_frame,
    text="Clear",
    width=14,
    command=clear_form
)

btnClear.pack(
    side=LEFT,
    padx=5
)


btnCharges = Button(
    button_form_frame,
    text="Open Charges",
    width=14,
    command=add_charge
)

btnCharges.pack(
    side=LEFT,
    padx=5
)


# --------------------------------
# Treeview Frame
# --------------------------------

tree_frame = Frame(root)

tree_frame.pack(
    fill=BOTH,
    expand=True,
    padx=20,
    pady=(0, 20)
)


# --------------------------------
# Scrollbars
# --------------------------------

vertical_scrollbar = Scrollbar(
    tree_frame,
    orient=VERTICAL
)

vertical_scrollbar.pack(
    side=RIGHT,
    fill=Y
)


horizontal_scrollbar = Scrollbar(
    tree_frame,
    orient=HORIZONTAL
)

horizontal_scrollbar.pack(
    side=BOTTOM,
    fill=X
)


# --------------------------------
# Main Treeview
# --------------------------------

tree = ttk.Treeview(
    tree_frame,
    columns=(
        "ID",
        "Name",
        "Gender",
        "Age"
    ),
    show="headings",
    selectmode="browse",
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


vertical_scrollbar.config(
    command=tree.yview
)

horizontal_scrollbar.config(
    command=tree.xview
)


# Headings
tree.heading(
    "ID",
    text="ID"
)

tree.heading(
    "Name",
    text="Name"
)

tree.heading(
    "Gender",
    text="Gender"
)

tree.heading(
    "Age",
    text="Age"
)


# Columns
tree.column(
    "ID",
    width=70,
    minwidth=60,
    anchor=CENTER,
    stretch=False
)

tree.column(
    "Name",
    width=280,
    minwidth=150,
    anchor=W,
    stretch=True
)

tree.column(
    "Gender",
    width=140,
    minwidth=100,
    anchor=CENTER
)

tree.column(
    "Age",
    width=100,
    minwidth=70,
    anchor=CENTER
)


tree.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)


# --------------------------------
# Alternating Row Colors
# --------------------------------

tree.tag_configure(
    "evenrow",
    background="#E8E8E8"
)

tree.tag_configure(
    "oddrow",
    background="#FFFFFF"
)


# --------------------------------
# Event Bindings
# --------------------------------

# Single-click fills the main form.
tree.bind(
    "<<TreeviewSelect>>",
    fill_form_from_tree
)

# Double-click opens the Charges window.
tree.bind(
    "<Double-1>",
    open_selected_user_charges
)

# Press Enter from the Age field
# to add a new user.
entryAge.bind(
    "<Return>",
    lambda event: add_user()
)


# --------------------------------
# Start Program
# --------------------------------

load_users()
entryName.focus()
root.mainloop()