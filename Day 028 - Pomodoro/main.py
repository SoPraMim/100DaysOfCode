from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
REPS = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global REPS
    REPS = 0
    window.after_cancel(timer)
    pomodoro_count_label.config(text=get_pomodoro_count_in_ticks())
    title_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    start_button.config(command=start_timer)



# ---------------------------- TIMER MECHANISM ------------------------------- # 
def empty():
    pass

def start_timer():
    start_button.config(command=empty)
    global REPS
    REPS += 1
    work_sec = WORK_MIN * 60
    short_breaks_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    # work_sec = 10
    # short_breaks_sec = 5
    if REPS % 8 in [1,3,5,7]:
        title_label.config(text="Work",fg=GREEN)
        countdown(work_sec)
    elif REPS % 8 in [2,4,6]:
        title_label.config(text="Break", fg=PINK)
        countdown(short_breaks_sec)
    elif REPS % 8 == 0:
        title_label.config(text="Break", fg=RED)
        countdown(long_break_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def countdown(count):
    count_min = int(count / 60)
    count_sec = count % 60
    text = f"{count_min:02d}:{count_sec:02d}"
    canvas.itemconfig(timer_text, text=text)
    if count > 0:
        global timer
        timer = window.after(1000, countdown, count-1)
    else:
        pomodoro_count_label.config(text=get_pomodoro_count_in_ticks())
        if REPS < 8:
            start_timer()
        else:
            pass

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(bg=YELLOW,
              padx=100,
              pady=50,
              highlightthickness=0)

canvas = Canvas(width=200,
                height=224,
                highlightthickness=0,
                bg=YELLOW)
img = PhotoImage(file="./Day 028 - Pomodoro/tomato.png")
canvas.create_image(100, 112, image= img)
timer_text = canvas.create_text(100,130, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
canvas.grid(column=1,
            row=1)

title_label = Label(fg=GREEN,
                   bg=YELLOW,
                   text="Timer",
                   font=(FONT_NAME,32,"bold"))
title_label.grid(column=1,
                 row= 0)

start_button = Button(text="Start",
                      command=start_timer,
                      font=(FONT_NAME,12,"normal"),
                      highlightthickness=0)
start_button.grid(column=0,
                  row= 2)

reset_button = Button(text="Reset",
                      command=reset_timer,
                      font=(FONT_NAME,12,"normal"),
                      highlightthickness= 0)
reset_button.grid(column=2,
                  row= 2)


def get_pomodoro_count_in_ticks():
    text = ""
    for i in range(REPS):
        text += "✔"
    return text
pomodoro_count_label = Label(fg=GREEN,
                             bg=YELLOW,
                             text= get_pomodoro_count_in_ticks(),
                             font=(FONT_NAME,16,"bold"),
                             highlightthickness= 0)
pomodoro_count_label.grid(column= 1,
                          row=3)


window.mainloop()