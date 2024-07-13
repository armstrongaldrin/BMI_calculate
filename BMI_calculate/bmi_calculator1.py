import tkinter
from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox as box
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime





conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()

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

window = Tk()


def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def save_bmi_data(name, weight, height, bmi):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO bmi_data (name, date, weight, height, bmi)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, date, weight, height, bmi))
    conn.commit()
def visualize_bmi_trend(name):
    c.execute('''
        SELECT date, bmi FROM bmi_data WHERE name = ? ORDER BY date
    ''', (name,))
    data = c.fetchall()
    if not data:
        box.showerror("Error", "No data found for the specified user.")
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



def input_calculate():
    try:
        name = e1.get()
        weight = float(e2.get())
        height = float(e3.get())
        if not name:
            raise ValueError("Name is required")
        bmi = int(calculate_bmi(weight, height))
        if bmi <18:
            l4.config(text=f"BMI: {bmi} : underweight ")
        elif bmi in range(18,25) :
            l4.config(text=f"BMI: {bmi} : Normal ")
        elif bmi in range(25,30) :
            l4.config(text=f"BMI: {bmi} : Overweight")
        elif bmi >30:
            l4.config(text=f"BMI: {bmi} Obese")
        else:
            l4.config(text="Enter a valid input  ")

        save_bmi_data(name, weight, height, bmi)
        box.showinfo("Success", "BMI data saved successfully")
    except ValueError as e:
        box.showerror("Error", str(e))

window.title("BMI CALCULATOR")


frame = Frame(window)

l1 = Label(window,text="BMI CALCULATOR", fg="black",font=("Garamond",10)).place(x = 150,y=20)
l2 = Label(window,text="Name",fg="black",font=("Arial", 10) ).place(x=100,y=60)
e1 = Entry(window,bd=0)
e1.place(x=200,y=61)
l2 = Label(window,text="Weight (kg)",fg="black",font=("Arial", 10) ).place(x=100,y=80)
e2 = Entry(window,bd=0)
e2.place(x=200,y=81)
l3 = Label(window,text="Height (m)",fg="black",font=("Arial", 10) ).place(x=100,y=100)
e3 = Entry(window,bd=0)
e3.place(x=200,y=101)

bt = Button(text="Calulate",command=input_calculate,fg="black").place(x=170,y=150)

l4 = Label(window,text="BMI",fg="black",font=("Arial", 10))
l4.place(x=100,y=200)

l5 = Label(window,text="Visualize BMI Trend:",fg="black",font=("Arial", 10))
l5.place(x=100,y=230)

e4 = Entry(window)




e4.place(x=240,y=230)

b2 = Button(window,text="Visualize Trend",command=lambda:visualize_bmi_trend(e4.get())).place(x=140,y=270)

window.geometry("400x400")
window.mainloop()