#!/usr/bin/env python

"""RemGanG Lottery app made with Python's Tkinter library."""

import json
import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
import threading


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Make winners variable
        self.winners = []

        # Initialize window and components
        self.title("RemGanG")
        self.geometry("400x435")
        self.style = ttk.Style(self)

        file_frame = tk.Frame(self)

        self.file_label = ttk.Label(file_frame, text="No File selected")
        self.file_label.pack(anchor=tk.W, side=tk.LEFT)

        ttk.Button(
            file_frame, 
            text='open', 
            command=self.open_file
        ).pack(anchor=tk.E, side=tk.RIGHT)

        file_frame.pack(fill=tk.X, padx=30, pady=15)

        details_frame = tk.LabelFrame(self, text="Details")
        self.count_label = ttk.Label(details_frame, text="Count: 0")
        self.dup_label = ttk.Label(details_frame, text="Duplicate keys: 0")

        self.count_label.pack(anchor=tk.W)
        self.dup_label.pack(anchor=tk.W)

        details_frame.pack(fill=tk.X, padx=30, pady=15)

        self.phone_label = ttk.Label(text="0000****000", font=("Consolas", 40))
        self.phone_label.pack()

        columns = ("Index", "Phone Number", "Username")
        self.winner_table = ttk.Treeview(
            self, 
            columns=columns, 
            show='headings', 
            height=5
        )

        for col in columns:
            self.winner_table.column(col, width=112)
            self.winner_table.heading(col, text=col)  

        self.winner_table.pack(padx=30, pady=15)

        self.start_btn = ttk.Button(
            self, 
            text='Find New Winner', 
            command=self.find_winner, 
            state='disable'
        )
        self.start_btn.pack(fill=tk.X, padx=30, pady=15)


    def open_file(self) -> None:
        """Open and load database file"""

        file = filedialog.askopenfilename(
            initialdir = "/",
            title = "Select Database",
            filetypes = (("sqlite database", "*.*"),)
        )
        if file:
            self.load_db(file)


    def load_db(self, dir: str) -> None:
        """
        Load sqlite database from input `dir` and display count of database rows
        """

        # make connection to database
        self.conn = sqlite3.connect(dir)
        self.curs = self.conn.cursor()

        # get count of all rows
        self.curs.execute("SELECT COUNT(user_id) FROM users")
        count = self.curs.fetchone()[0]

        # find duplicate phone numbers
        self.curs.execute(
            "SELECT SUM(counts.cnt) as total "
            "FROM ( "
                "SELECT COUNT(phone_number) as cnt "
                "FROM users "
                "GROUP BY phone_number "
                "HAVING COUNT(*) > 1 "
            ") counts "
        )
        duplicates = self.curs.fetchone()[0]

        # update labels
        self.file_label['text'] = "Databese successfully loaded"
        self.count_label['text'] = "Count: " + str(count)
        self.dup_label['text'] = "Duplicate keys: " + str(duplicates)
        self.start_btn['state'] = 'enable'


    def get_random(self) -> 'tuple[str]':
        """Return a random row from database with sqlite's builtin `RANDOM()` method"""

        self.curs.execute("SELECT * FROM users ORDER BY RANDOM() LIMIT 1")
        res = self.curs.fetchone()
        return res[0], res[1], to_phone(res[2])


    def update_table(self) -> None:
        """Add last winner to winners table"""

        last = self.winners[-1]
        self.winner_table.insert(
            "", tk.END, values=(
                len(self.winners), 
                hide_phone(last[2]), 
                last[1]
            )
        )


    def do_animation(self, index: int = 0, next: int = 0, max: int = 0) -> None:
        """Display finding number animation"""

        # Go to the next number when the counter reaches the digit of phone number.
        if next > max:
            index += 5 if index == 3 else 1

            # return when animation is done on all digits
            if index > 10:
                self.update_table()
                return

            # set max of next digit of phone number
            max = int(self.winners[-1][2][index])
            next = 0
        else:
            # show the increased digit
            label = self.phone_label['text']
            self.phone_label['text'] = label[:index] + str(next) + label[index+1:]
        
        # add timer for next counter animation
        threading.Timer(0.2, self.do_animation, (index, next+1, max)).start()


    def find_winner(self):
        """Find and display winners"""

        # reset the phone number label
        self.phone_label['text'] = "0000****000"

        # find a new winner and do counter animations
        self.winners.append(self.get_random())
        self.do_animation()


def hide_phone(phone: str) -> str:
    """Hide 4 digits of given phone number"""

    return ''.join('*' if x>3 and x<8 else phone[x] for x in range(len(phone)))


def to_phone(phone: int) -> str:
    """Remove 98 from phone number"""

    return '0' + str(phone)[2:]


if __name__ == "__main__":
    # Make an app with given winner counts
    app = App()
    app.mainloop()

    # Save winners to a file
    with open('winners.json', 'w') as file:
        json.dump(app.winners, file)