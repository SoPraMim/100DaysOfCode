# ---------------------------- Imports ---------------------------- #
from tkinter import *
from tkinter import messagebox
import pandas as pd
import pyperclip

#
DATA_LOCATION = "Day 030 - Password Manager 2/password_bank.json"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
        #Password Generator Project
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    n_characters = 15
    nr_letters= random.randint(0,n_characters) 
    nr_symbols = random.randint(0,n_characters - nr_letters)
    nr_numbers = n_characters - nr_letters - nr_symbols

    password = []
    for _ in range(0,nr_letters):
        password.append(random.choice(letters))

    for _ in range(0,nr_symbols):
        password.append(random.choice(symbols))
    
    for _ in range(0,nr_numbers):
        password.append(random.choice(numbers))

    random.shuffle(password)
    password = ''.join(password)
    password_input.delete(0,END)
    password_input.insert(END, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    try:
        saved_passwords = pd.read_json(DATA_LOCATION)
    except:
        saved_passwords = pd.DataFrame()
    
    to_search = website_input.get()
    try:
        password_found = to_search in saved_passwords["Website"].values
    except:
        password_found = False
    if password_found:
        if messagebox.askyesno(title=website_input.get(), message ="Do you want to overwrite existing password?"):
            saved_passwords.loc[saved_passwords.Website == to_search, 'Username'] = username_input.get()
            saved_passwords.loc[saved_passwords.Website == to_search, 'Password'] = password_input.get()
            saved_passwords.to_json(DATA_LOCATION)
    else:
        if messagebox.askyesno(title=website_input.get(), message ="Save new password?"):
            to_file = {"Website": [website_input.get()],
                    "Username": [username_input.get()],
                    "Password": [password_input.get()]
                    }
            to_file = pd.DataFrame(to_file)
            to_file = pd.concat([saved_passwords,to_file],ignore_index = True)
            to_file.to_json(DATA_LOCATION)

                
# ---------------------------- Search Function ------------------------------- #
def search_password():
    try:
        saved_passwords = pd.read_json(DATA_LOCATION)
    except:
        saved_passwords = pd.DataFrame()
    to_search = website_input.get()
    username_input.delete(0,END)
    username_input.insert(END, str(saved_passwords.loc[saved_passwords.Website == to_search, 'Username'].values[0]))   
    password_input.delete(0,END)
    password_input.insert(END, str(saved_passwords.loc[saved_passwords.Website == to_search, 'Password'].values[0])) 
    


# ---------------------------- UI SETUP ------------------------------- #
# if __name__ == "__main__":
window = Tk()
window.title("MyPass")
window.config(padx=50,
            pady=50)

# Canvas
canvas = Canvas(width=200, height=200)

img = PhotoImage(file="Day 030 - Password Manager 2/logo.png")
canvas.create_image(100, 100, image= img)
canvas.grid(column=1,
            row=0,
            sticky=W+E+N+S)

# Labels
website_label = Label(text="Website: ",)
website_label.grid(column= 0,
                    row=1,
                    sticky=W+E+N+S)

username_label = Label(text="Email/Username:")
username_label.grid(column=0,
                    row=2,
                    sticky=W+E+N+S)
password_label = Label(text="Password: ")
password_label.grid(column=0,
                    row=3,
                    sticky=W+E+N+S)

# Entries
website_input = Entry(width=35)
website_input.grid(column=1,
                    row=1,
                    sticky=W+E+N+S)
website_input.focus()

username_input = Entry(width=35)
username_input.grid(column=1,
                    row=2,
                    columnspan=2,
                    sticky=W+E+N+S)
#username_input.insert(END, "some_email@host.com")

password_input = Entry(width=21)
password_input.grid(column=1,
                    row=3,
                    sticky=W+E+N+S)

# Buttons
search_button = Button(text="Search Password",
                        command=search_password)
search_button.grid(column=2,
                    row=1)

password_generate_button = Button(text="Generate Password",
                                command=generate_password,
                                highlightthickness=0)
password_generate_button.grid(column=2,
                            row=3,
                            sticky=W+E+N+S)

save_password_button = Button(text="Add",
                            command=save_password,
                            width=45)
save_password_button.grid(column=1,
                        row=4,
                        columnspan=2)
window.mainloop()