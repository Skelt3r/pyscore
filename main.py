from tkinter import  Button, Entry, Frame, Label, messagebox, Tk, Toplevel
from rich import print
from sys import exit


class Scoreboard:
    def __init__(self, num_rounds, num_players):
        self.height = 6
        self.width = 12
        self.bg_color = 'black'
        self.fg_color = 'white'
        self.num_rounds = num_rounds
        self.num_players = num_players
        self.board = list()
    

    def set_value(self, button, prompt, int_only=False):

        def ok(event=None):
            if int_only:
                try:
                    button.config(text=int(text_entry.get()))
                    self.calculate_total_score()
                    self.calculate_wins()
                    win.destroy()
                except ValueError:
                    messagebox.showerror('Integer required', 'Score must be an integer.')
            else:
                button.config(text=text_entry.get())
                win.destroy()

        win = Toplevel(self.root)
        win.title('Name')
        win.wm_attributes('-topmost', True)

        Label(win, text=prompt).pack(anchor='c', padx=5, pady=5, side='top')

        text_entry = Entry(win)
        text_entry.pack(anchor='c', padx=5, pady=5, side='top')

        button_frame = Frame(win)
        button_frame.pack(anchor='c', side='top')

        Button(button_frame, text='OK', command=ok).pack(anchor='c', padx=5, pady=5, side='left')
        Button(button_frame, text='Cancel', command=win.destroy).pack(anchor='c', padx=5, pady=5, side='left')

        text_entry.focus()
        text_entry.bind('<Return>', ok)
        text_entry.bind('<Escape>', win.destroy)


    def calculate_total_score(self):
        for player in self.data.items():
            rounds = player[1][1:-2]
            button = player[1][-2]
            score = sum([int(r['text']) for r in rounds if r['text'] != str()])
            button['text'] = score
            

    def calculate_wins(self):
        compare = list()
        wins = dict()

        for i in range(self.num_players):
            wins[f'i{i}'] = 0

        for i in range(self.num_rounds):
            temp_list = list()
            
            for player in self.data.items():
                rounds = player[1][1:-2]
                temp_list.append(int(rounds[i]['text']) if rounds[i]['text'] != str() else 0)
            
            compare.append(temp_list)
        
        for round in compare:
            scores = list()
            topscore = 0
            index = 0

            for i in range(self.num_players):
                scores.append(round[i])
            
            for score in scores:
                if score > topscore:
                    topscore = score
            
            for score in scores:
                if score == topscore and score != 0:
                    wins[f'i{index}'] += 1

                index += 1

        index = 0

        for num in wins.values():
            self.data[index][-1]['text'] = num
            index += 1


    def menu(self):
        pass
    

    def run(self):
        self.root = Tk()
        self.root.title('Scoreboard')
        self.root.wm_attributes('-topmost', True)
        self.root.wm_attributes('-fullscreen', True)

        bg_frame = Frame(self.root, bg=self.bg_color)
        bg_frame.pack(expand=True, fill='both')

        scoreboard_frame = Frame(bg_frame)
        scoreboard_frame.place(anchor='c', relx=0.5, rely=0.5)

        x_button = Button(bg_frame, bd=5, relief='ridge', font=('Arial', 12, 'bold'), text='X', command=exit, padx=5, pady=5)
        x_button.pack(padx=5, pady=5, side='top', anchor='ne')

        header_frame = Frame(scoreboard_frame, bg=self.bg_color)
        header_frame.pack(side='top')

        Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, text=f'Name').pack(side='left', anchor='s')

        for n in range(self.num_rounds):
            Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, text=f'R{n+1}').pack(side='left', anchor='s')

        for p in range(self.num_players):
            temp_list = list()

            temp_frame = Frame(scoreboard_frame)
            temp_frame.pack(side='top')

            temp_button1 = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, text=f'Player {p+1}')
            temp_button1.config(command=lambda b=temp_button1: self.set_value(b, 'Enter a player/team name:'))
            temp_button1.pack(side='left')

            temp_list.append(temp_button1)

            for n in range(self.num_rounds):
                temp_button2 = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width)
                temp_button2.config(command=lambda b=temp_button2: self.set_value(b, 'Enter a score for this round:', True))
                temp_button2.pack(side='left')

                temp_list.append(temp_button2)
            
            temp_button3 = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, text='0')
            temp_button4 = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, text='0')
            temp_button3.pack(side='left')
            temp_button4.pack(side='left')

            temp_list.extend([temp_button3, temp_button4])
            self.board.extend([temp_list])

        Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, text=f'Score').pack(side='left', anchor='s')
        Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, text=f'Wins').pack(side='left', anchor='s')

        self.data = dict(enumerate(self.board))
        
        self.root.mainloop()

if __name__ == '__main__':
    scoreboard = Scoreboard(10, 4)
    scoreboard.run()
