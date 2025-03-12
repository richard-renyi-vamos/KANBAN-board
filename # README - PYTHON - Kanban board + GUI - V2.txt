CHATGPT CONVERSATION

********

ADD GUI FOR SETTINGS

----------

import tkinter as tk
from tkinter import simpledialog

class KanbanBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Kanban Board")

        self.lists = {}
        self.create_list_button = tk.Button(root, text="Create List", command=self.create_list)
        self.create_list_button.pack()

    def create_list(self):
        list_name = simpledialog.askstring("Input", "Enter list name:")
        if list_name:
            list_frame = tk.Frame(self.root)
            list_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

            tk.Label(list_frame, text=list_name).pack()
            card_entry = tk.Entry(list_frame)
            card_entry.pack()
            add_card_button = tk.Button(list_frame, text="Add Card", command=lambda list_name=list_name, card_entry=card_entry: self.add_card(list_name, card_entry))
            add_card_button.pack()
            cards_frame = tk.Frame(list_frame)
            cards_frame.pack()
            self.lists[list_name] = {"entry": card_entry, "cards": cards_frame}

    def add_card(self, list_name, card_entry):
        card_text = card_entry.get()
        if card_text:
            card_label = tk.Label(self.lists[list_name]["cards"], text=card_text, relief=tk.RAISED)
            card_label.pack(fill=tk.X)
            card_label.bind("<Button-1>", lambda event, label=card_label: self.rename_card(event, label))
            card_entry.delete(0, tk.END)

    def rename_card(self, event, card_label):
        new_text = simpledialog.askstring("Rename Card", "Enter a new name:", initialvalue=card_label.cget("text"))
        if new_text:
            card_label.config(text=new_text)

if __name__ == "__main__":
    root = tk.Tk()
    kanban_board = KanbanBoard(root)
    root.mainloop()


# CREATED WITH THE HELP OF OPEN-AI CHAT GPT: https://chat.openai.com/chat
ChatGPT said:
Here's your updated code with a GUI settings menu added using Tkinter. The settings menu allows you to customize the board title and toggle dark mode.

Kanban Gui Settings

Answer in chat instead
Now you have a settings menu where you can change the board title and toggle dark mode! Let me know if you want any further enhancements. 🚀

**************

import tkinter as tk
from tkinter import simpledialog, Menu

class KanbanBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Kanban Board")
        self.dark_mode = False

        # Menu bar
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)
        
        # Settings menu
        self.settings_menu = Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="Change Board Title", command=self.change_title)
        self.settings_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        self.lists = {}
        self.create_list_button = tk.Button(root, text="Create List", command=self.create_list)
        self.create_list_button.pack()

    def create_list(self):
        list_name = simpledialog.askstring("Input", "Enter list name:")
        if list_name:
            list_frame = tk.Frame(self.root, bg="black" if self.dark_mode else "white")
            list_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

            tk.Label(list_frame, text=list_name, bg="black" if self.dark_mode else "white", fg="white" if self.dark_mode else "black").pack()
            card_entry = tk.Entry(list_frame)
            card_entry.pack()
            add_card_button = tk.Button(list_frame, text="Add Card", command=lambda list_name=list_name, card_entry=card_entry: self.add_card(list_name, card_entry))
            add_card_button.pack()
            cards_frame = tk.Frame(list_frame)
            cards_frame.pack()
            self.lists[list_name] = {"entry": card_entry, "cards": cards_frame}

    def add_card(self, list_name, card_entry):
        card_text = card_entry.get()
        if card_text:
            card_label = tk.Label(self.lists[list_name]["cards"], text=card_text, relief=tk.RAISED)
            card_label.pack(fill=tk.X)
            card_label.bind("<Button-1>", lambda event, label=card_label: self.rename_card(event, label))
            card_entry.delete(0, tk.END)

    def rename_card(self, event, card_label):
        new_text = simpledialog.askstring("Rename Card", "Enter a new name:", initialvalue=card_label.cget("text"))
        if new_text:
            card_label.config(text=new_text)

    def change_title(self):
        new_title = simpledialog.askstring("Board Title", "Enter new board title:")
        if new_title:
            self.root.title(new_title)
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "black" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"
        self.root.configure(bg=bg_color)
        self.create_list_button.config(bg=bg_color, fg=fg_color)
        for list_name, elements in self.lists.items():
            elements["cards"].config(bg=bg_color)
            elements["entry"].config(bg=bg_color, fg=fg_color)

if __name__ == "__main__":
    root = tk.Tk()
    kanban_board = KanbanBoard(root)
    root.mainloop()
