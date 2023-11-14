from tkinter import *
from tkinter.messagebox import *
from random import shuffle, choice
import pyperclip
import json

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
    website = ent_website.get().title()  # Returns the entry's current text as a string.
    email = ent_email.get().lower()
    pswd = ent_password.get()

    if website != "" and email != "" and pswd != "":
        global count_number
        count_number += 1

        is_confirmed = askyesno(
            "Validation",
            f"Platform: {website}\nE-mail: {email}\nPassword: {pswd}\n Do you want to save?"
        )

        if is_confirmed:
            entered_data = {
                website: {
                    "email": email,
                    "password": pswd
                }
            }
            try:  # try to OPEN and READ the JSON file (if it does not exist, it'll through the ERROR)
                with open("db.json", "r") as db_file:
                    # LOAD json file to READ data in it
                    data_in_db_file = json.load(db_file)
                    # TODO - ERROR - if the website exist in db, but yo wanna add 2nd username and password
            except FileNotFoundError:  # catch that error and UPDATE the json file with new data
                with open("db.json", mode="w") as db_file:
                    # WRITE (dump) the updated data into JSON database file
                    json.dump(entered_data, db_file, indent=4)
                    #    dump(DICTIONARY which should be converted to JSON object, FILE opened in write or append mode)
            else:  # if file exist, WRITE the UPDATED data into JSON file
                # UPDATE the loaded json file and add the new data
                data_in_db_file.update(entered_data)

                with open("db.json", mode="w") as db_file:
                    # WRITE (dump) the updated data into JSON database file
                    json.dump(data_in_db_file, db_file, indent=4)
                    #    dump(DICTIONARY which should be converted to JSON object, FILE opened in write or append mode)
            finally:
                ent_website.delete(0, END)
                ent_email.delete(0, END)
                ent_password.delete(0, END)

            showinfo("Confirmation", "Successfully saved")
    else:
        showwarning("W A R N I N G", "Please, fill all empty areas")


# ----------------------------------------------------------------------- SEARCH DATABASE --------------------------- #
def search_database():
    website = ent_website.get().title()  # read and find matching key (which is website name)
    # open json data in READ MODE
    try:
        with open("db.json", mode="r") as db_file:
            database = json.load(db_file)  # json.load() returns Python DICTIONARY
    except FileNotFoundError:
        showinfo("ATTENTION", "Database is empty")
    else:
        if website in database:
            email = database[website]['email']
            password = database[website]['password']

            pyperclip.copy(password)  # copy password to clipboard

            is_ok_clicked = showinfo(
                f"{website}",
                f"E-mail: {email}\nPassword: {password}"
            )
            if is_ok_clicked:
                ent_website.delete(0, END)
                ent_email.delete(0, END)
                ent_password.delete(0, END)
        else:
            if website == "":
                showinfo("ATTENTION", "Please, fill all empty areas")
            else:
                showinfo("ATTENTION", f"No record about '{website}' in database")


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
    foreground=TXT_COLOR,
    width=25
)
ent_website.focus()
ent_website.grid(column=1, row=1, pady=PADDING_NS)
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
    foreground=TXT_COLOR,
    width=25
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

btn_search = Button(
    text="Search Password",
    font=FONT_BTN,
    background=BTN_BG_COLOR,
    foreground=TXT_COLOR,
    pady=PADDING_NS,
    command=search_database
)
btn_search.grid(column=2, row=1, sticky=E + W)

window.mainloop()
