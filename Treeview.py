from tkinter import *
from tkinter import ttk, messagebox
import logic


# --------------------------------
# Main Window
# --------------------------------

root = Tk()
root.title("User Records")
root.geometry("700x500")
root.minsize(650, 400)


# --------------------------------
# Insert a Treeview Row
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
    entryName.delete(0, END)
    entryAge.delete(0, END)
    gender_var.set("Male")
    entryName.focus()


# --------------------------------
# Add User
# --------------------------------

def add_user():
    name = entryName.get().strip()
    gender = gender_var.get().strip()
    age_text = entryAge.get().strip()

    if not name or not gender or not age_text:
        messagebox.showerror(
            "Missing Information",
            "Please enter a name, gender, and age."
        )
        return

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
        return

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
        charge_id = logic.add_charge(
            user_id,
            charge,
            description
        )

    except AttributeError:
        messagebox.showerror(
            "Missing Function",
            "The add_charge() function is missing from logic.py.",
            parent=charges_window
        )
        return

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to save the charge.\n\n{error}",
            parent=charges_window
        )
        return

    charges_tree.insert(
        "",
        END,
        values=(
            charge_id,
            f"${charge:.2f}",
            description
        )
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
        charges = logic.get_charges(user_id)

        for charge in charges:
            charge_id = charge[0]
            amount = charge[1]
            description = charge[2]

            charges_tree.insert(
                "",
                END,
                values=(
                    charge_id,
                    f"${float(amount):.2f}",
                    description
                )
            )

    except AttributeError:
        # The window can still open if get_charges()
        # has not been created yet in logic.py.
        return

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to load charges.\n\n{error}",
            parent=charges_window
        )

# --------------------------------
# Show Total Charges
# --------------------------------

def show_total_charges(user_id, charges_window):
    try:
        total = logic.get_total_charges(user_id)

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
    charges_window.title(f"Charges - {name}")
    charges_window.geometry("600x500")
    charges_window.minsize(500, 400)

    charges_window.transient(root)

    # --------------------------------
    # Selected User
    # --------------------------------

    user_frame = Frame(charges_window)
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

    charge_form = Frame(charges_window)
    charge_form.pack(
        fill=X,
        padx=20,
        pady=10
    )

    charge_form.columnconfigure(
        1,
        weight=1
    )

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

    charges_tree_frame = Frame(charges_window)
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
        width=300,
        minwidth=150,
        anchor=W,
        stretch=True
    )

    charges_tree.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )

    # --------------------------------
    # Buttons
    # --------------------------------

    button_frame = Frame(charges_window)
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

    btnShowSumOfCharges = Button(
        button_frame,
        text="Show Total Charges",
        width=18,
        command=lambda: show_total_charges(user_id, charges_window)
    )
    btnShowSumOfCharges.pack(
        side=LEFT,
        padx=5
    )
    # Press Enter while in the description field
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

    # Wait until the Toplevel window is visible
    # before making it modal.
    charges_window.update_idletasks()
    charges_window.wait_visibility()
    charges_window.grab_set()


# --------------------------------
# Open Charges for Double-Clicked Row
# --------------------------------

def open_selected_user_charges(event=None):
    # Get the row under the mouse pointer.
    selected_item = tree.identify_row(event.y)

    if not selected_item:
        return

    # Select the row that was double-clicked.
    tree.selection_set(selected_item)
    tree.focus(selected_item)

    row_data = tree.item(
        selected_item,
        "values"
    )

    if not row_data:
        return

    user_id = row_data[0]
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


# Add User Button
btnSubmit = Button(
    form_frame,
    text="Add User",
    command=add_user
)
btnSubmit.grid(
    row=0,
    column=6,
    padx=5,
    pady=5
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

tree.bind(
    "<Double-1>",
    open_selected_user_charges
)

entryAge.bind(
    "<Return>",
    lambda event: add_user()
)

def add_charge():
    selected_item = tree.focus()

    if not selected_item:
        messagebox.showerror(
            "No User Selected",
            "Please select a user to add a charge."
        )
        return

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

    user_id = row_data[0]
    name = row_data[1]

    open_charges(
        user_id,
        name
    )
# --------------------------------
# Start Program
# --------------------------------

load_users()
entryName.focus()
root.mainloop()