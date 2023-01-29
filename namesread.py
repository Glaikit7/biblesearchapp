import tkinter as tk
import json
import re

# load the names and meanings from the json file
with open('biblenames.json', 'r') as infile:
    names_dict = json.load(infile)

# create the Tkinter UI
root = tk.Tk()
root.title("Bible Name Search")

# create the Textbox for the user to enter the desired passage
passage_text = tk.StringVar()
font = ('Helvetica', 12)
passage_entry = tk.Entry(root, textvariable=passage_text,width=100, font=font)
passage_entry.pack()

# create the Listbox to display the results
result_list = tk.Listbox(root, width=40, height=10,font=font)
result_list.pack()

# create the search button
def search():
    # clear the Listbox
    result_list.delete(0, tk.END)

    # get the passage of scripture from the user
    passage = passage_text.get()
    # remove all punctuation and whitespace from the passage
    passage = re.sub(r'[^\w\s]','',passage)

    # split the passage into a list of words
    words = passage.split()
    # iterate over the words in the passage
    for word in words:
        # if the word is a key in the names dictionary, add the name and meaning to the Listbox
        if word in names_dict:
            result_list.insert(tk.END, f"{word}: {names_dict[word]}")

search_button = tk.Button(root, text="Search", command=search)
search_button.pack()

# run the Tkinter UI
root.mainloop()



