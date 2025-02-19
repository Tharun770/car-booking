import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

#CONNECTION OF DB
conn = sqlite3.connect("car_booking.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        car TEXT,
        date_time TEXT
    )
""")
conn.commit()

def book_car():
    user_name = name_entry.get()
    selected_car = car_var.get()
    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not user_name:
        messagebox.showwarning("Input Error", "Please enter your name.")
    elif not selected_car:
        messagebox.showwarning("Selection Error", "Please select a car.")
    else:
        # Insert booking into database
        cursor.execute("INSERT INTO bookings (name, car, date_time) VALUES (?, ?, ?)", 
                       (user_name, selected_car, booking_time))
        conn.commit()
        
        messagebox.showinfo("Booking Confirmed", f"Hello {user_name}, your {selected_car} has been booked!\nTime: {booking_time}")

def view_bookings():
    # Create a new window for the table
    view_window = tk.Toplevel(root)
    view_window.title("View Bookings")
    view_window.geometry("500x300")

    # Table
    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Car", "Date & Time"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Car", text="Car")
    tree.heading("Date & Time", text="Date & Time")

    tree.column("ID", width=30, anchor="center")
    tree.column("Name", width=120, anchor="center")
    tree.column("Car", width=120, anchor="center")
    tree.column("Date & Time", width=150, anchor="center")

    tree.pack(pady=10, fill="both", expand=True)

    # Fetch data from database
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    for booking in bookings:
        tree.insert("", "end", values=booking)

# Create main window
root = tk.Tk()
root.title("Car Booking System")
root.geometry("400x300")

# Heading
tk.Label(root, text="Car Booking System", font=("Arial", 14, "bold")).pack(pady=10)

# Name Entry
tk.Label(root, text="Enter your name:").pack()
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

# Car Selection Dropdown
tk.Label(root, text="Select a Car:").pack()
car_var = tk.StringVar()
car_choices = ["Tesla Model 3", "Toyota Innova", "Hyundai Creta", "Mercedes Benz", "Maruti Swift"]
car_dropdown = ttk.Combobox(root, textvariable=car_var, values=car_choices, state="readonly")
car_dropdown.pack(pady=5)
car_dropdown.current(0)

# Buttons
book_button = tk.Button(root, text="Book Now", command=book_car)
book_button.pack(pady=10)

view_button = tk.Button(root, text="View Bookings", command=view_bookings)
view_button.pack(pady=5)

# Run the app
root.mainloop()

# Close DB connection when app is closed
conn.close()






