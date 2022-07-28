import json
import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
import threading


class App(tk.Tk):
    def __init__(self, winners_count: int):
        super().__init__()

        # Make winner variables
        self.winners_count = winners_count
        self.winners = []

        # Initialize window and components
        self.title("RemGanG Draw")
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

        self.phone_label = ttk.Label(text="0000****000", font=("Consolas", 43))
        self.phone_label.pack()

        columns = ("Index", "Phone Number", "Username")
        self.winner_table = ttk.Treeview(
            self, 
            columns=columns, 
            show='headings', 
            height=self.winners_count
        )

        for col in columns:
            self.winner_table.column(col, width=112)
            self.winner_table.heading(col, text=col)  

        self.winner_table.pack(padx=30, pady=15)

        self.start_btn = ttk.Button(
            self, 
            text='Find New Winner', 
            command=self.find_winner, 
            # state='disable'
        )
        self.start_btn.pack(fill=tk.X, padx=30, pady=15)


    def open_file(self) -> None:
        """Open and load database file"""

        file = filedialog.askopenfilename(
            initialdir = "/",
            title = "Select Database",
            filetypes = (("Json Database", "*.json"),)
        )
        if file:
            self.load_db(file)


    def load_db(self, dir: str) -> None:
        """
        Load sqlite database from input `dir` and display count of database rows
        """

        self.conn = sqlite3.connect(dir)
        self.curs = self.conn.cursor()
        self.curs.execute("SELECT COUNT(*) FROM table")
        count = self.curs.fetchone()[0]
        self.file_label['text'] = "Databese successfully loaded"
        self.count_label['text'] = "Count: " + str(count)
        self.start_btn['state'] = 'enable'


    def get_random(self) -> 'tuple[str]':
        """Return random a row from database with sqlite's builtin `RANDOM()` method"""

        return ("09195602518", "@Sina_P")
        # self.curs.execute("SELECT * FROM table ORDER BY RANDOM() LIMIT 1")
        # return self.curs.fetchone()


    def update_table(self) -> None:
        """Add last winner to winners table"""

        last = self.winners[-1]
        self.winner_table.insert(
            "", tk.END, values=(
                len(self.winners), 
                hide_phone(last[0]), 
                last[1]
            )
        )


    def do_animation(self, index: int = 0, next: int = 0, max: int = 0) -> None:
        """Display finding number animation"""

        if next > max:
            index += 5 if index == 3 else 1
            if index > 10:
                self.update_table()
                return
            max = int(self.winners[-1][0][index])
            next = 0
        else:
            label = self.phone_label['text']
            self.phone_label['text'] = label[:index] + str(next) + label[index+1:]
        
        threading.Timer(0.2, self.do_animation, (index, next+1, max)).start()


    def find_winner(self):
        """Find and display winners"""

        self.phone_label['text'] = "0000****000"
        if len(self.winners) < self.winners_count:
            self.winners.append(self.get_random())
            self.do_animation()


def hide_phone(phone: str) -> str:
    """Hide 4 digits of given phone number"""

    return ''.join('*' if x>3 and x<8 else phone[x] for x in range(len(phone)))


if __name__ == "__main__":
    # Make an app with given winner counts
    app = App(winners_count=5)
    app.mainloop()

    with open('winners.json', 'w') as file:
        json.dump(app.winners, file)