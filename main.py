```python
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================================
# COLORS
# ==========================================================

BG = "#F4F7FB"
WHITE = "#FFFFFF"
DARK = "#172033"
TEXT = "#374151"
MUTED = "#6B7280"

BLUE = "#2563EB"
GREEN = "#16A34A"
RED = "#DC2626"
ORANGE = "#F59E0B"
PURPLE = "#7C3AED"
CYAN = "#0891B2"

LIGHT_BLUE = "#EFF6FF"
LIGHT_GREEN = "#ECFDF5"
LIGHT_RED = "#FEF2F2"
LIGHT_ORANGE = "#FFFBEB"


# ==========================================================
# STUDENT DATA
# ==========================================================

students = {
    "S001": {
        "name": "Rahul Sharma",
        "age": 20,
        "gender": "Male",
        "course": "BCA",
        "marks": 85
    },

    "S002": {
        "name": "Priya Patel",
        "age": 19,
        "gender": "Female",
        "course": "BBA",
        "marks": 92
    },

    "S003": {
        "name": "Aman Khan",
        "age": 21,
        "gender": "Male",
        "course": "BSc",
        "marks": 74
    },

    "S004": {
        "name": "Sneha Verma",
        "age": 20,
        "gender": "Female",
        "course": "BCA",
        "marks": 88
    }
}


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title("Student Record Management System")

root.geometry("1250x800")

root.minsize(1050, 700)

root.configure(bg=BG)


# ==========================================================
# STYLE
# ==========================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass


style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=38,
    fieldbackground=WHITE,
    font=("Arial", 10)
)


style.configure(
    "Treeview.Heading",
    background=DARK,
    foreground=WHITE,
    font=("Arial", 10, "bold"),
    padding=10
)


style.map(
    "Treeview",
    background=[
        ("selected", "#DBEAFE")
    ],
    foreground=[
        ("selected", DARK)
    ]
)


style.configure(
    "TEntry",
    padding=8,
    font=("Arial", 10)
)


style.configure(
    "TCombobox",
    padding=7,
    font=("Arial", 10)
)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def create_button(parent, text, command, color, width=13):

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        width=width,
        height=2
    )

    return button


def get_grade(marks):

    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


def get_status(marks):

    if marks >= 40:
        return "Passed"

    return "Failed"


def get_average_marks():

    if not students:
        return 0

    return sum(
        student["marks"]
        for student in students.values()
    ) / len(students)


def get_passed_count():

    return sum(
        1
        for student in students.values()
        if student["marks"] >= 40
    )


def get_failed_count():

    return sum(
        1
        for student in students.values()
        if student["marks"] < 40
    )


# ==========================================================
# STATUS MESSAGE
# ==========================================================

def show_status(message, color=GREEN):

    status_label.config(
        text=message,
        fg=color
    )


# ==========================================================
# UPDATE DASHBOARD
# ==========================================================

def update_dashboard():

    total_students_label.config(
        text=str(len(students))
    )

    passed_label.config(
        text=str(get_passed_count())
    )

    failed_label.config(
        text=str(get_failed_count())
    )

    average_label.config(
        text=f"{get_average_marks():.1f}%"
    )


# ==========================================================
# CLEAR FIELDS
# ==========================================================

def clear_fields():

    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)

    gender_combo.set("")
    course_combo.set("")

    entry_marks.delete(0, tk.END)

    entry_id.focus()


# ==========================================================
# GET INPUT VALUES
# ==========================================================

def get_input_values():

    student_id = entry_id.get().strip()
    name = entry_name.get().strip()

    try:
        age = int(entry_age.get())
    except ValueError:
        age = 0

    gender = gender_combo.get()
    course = course_combo.get()

    try:
        marks = float(entry_marks.get())
    except ValueError:
        marks = -1

    return (
        student_id,
        name,
        age,
        gender,
        course,
        marks
    )


# ==========================================================
# REFRESH TABLE
# ==========================================================

def refresh_table(data=None):

    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        data = students

    for student_id, student in data.items():

        marks = student["marks"]

        grade = get_grade(marks)

        status = get_status(marks)

        if status == "Passed":
            tag = "passed"
        else:
            tag = "failed"

        tree.insert(
            "",
            tk.END,
            values=(
                student_id,
                student["name"],
                student["age"],
                student["gender"],
                student["course"],
                f"{marks:.1f}%",
                grade,
                status
            ),
            tags=(tag,)
        )

    update_dashboard()


# ==========================================================
# ADD STUDENT
# ==========================================================

def add_student():

    (
        student_id,
        name,
        age,
        gender,
        course,
        marks
    ) = get_input_values()


    if not student_id:

        messagebox.showerror(
            "Missing Student ID",
            "Please enter a Student ID."
        )

        return


    if not name:

        messagebox.showerror(
            "Missing Name",
            "Please enter the student's name."
        )

        return


    if age <= 0 or age > 100:

        messagebox.showerror(
            "Invalid Age",
            "Please enter a valid age."
        )

        return


    if not gender:

        messagebox.showerror(
            "Missing Gender",
            "Please select gender."
        )

        return


    if not course:

        messagebox.showerror(
            "Missing Course",
            "Please select a course."
        )

        return


    if marks < 0 or marks > 100:

        messagebox.showerror(
            "Invalid Marks",
            "Marks must be between 0 and 100."
        )

        return


    if student_id in students:

        messagebox.showerror(
            "Duplicate Student",
            f"Student ID {student_id} already exists."
        )

        return


    students[student_id] = {
        "name": name,
        "age": age,
        "gender": gender,
        "course": course,
        "marks": marks
    }


    refresh_table()

    clear_fields()

    show_status(
        f"✓ Student {name} added successfully!",
        GREEN
    )


# ==========================================================
# UPDATE STUDENT
# ==========================================================

def update_student():

    (
        student_id,
        name,
        age,
        gender,
        course,
        marks
    ) = get_input_values()


    if student_id not in students:

        messagebox.showerror(
            "Student Not Found",
            f"Student ID {student_id} was not found."
        )

        return


    if not name:

        messagebox.showerror(
            "Invalid Name",
            "Please enter the student's name."
        )

        return


    if age <= 0 or age > 100:

        messagebox.showerror(
            "Invalid Age",
            "Please enter a valid age."
        )

        return


    if not gender or not course:

        messagebox.showerror(
            "Missing Information",
            "Please select gender and course."
        )

        return


    if marks < 0 or marks > 100:

        messagebox.showerror(
            "Invalid Marks",
            "Marks must be between 0 and 100."
        )

        return


    students[student_id].update({
        "name": name,
        "age": age,
        "gender": gender,
        "course": course,
        "marks": marks
    })


    refresh_table()

    clear_fields()

    show_status(
        f"✓ Student {student_id} updated successfully!",
        BLUE
    )


# ==========================================================
# DELETE STUDENT
# ==========================================================

def delete_student():

    student_id = entry_id.get().strip()


    if not student_id:

        messagebox.showerror(
            "Missing Student ID",
            "Please enter a Student ID."
        )

        return


    if student_id not in students:

        messagebox.showerror(
            "Student Not Found",
            f"Student ID {student_id} was not found."
        )

        return


    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete {student_id}?"
    )


    if not confirm:
        return


    del students[student_id]


    refresh_table()

    clear_fields()


    show_status(
        f"✓ Student {student_id} deleted.",
        RED
    )


# ==========================================================
# SEARCH STUDENT
# ==========================================================

def search_student():

    search_text = entry_search.get().strip().lower()


    if not search_text:

        refresh_table()

        show_status(
            "Showing all students.",
            TEXT
        )

        return


    filtered = {}


    for student_id, student in students.items():

        if (
            search_text in student_id.lower()
            or search_text in student["name"].lower()
            or search_text in student["course"].lower()
            or search_text in student["gender"].lower()
        ):

            filtered[student_id] = student


    refresh_table(filtered)


    if filtered:

        show_status(
            f"✓ Found {len(filtered)} student(s).",
            BLUE
        )

    else:

        show_status(
            f"✕ No student found for '{search_text}'.",
            RED
        )


# ==========================================================
# SHOW ALL
# ==========================================================

def show_all():

    entry_search.delete(0, tk.END)

    refresh_table()

    show_status(
        f"Showing all {len(students)} students.",
        TEXT
    )


# ==========================================================
# FILTER BY COURSE
# ==========================================================

def filter_course():

    selected_course = filter_course_combo.get()


    if selected_course == "All":

        refresh_table()

        return


    filtered = {}


    for student_id, student in students.items():

        if student["course"] == selected_course:

            filtered[student_id] = student


    refresh_table(filtered)


    show_status(
        f"Showing {len(filtered)} student(s) from {selected_course}.",
        PURPLE
    )


# ==========================================================
# SELECT STUDENT FROM TABLE
# ==========================================================

def select_student(event):

    selected = tree.selection()


    if not selected:
        return


    item = tree.item(selected[0])

    values = item["values"]


    if not values:
        return


    student_id = values[0]


    if student_id not in students:
        return


    student = students[student_id]


    clear_fields()


    entry_id.insert(
        0,
        student_id
    )

    entry_name.insert(
        0,
        student["name"]
    )

    entry_age.insert(
        0,
        student["age"]
    )

    gender_combo.set(
        student["gender"]
    )

    course_combo.set(
        student["course"]
    )

    entry_marks.insert(
        0,
        student["marks"]
    )


# ==========================================================
# HEADER
# ==========================================================

header = tk.Frame(
    root,
    bg=DARK,
    height=100
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title = tk.Label(
    header,
    text="🎓  STUDENT RECORDS",
    font=("Arial", 25, "bold"),
    bg=DARK,
    fg=WHITE
)

title.pack(
    side="left",
    padx=35,
    pady=18
)


subtitle = tk.Label(
    header,
    text="Student Management Dashboard",
    font=("Arial", 11),
    bg=DARK,
    fg="#CBD5E1"
)

subtitle.pack(
    side="left"
)


# ==========================================================
# DASHBOARD CARDS
# ==========================================================

cards_frame = tk.Frame(
    root,
    bg=BG
)

cards_frame.pack(
    fill="x",
    padx=30,
    pady=20
)


def create_card(parent, title, value, color):

    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground="#E5E7EB",
        highlightthickness=1
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=7
    )


    bar = tk.Frame(
        card,
        bg=color,
        width=6
    )

    bar.pack(
        side="left",
        fill="y"
    )


    content = tk.Frame(
        card,
        bg=WHITE
    )

    content.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=12
    )


    tk.Label(
        content,
        text=title,
        font=("Arial", 9, "bold"),
        bg=WHITE,
        fg=MUTED
    ).pack(
        anchor="w"
    )


    value_label = tk.Label(
        content,
        text=value,
        font=("Arial", 22, "bold"),
        bg=WHITE,
        fg=DARK
    )

    value_label.pack(
        anchor="w",
        pady=(5, 0)
    )


    return value_label


total_students_label = create_card(
    cards_frame,
    "TOTAL STUDENTS",
    "0",
    BLUE
)


passed_label = create_card(
    cards_frame,
    "PASSED",
    "0",
    GREEN
)


failed_label = create_card(
    cards_frame,
    "FAILED",
    "0",
    RED
)


average_label = create_card(
    cards_frame,
    "AVERAGE MARKS",
    "0%",
    PURPLE
)


# ==========================================================
# STUDENT FORM
# ==========================================================

form_container = tk.Frame(
    root,
    bg=WHITE,
    highlightbackground="#E5E7EB",
    highlightthickness=1
)

form_container.pack(
    fill="x",
    padx=30,
    pady=5
)


form_title = tk.Label(
    form_container,
    text="Student Information",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    fg=DARK
)

form_title.grid(
    row=0,
    column=0,
    columnspan=6,
    sticky="w",
    padx=20,
    pady=(15, 10)
)


# -------------------------
# ROW 1
# -------------------------

tk.Label(
    form_container,
    text="Student ID",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=1,
    column=0,
    padx=(20, 5),
    pady=7,
    sticky="w"
)


tk.Label(
    form_container,
    text="Student Name",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=1,
    column=2,
    padx=(20, 5),
    pady=7,
    sticky="w"
)


tk.Label(
    form_container,
    text="Age",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=1,
    column=4,
    padx=(20, 5),
    pady=7,
    sticky="w"
)


entry_id = ttk.Entry(
    form_container,
    width=20
)

entry_id.grid(
    row=2,
    column=0,
    padx=(20, 10),
    pady=(0, 12)
)


entry_name = ttk.Entry(
    form_container,
    width=25
)

entry_name.grid(
    row=2,
    column=2,
    padx=(20, 10),
    pady=(0, 12)
)


entry_age = ttk.Entry(
    form_container,
    width=15
)

entry_age.grid(
    row=2,
    column=4,
    padx=(20, 20),
    pady=(0, 12)
)


# -------------------------
# ROW 2
# -------------------------

tk.Label(
    form_container,
    text="Gender",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=3,
    column=0,
    padx=(20, 5),
    pady=7,
    sticky="w"
)


tk.Label(
    form_container,
    text="Course",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=3,
    column=2,
    padx=(20, 5),
    pady=7,
    sticky="w"
)


tk.Label(
    form_container,
    text="Marks (%)",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=3,
    column=4,
    padx=(20, 5),
    pady=7,
    sticky="w"
)


gender_combo = ttk.Combobox(
    form_container,
    values=["Male", "Female", "Other"],
    width=18,
    state="readonly"
)

gender_combo.grid(
    row=4,
    column=0,
    padx=(20, 10),
    pady=(0, 15)
)


course_combo = ttk.Combobox(
    form_container,
    values=[
        "BCA",
        "BBA",
        "BSc",
        "BCom",
        "BA",
        "BTech",
        "MCA",
        "MBA",
        "MSc"
    ],
    width=23,
    state="readonly"
)

course_combo.grid(
    row=4,
    column=2,
    padx=(20, 10),
    pady=(0, 15)
)


entry_marks = ttk.Entry(
    form_container,
    width=15
)

entry_marks.grid(
    row=4,
    column=4,
    padx=(20, 20),
    pady=(0, 15)
)


# ==========================================================
# ACTION BUTTONS
# ==========================================================

actions = tk.Frame(
    root,
    bg=BG
)

actions.pack(
    pady=15
)


create_button(
    actions,
    "＋ Add Student",
    add_student,
    GREEN,
    15
).pack(
    side="left",
    padx=5
)


create_button(
    actions,
    "✎ Update",
    update_student,
    BLUE,
    13
).pack(
    side="left",
    padx=5
)


create_button(
    actions,
    "✕ Delete",
    delete_student,
    RED,
    13
).pack(
    side="left",
    padx=5
)


create_button(
    actions,
    "Clear Fields",
    clear_fields,
    ORANGE,
    14
).pack(
    side="left",
    padx=5
)


# ==========================================================
# SEARCH AND FILTER
# ==========================================================

search_container = tk.Frame(
    root,
    bg=WHITE,
    highlightbackground="#E5E7EB",
    highlightthickness=1
)

search_container.pack(
    fill="x",
    padx=30,
    pady=(0, 10)
)


tk.Label(
    search_container,
    text="🔍 Search",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=DARK
).pack(
    side="left",
    padx=(15, 8),
    pady=12
)


entry_search = ttk.Entry(
    search_container,
    width=35
)

entry_search.pack(
    side="left",
    padx=5,
    pady=12
)


create_button(
    search_container,
    "Search",
    search_student,
    BLUE,
    11
).pack(
    side="left",
    padx=5,
    pady=5
)


create_button(
    search_container,
    "Show All",
    show_all,
    DARK,
    11
).pack(
    side="left",
    padx=5,
    pady=5
)


tk.Label(
    search_container,
    text="Course:",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(
    side="left",
    padx=(25, 5)
)


filter_course_combo = ttk.Combobox(
    search_container,
    values=[
        "All",
        "BCA",
        "BBA",
        "BSc",
        "BCom",
        "BA",
        "BTech",
        "MCA",
        "MBA",
        "MSc"
    ],
    width=12,
    state="readonly"
)

filter_course_combo.set("All")

filter_course_combo.pack(
    side="left",
    padx=5
)


filter_course_combo.bind(
    "<<ComboboxSelected>>",
    lambda event: filter_course()
)


# ==========================================================
# TABLE
# ==========================================================

table_container = tk.Frame(
    root,
    bg=WHITE,
    highlightbackground="#E5E7EB",
    highlightthickness=1
)

table_container.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(0, 5)
)


table_title = tk.Label(
    table_container,
    text="Student Records",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    fg=DARK
)

table_title.pack(
    anchor="w",
    padx=15,
    pady=(12, 5)
)


table_area = tk.Frame(
    table_container,
    bg=WHITE
)

table_area.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


columns = (
    "Student ID",
    "Name",
    "Age",
    "Gender",
    "Course",
    "Marks",
    "Grade",
    "Status"
)


tree = ttk.Treeview(
    table_area,
    columns=columns,
    show="headings"
)


tree.heading(
    "Student ID",
    text="STUDENT ID"
)

tree.heading(
    "Name",
    text="NAME"
)

tree.heading(
    "Age",
    text="AGE"
)

tree.heading(
    "Gender",
    text="GENDER"
)

tree.heading(
    "Course",
    text="COURSE"
)

tree.heading(
    "Marks",
    text="MARKS"
)

tree.heading(
    "Grade",
    text="GRADE"
)

tree.heading(
    "Status",
    text="STATUS"
)


tree.column(
    "Student ID",
    width=100,
    anchor="center"
)

tree.column(
    "Name",
    width=190,
    anchor="w"
)

tree.column(
    "Age",
    width=70,
    anchor="center"
)

tree.column(
    "Gender",
    width=90,
    anchor="center"
)

tree.column(
    "Course",
    width=100,
    anchor="center"
)

tree.column(
    "Marks",
    width=100,
    anchor="center"
)

tree.column(
    "Grade",
    width=80,
    anchor="center"
)

tree.column(
    "Status",
    width=110,
    anchor="center"
)


# ==========================================================
# TABLE COLORS
# ==========================================================

tree.tag_configure(
    "passed",
    background=LIGHT_GREEN,
    foreground="#166534"
)


tree.tag_configure(
    "failed",
    background=LIGHT_RED,
    foreground="#991B1B"
)


scrollbar = ttk.Scrollbar(
    table_area,
    orient="vertical",
    command=tree.yview
)

tree.configure(
    yscrollcommand=scrollbar.set
)


tree.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar.pack(
    side="right",
    fill="y"
)


tree.bind(
    "<ButtonRelease-1>",
    select_student
)


# ==========================================================
# STATUS BAR
# ==========================================================

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=TEXT
)

status_label.pack(
    pady=(5, 10)
)


# ==========================================================
# KEYBOARD SHORTCUT
# ==========================================================

entry_search.bind(
    "<Return>",
    lambda event: search_student()
)


# ==========================================================
# INITIAL DISPLAY
# ==========================================================

refresh_table()

show_status(
    f"✓ System ready — {len(students)} students loaded.",
    GREEN
)


# ==========================================================
# START APPLICATION
# ==========================================================

root.mainloop()
```
