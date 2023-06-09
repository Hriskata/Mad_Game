from tkinter import *
import random
from PIL import ImageTk, Image
import requests
from io import BytesIO


# global list with possible words
words = ["apple", "banana", "orange", "elephant", "function"]

mistake_0 = "https://github.com/Hriskata/Mad_Game/blob/main/images/0.png?raw=true"
mistake_1 = "https://github.com/Hriskata/Mad_Game/blob/main/images/1.png?raw=true"
mistake_2 = "https://github.com/Hriskata/Mad_Game/blob/main/images/2.png?raw=true"
mistake_3 = "https://github.com/Hriskata/Mad_Game/blob/main/images/3.png?raw=true"
mistake_4 = "https://github.com/Hriskata/Mad_Game/blob/main/images/4.png?raw=true"
mistake_5 = "https://github.com/Hriskata/Mad_Game/blob/main/images/5.png?raw=true"
mistake_6 = "https://github.com/Hriskata/Mad_Game/blob/main/images/6.png?raw=true"
mistake_7 = "https://github.com/Hriskata/Mad_Game/blob/main/images/7.png?raw=true"

images_mistakes_list = [mistake_0, mistake_1, mistake_2, mistake_3, mistake_4, mistake_5, mistake_6, mistake_7]

# function that generate the random word
def generate_word():
    word = random.choice(words)
    return word


# global dict for buttons: key->value: letter->letter_button
letter_buttons = {}

def creating_buttons():
    # generating letter buttons
    for letter in "abcdefghijklmnopqrstuvwxyz":
        letter_button = Button(letters_frame, text=letter, width=1, command=lambda l=letter: letter_click(l))
        letter_buttons[letter] = letter_button
        letter_button.pack(side="left")


# function to display the image from my github
def display_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
        except:
            print("Failed to open or load the image.")
    else:
        print("Failed to download the image.")


# function that reveals letters of the word
def reveal_letter(letter):
    if letter in chosen_word:
        indexes = [i for i, c in enumerate(chosen_word) if c == letter]
        for i in indexes:
            current_guess[i] = letter
        guess.set(" ".join(current_guess))
        if "_ " not in current_guess:
            result.set("You WON!")
            play_again_button.config(state="active")
            for i in letter_buttons:
                letter_buttons[i].config(state="disable")

    else:
        current_mistakes.set(current_mistakes.get()+1)
        display_image(images_mistakes_list[current_mistakes.get()])
        if current_mistakes.get() >= 7:
            for i in letter_buttons:
                letter_buttons[i].config(state="disable")
            result.set("You LOST!")
            play_again_button.config(state="active")


# function that reveals the first and last letter of the word
def reveal_first_last_l(chosen_word):
    current_guess[0] = chosen_word[0]
    current_guess[len(current_guess)-1] = chosen_word[len(chosen_word)-1]
    letter_buttons[chosen_word[0]].config(state="disable")
    letter_buttons[chosen_word[len(chosen_word)-1]].config(state="disable")
    if chosen_word[0] in chosen_word:
        indexes = [i for i, c in enumerate(chosen_word) if c == chosen_word[0]]
        for i in indexes:
            current_guess[i] = chosen_word[0]
        guess.set(" ".join(current_guess))
    if chosen_word[len(chosen_word)-1] in chosen_word:
        indexes = [i for i, c in enumerate(chosen_word) if c == chosen_word[len(chosen_word)-1]]
        for i in indexes:
            current_guess[i] = chosen_word[len(chosen_word)-1]
        guess.set(" ".join(current_guess))


# function: when u click - disable the button after click
def letter_click(letter):
    letter_buttons[letter].config(state="disable")
    reveal_letter(letter)


# button for play again option
# WORK :D
# this WAS a future idea :D
def play_again():
    try:
        global chosen_word
        chosen_word = generate_word()
        global current_guess
        current_guess = ["_ " for _ in chosen_word]
        for i in letter_buttons:
            letter_buttons[i].config(state="active")
        guess.set(" ".join(current_guess))
        reveal_first_last_l(chosen_word)
        current_mistakes.set(0)
        result.set("")
        display_image(images_mistakes_list[current_mistakes.get()])
    except Exception as e:
        print(e)
        future_label = Label(window, text="FUTURE IDEA")
        future_label.grid(row=8, column=0, columnspan=2)
        play_again_button.config(state="disable")


# function to close the application
def close_app():
    window.destroy()

# generate random word from the global list with words
chosen_word = generate_word()

# creating window
window = Tk()
window.title("Mad game")
window.geometry("440x400")

# label for the chosen word
current_guess = ["_ " for _ in chosen_word]
guess = StringVar()
guess_label = Label(window, textvariable=guess)
guess.set(" ".join(current_guess))
guess_label.grid(row=0, column=0, columnspan=2)

# letters frame for buttons
letters_frame = Frame(window)
letters_frame.grid(row=1, column=0, columnspan=2)

# calling the creating buttons function
creating_buttons()

# revealing the first and last letter
reveal_first_last_l(chosen_word)

# mistakes frame
mistakes_frame = Frame(window)
mistakes_frame.grid(row=2, column=0, rowspan=3, columnspan=2)

# mistakes label
mistakes_text_label = Label(mistakes_frame, text="You can make only 6 mistakes!")
mistakes_text_label.grid(row=2, column=0, columnspan=2)

# text mistakes label
mistakes_text_label = Label(mistakes_frame, text="Mistakes:")
mistakes_text_label.grid(row=3, column=0)

# number mistakes label
current_mistakes = IntVar()
current_mistakes.set(0)
mistakes_label = Label(mistakes_frame, textvariable=current_mistakes)
mistakes_label.grid(row=3, column=1, columnspan=2)

# label for images
image_label = Label(mistakes_frame)
display_image(images_mistakes_list[0])
image_label.grid(row=4,column=0, rowspan=2, columnspan=2)

# result text label
result = StringVar()
result_label = Label(window, textvariable=result)
result.set("")
result_label.grid(row=6, column=0, columnspan=2)

# play again button
play_again_button = Button(window, text="PLAY AGAIN", command=play_again, state="disable")
play_again_button.grid(row=7,column=0)

# exit button
exit_button = Button(window, text="EXIT", command=close_app)
exit_button.grid(row=7,column=1)

window.mainloop()
