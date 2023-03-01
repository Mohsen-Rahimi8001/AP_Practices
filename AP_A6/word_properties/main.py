from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.font import Font
from tkinter.scrolledtext import *
import file_menu
import edit_menu
import format_menu
import help_menu
import word_check
from threading import Thread

root = Tk()
root.title("Text Editor-Untiltled")
root.geometry("300x250+300+300")
root.minsize(width=400, height=400)

text = ScrolledText(root, state='normal', height=400, width=400, wrap='word', pady=2, padx=3, undo=True)
text.pack(fill=Y, expand=1)
text.focus_set()
menubar = Menu(root)
mymenu = Menu(root)
mymenu.add_command(label="mycommand", command = print)
file_menu.main(root, text, menubar)
edit_menu.main(root, text, menubar)
format_menu.main(root, text, menubar)
help_menu.main(root, text, menubar)

def word_retrieve():
    word = ""
    def inner(event:Event):
        nonlocal word
        
        if event.char == ' ':
            if word != '':
                Thread(target=word_check.check_word, args=(word.strip(),)).start()
                word = ""
        else:
            word += event.char

    return inner

word_retriever = word_retrieve()

text.bind("<Key>", word_retriever)

root.mainloop()

