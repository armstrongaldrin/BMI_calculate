import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()

# Create table for storing user BMI data
c.execute('''
    CREATE TABLE IF NOT EXISTS bmi_data (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        bmi REAL NOT NULL
    )
''')
conn.commit()

# Function to calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# Function to save BMI data
def save_bmi_data(name, weight, height, bmi):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO bmi_data (name, date, weight, height, bmi)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, date, weight, height, bmi))
    conn.commit()

# Function to visualize BMI trend
def visualize_bmi_trend(name):
    c.execute('''
        SELECT date, bmi FROM bmi_data WHERE name = ? ORDER BY date
    ''', (name,))
    data = c.fetchall()
    if not data:
        messagebox.showerror("Error", "No data found for the specified user.")
        return
    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
    bmis = [row[1] for row in data]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmis, marker='o')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.title(f'BMI Trend for {name}')
    plt.grid(True)
    plt.show()

# Function to handle BMI calculation and data saving
def input_calculate():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if not name:
            raise ValueError("Name is required")
        bmi = calculate_bmi(weight, height)
        bmi_result_label.config(text=f"BMI: {bmi}")
        save_bmi_data(name, weight, height, bmi)
        messagebox.showinfo("Success", "BMI data saved successfully")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Create main application window
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("800x800")

# Create and place widgets
l1= tk.Text(root)

ttk.Label(root, text="Name:").grid(column=0, row=0, padx=5, pady=5, sticky='W')

name_entry = ttk.Entry(root)
name_entry.grid(column=1, row=0, padx=5, pady=5, sticky='EW' )

ttk.Label(root, text="Weight (kg):").grid(column=0, row=1, padx=5, pady=5, sticky='W')
weight_entry = ttk.Entry(root)
weight_entry.grid(column=1, row=1, padx=5, pady=5, sticky='EW')

ttk.Label(root, text="Height (m):").grid(column=0, row=2, padx=5, pady=5, sticky='W')
height_entry = ttk.Entry(root)
height_entry.grid(column=1, row=2, padx=5, pady=5, sticky='EW')

calculate_button = ttk.Button(root, text="Calculate BMI", command=input_calculate)
calculate_button.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

bmi_result_label = ttk.Label(root, text="BMI: ")
bmi_result_label.grid(column=0, row=4, columnspan=2, padx=5, pady=5)

ttk.Label(root, text="Visualize BMI Trend:").grid(column=0, row=5, padx=5, pady=5, sticky='W')
name_trend_entry = ttk.Entry(root)
name_trend_entry.grid(column=1, row=5, padx=5, pady=5, sticky='EW')

visualize_button = ttk.Button(root, text="Visualize", command=lambda: visualize_bmi_trend(name_trend_entry.get()))
visualize_button.grid(column=0, row=6, columnspan=2, padx=5, pady=5)

# Configure column weights for resizing
root.columnconfigure(1, weight=1)

# Run the application
root.mainloop()

# Close database connection on exit
conn.close()
