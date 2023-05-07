from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import sqlite3

# Create window
window = Tk()
window.title("Medicine Reminder App")
window.geometry("500x500")
window.configure(bg="#F7F7F7")

# Set fonts
large_font = Font(family="Helvetica", size=20)
medium_font = Font(family="Helvetica", size=16)
small_font = Font(family="Helvetica", size=12)

# Create labels
title_label = Label(window, text="Medicine Reminder App", font=large_font, bg="#F7F7F7")
title_label.pack(pady=20)

medicine_label = Label(window, text="Medicine Name", font=medium_font, bg="#F7F7F7")
medicine_label.pack()

# Create medicine input field
medicine_entry = Entry(window, font=medium_font)
medicine_entry.pack()

# Create time input fields
time_label = Label(window, text="Time", font=medium_font, bg="#F7F7F7")
time_label.pack(pady=(20, 10))

hour_entry = Spinbox(window, from_=0, to=23, width=2, font=small_font)
hour_entry.pack(side=LEFT, padx=10)

colon_label = Label(window, text=":", font=medium_font, bg="#F7F7F7")
colon_label.pack(side=LEFT)

minute_entry = Spinbox(window, from_=0, to=59, width=2, font=small_font)
minute_entry.pack(side=LEFT, padx=10)

# Create save button
def add_medicine():
    # Add medicine to database
    name = medicine_entry.get().strip()
    hour = int(hour_entry.get())
    minute = int(minute_entry.get())
    if name and hour and minute:
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicines (name, hour, minute) VALUES (?, ?, ?)", (name, hour, minute))
        conn.commit()
        load_medicines()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

save_button = Button(window, text="Save", font=medium_font, command=add_medicine)
save_button.pack(pady=20)

# Create a list of medicines
medicine_listbox = Listbox(window, font=small_font, width=40, height=10)
medicine_listbox.pack(pady=20)

# Create delete button
def delete_medicine():
    # Delete selected medicine from database
    selected_medicine = medicine_listbox.get(ANCHOR)
    if selected_medicine:
        name = selected_medicine.split(" ")[0]
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medicines WHERE name=?", (name,))
        conn.commit()
        load_medicines()

delete_button = Button(window, text="Delete", font=medium_font, command=delete_medicine)
delete_button.pack()

# Connect to database
conn = sqlite3.connect("medicines.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY,
                name TEXT,
                hour INTEGER,
                minute INTEGER
                )""")
conn.commit()

def load_medicines():
    # Load medicines from database
    medicine_listbox.delete(0, END)
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    for medicine in medicines:
        name = medicine
