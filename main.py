from tkinter import *
from tkinter.messagebox import *
from random import shuffle, choice
import pyperclip

PADDING_WINDOW_X = 50
PADDING_WINDOW_y = 50
PADDING_LOGO = 20
PADDING_EW = 10
PADDING_NS = 1
FONT = ("Courier", 7)
FONT_BTN = ("Courier", 7, "bold")
BACKGROUND_COLOR = "white"
BTN_BG_COLOR = "#a0e4f8"
BLUE = "#6db1cf"
TXT_COLOR = "#14415b"
ENTRY_BORDER_COLOR_SELECTED = "#ee787a"
ENTRY_BORDER_COLOR_IDLE = "#fbdb54"
count_number = 0
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
NUM_OF_LETTERS_IN_PASSWORD = 8
NUM_OF_NUMBERS_IN_PASSWORD = 4
NUM_OF_SYMBOLS_IN_PASSWORD = 4


# ----------------------------------------------------------------------- GENERATE PASSWORD ------------------------- #
def generate_password():
    if len(ent_password.get()) == 0:
        row_password = [choice(LETTERS) for _ in range(0, NUM_OF_LETTERS_IN_PASSWORD)]
        row_password += [choice(NUMBERS) for _ in range(0, NUM_OF_NUMBERS_IN_PASSWORD)]
        row_password += [choice(SYMBOLS) for _ in range(0, NUM_OF_SYMBOLS_IN_PASSWORD)]

        shuffle(row_password)

        generated_password = "".join([str(item) for item in row_password])

        ent_password.insert(0, generated_password)
        pyperclip.copy(generated_password)
    else:
        # clear entry and regenerate a new password
        ent_password.delete(0, END)
        generate_password()


# -----------------------------------------------------------------------  SAVE PASSWORD ---------------------------- #
def save_data():
    website = ent_website.get()  # Returns the entry's current text as a string.
    email = ent_email.get()
    pswd = ent_password.get()

    if website != "" and email != "" and pswd != "":
        global count_number
        count_number += 1

        is_confirmed = askyesno(
            "Validation",
            f"Platform: {website}\nE-mail: {email}\nPassword: {pswd}\n Do you want to save?"
        )

        if is_confirmed:
            with open("db.txt", mode="a") as db_file:
                db_file.write(f"{count_number}) Platform: {website} | E-mail: {email} | Password: {pswd}\n")
                ent_website.delete(0, END)
                ent_email.delete(0, END)
                ent_password.delete(0, END)

            showinfo("Confirmation", "Successfully saved")
    else:
        showwarning("W A R N I N G", "Please, fill all empty areas")


# -------------------------------------------------------------------------  UI SETUP ------------------------------- #
# WINDOW
window = Tk()
window.title("Passwordistan")
window.config(
    padx=PADDING_WINDOW_X,
    pady=PADDING_WINDOW_y,
    background=BACKGROUND_COLOR
)

# CANVAS
canvas = Canvas(
    width=250,
    height=200,
    background=BACKGROUND_COLOR,
    highlightthickness=0
)

# CANVAS > logo
logo = PhotoImage(file="logo.png")
canvas.create_image(125, 100, image=logo)
canvas.grid(column=0, row=0, columnspan=3, pady=PADDING_LOGO)

#  ------------------------------------------------------------- LABELS
# > website
lbl_website = Label(
    text="Website",
    font=FONT,
    background=BACKGROUND_COLOR,
    foreground=TXT_COLOR,
    padx=PADDING_EW,
    pady=PADDING_NS,
)
lbl_website.grid(column=0, row=1)
# > email
lbl_email = Label(
    text="Email / Username",
    font=FONT,
    background=BACKGROUND_COLOR,
    foreground=TXT_COLOR,
    padx=PADDING_EW,
    pady=PADDING_NS,
)
lbl_email.grid(column=0, row=2)
#  > password
lbl_password = Label(
    text="Password",
    font=FONT,
    background=BACKGROUND_COLOR,
    foreground=TXT_COLOR,
    padx=PADDING_EW,
    pady=PADDING_NS,
)
lbl_password.grid(column=0, row=3)

# --------------------------------------------------------------- ENTRIES
#  > website name
ent_website = Entry(
    highlightcolor=ENTRY_BORDER_COLOR_SELECTED,
    highlightthickness=2,
    highlightbackground=ENTRY_BORDER_COLOR_IDLE,
    foreground=TXT_COLOR
)
ent_website.focus()
ent_website.grid(column=1, row=1, columnspan=2, sticky=E + W, pady=PADDING_NS)
#  > email
ent_email = Entry(
    highlightcolor=ENTRY_BORDER_COLOR_SELECTED,
    highlightthickness=2,
    highlightbackground=ENTRY_BORDER_COLOR_IDLE,
    foreground=TXT_COLOR
)
# ent_email.insert(0, "@gmail.com")
ent_email.grid(column=1, row=2, columnspan=2, sticky=E + W, pady=PADDING_NS)
#  > password
ent_password = Entry(
    highlightcolor=ENTRY_BORDER_COLOR_SELECTED,
    highlightthickness=2,
    highlightbackground=ENTRY_BORDER_COLOR_IDLE,
    foreground=TXT_COLOR
)
ent_password.grid(column=1, row=3, pady=PADDING_NS)

#  -------------------------------------------------------------- BUTTONS
# > generate
btn_generate = Button(
    text="Generate Password",
    font=FONT_BTN,
    background=BTN_BG_COLOR,
    foreground=TXT_COLOR,
    pady=PADDING_NS,
    command=generate_password
)
btn_generate.grid(column=2, row=3)
# > save
btn_save = Button(
    text="Save",
    font=FONT_BTN,
    background=BTN_BG_COLOR,
    foreground=TXT_COLOR,
    pady=PADDING_NS,
    command=save_data
)
btn_save.grid(column=1, row=4, columnspan=2, sticky=E + W)

window.mainloop()
