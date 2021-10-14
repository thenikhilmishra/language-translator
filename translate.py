# import tkinter, speech_recognition, webbrowser, gTTS, playsound Libraries
import tkinter as tk
from tkinter import Frame, Label, Canvas, PhotoImage
import speech_recognition as sr
import webbrowser
from gtts import gTTS
import playsound


language = ''
new_text = ''
count = 0
# Function definition to convert a audio in hindi
def translate_to_hindi():
    global new_text
    global language

    # Set Language
    language='hi'

    # Take audio from microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Delete content from TextBox(position 0 to end)
        recognized_text.delete(1.0, tk.END)
        audio = r.listen(source)

    # Trying to convert in hindi
    try:
        text = r.recognize_google(audio, language="hi-IN")
        new_text = "Input : {}".format(text)
        # Delete content from TextBox(position 0 to end)
        recognized_text.delete(1.0, tk.END)
        # Insert new_text at TextBox(position 0)
        recognized_text.insert(1.0, new_text)

    # If fails
    except:
        new_text = "Please try again"
        # Delete content from TextBox(position 0 to end)
        recognized_text.delete(1.0, tk.END)
        # Insert new_text at TextBox position 0
        recognized_text.insert(1.0, new_text)

# Function definition to convert a audio in english
def translate_to_english():
    global new_text
    global language

    # Set language
    language='en-us'

    # Record voice from microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Delete content from TextBox(position 0 to end)
        recognized_text.delete(1.0, tk.END)
        audio = r.listen(source)

    # Trying to convert in english
    try:
        text = r.recognize_google(audio)
        new_text = "Input : {}".format(text)
        # Delete content from TextBox(position 0 to end)
        recognized_text.delete(1.0, tk.END)
        # Insert new_text at TextBox(position 0)
        recognized_text.insert(1.0, new_text)

    # If fails
    except:
        new_text = "Please try again"
        # Delete content from position 0 to end
        recognized_text.delete(1.0, tk.END)
        # Insert new_text at position 0
        recognized_text.insert(1.0, new_text)

# Search function to search in chrome browser
def search():
    search_term = recognized_text.get(1.8, tk.END)
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    url = "https://www.google.com/search?q={}".format(search_term)    
    webbrowser.get(chrome_path).open_new_tab(url)

# Speak function (Text to speak converter)
def speak():
    global count
    speak_text = new_text[8:]
    print(speak_text)
    myobj = gTTS(text=speak_text, lang=language, slow=False)
    # Saving the converted audio in a mp3 file
    myobj.save(f'speech{count%2}.mp3')
    playsound.playsound(f'speech{count%2}.mp3')
    count += 1

root = tk.Tk()

root.geometry("640x640")
root.title("Language Translator")
#root.iconbitmap(r'icon.ico')
root['bg'] = "#9fd3c7"
root.minsize(540, 640) 

mainframe=Frame(bg="#ffffff")
mainframe.pack( pady=10, padx=20)
# Styling the frame which helps to make our background stylish
frame1 = Frame(mainframe, bg = "#ffffff", height=50, padx=10)
# Plcae the frame in GUI window
frame1.pack()

# Styling the label which show the text in our tkinter window
label = Label(frame1, text = "Speech to Text", font = "Times 30 italic", bg = "#ffffff", fg="#0058e8")
# Plcae the label in GUI window
label.grid(row=0, column=0)

frame2 = Frame(mainframe, bg = "#ffffff")
frame2.pack(pady=5)

frame2child = Frame(frame2, bg = "#ffffff")
frame2child.grid(row=0, column=0, padx=10)

# Lauguage Selection Label
label = Label(frame2child, text = "Choose a Language", font = "helvetica 20 italic", bg = "#ffffff", fg="#0058e8")
label.pack()

# Hindi Button
hindi_btn = PhotoImage(file='assets/hindi.png')
# Buttons in tkinter window
btn_hindi = tk.Button(frame2child, image=hindi_btn, bg="#ffffff", borderwidth=1, command=translate_to_hindi)
btn_hindi.pack(pady=10)

# English Button
english_btn = PhotoImage(file='assets/english.png')
btn_english = tk.Button(frame2child, image=english_btn, bg="#ffffff", borderwidth=1, command=translate_to_english)
btn_english.pack(pady=10)

# Animated GIF
# Mic GIF
# Frames in GIF
framesmic = [PhotoImage(file='assets/micuiani.gif', format = 'gif -index %i' %(i)) for i in range(147)]
# Update GIF function
def updatemic(ind):
    framemic = framesmic[ind]
    if (ind==146):
        ind = 0
    else:
        ind += 1
    labelmic.configure(image=framemic)
    root.after(50, updatemic, ind)
# GIF Label in tkinter window
labelmic = Label(frame2, bg="#ffffff", height=250, width=250)
# Place in GUI
labelmic.grid(row=0, column=1)
root.after(0, updatemic, 0)

frame3 = Frame(mainframe, bg = "#ffffff")
frame3.pack()

labeltext = Label(frame3, text = "Text", font = "Times 30 italic", bg = "#ffffff", fg="#0058e8")
labeltext.grid(row=0, column=0)

frame4 = Frame(mainframe, bg = "#ffffff")
frame4.pack()

# Text Box
recognized_text = tk.Text(frame4, padx=10, width=30, height=10, borderwidth=3)
recognized_text.grid(row=0, column=0, pady=5, padx=10, rowspan=2)

# Search Button
search_btn = PhotoImage(file='assets/search.png')
btn_search = tk.Button(frame4, image=search_btn, bg="#ffffff", borderwidth=1, command=search)
btn_search.grid(row=0, column=1, padx=10)

# Speak Button
speak_btn = PhotoImage(file='assets/speak.png')
btn_speak = tk.Button(frame4, image=speak_btn, bg="#ffffff", command=speak)
btn_speak.grid(row=1, column=1, padx=10)

# Robot GIF
framesrobo = [PhotoImage(file='assets/talkingrobo.gif',format = 'gif -index %i' %(i)) for i in range(5)]
def updaterobo(ind):
    framerobo = framesrobo[ind]
    if (ind==4):
        ind = 0
    else:
        ind += 1
    labelrobo.configure(image=framerobo)
    root.after(100, updaterobo, ind)
labelrobo = Label(frame4, bg="#ffffff")
labelrobo.grid(row=0, column=3, rowspan=2, padx=10)
root.after(0, updaterobo, 0)

root.mainloop()