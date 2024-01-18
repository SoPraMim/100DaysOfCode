from tkinter import *

# Window
screen = Tk()
screen.title("Mile to Km Converter")
# screen.minsize(width=100, height=100)
screen.config(padx=10,pady=10)

# Miles input
miles_entry = Entry(screen,width=10,justify="center")
miles_entry.insert(END, string="0",)
miles_entry.grid(column=1,row=0)

miles_label = Label(text="Miles",justify="left")
miles_label.grid(column=2,row=0)

# Km output
equal_label = Label(text="is equal to",justify="right")
equal_label.grid(column=0,row=1)

km_output_label = Label(text="0")
km_output_label.grid(column=1,row=1)

km_label = Label()
km_label.config(text="Km")
km_label.grid(column=2,row=1)

# Calculate button
def calculate():
    miles_input = float(miles_entry.get())
    km = round(miles_input * 1.609344, 2)
    km_output_label.config(text=km)

calculate_button = Button(text="Calculate", command=calculate)
calculate_button.grid(column=1,row=2)

screen.mainloop()