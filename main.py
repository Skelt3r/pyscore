from tkinter import  Button, Entry, Frame, Label, messagebox, Tk, Toplevel
from sys import exit


class Scoreboard:
    def __init__(self, num_rounds, num_players):
        self.height = 6
        self.width = 12

        self.bg_color = 'black'
        self.fg_color = 'white'
        
        self.button_font = ('Arial', 12, 'bold')
        self.large_button_font = ('Arial', 36, 'bold')
        self.logo_font = ('Terminal', 64, 'underline')

        self.num_rounds = num_rounds
        self.num_players = num_players

        self.board = list()
        self.root = Tk()
        self.root.title('PyScore')
        self.root.wm_attributes('-topmost', True)
        self.root.wm_attributes('-fullscreen', True)

        self.bg_frame = Frame(self.root, bg=self.bg_color)
        self.bg_frame.pack(expand=True, fill='both')

        x_button = Button(self.bg_frame, bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.button_font, text='X', command=exit, padx=5, pady=5)
        x_button.pack(padx=5, pady=5, side='top', anchor='ne')

        self.generate_menu()
        self.root.mainloop()
    

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
        
        def cancel(event=None):
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
        Button(button_frame, text='Cancel', command=cancel).pack(anchor='c', padx=5, pady=5, side='left')

        text_entry.focus()
        text_entry.bind('<Return>', ok)
        text_entry.bind('<Escape>', cancel)


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


    def reset_board(self):
        self.board.clear()
        self.scoreboard_frame.destroy()
        self.generate_board()

    
    def end_game(self):
        self.board.clear()
        self.scoreboard_frame.destroy()
        self.generate_menu()


    def generate_menu(self):
        self.logo_label = Label(self.bg_frame, bg=self.bg_color, fg=self.fg_color, font=self.logo_font, text='PyScore')
        self.logo_label.place(relx=0.5, rely=0.3, anchor='c')

        self.start_button = Button(self.bg_frame, command=self.generate_board, bd=5, relief='ridge', font=self.large_button_font, text='Start Game')
        self.start_button.place(relx=0.5, rely=0.5, anchor='c')

        self.exit_button = Button(self.bg_frame, command=exit, bd=5, relief='ridge', font=self.large_button_font, text='Exit')
        self.exit_button.place(relx=0.5, rely=0.6, anchor='c')
    

    def generate_board(self):
        self.logo_label.destroy()
        self.start_button.destroy()
        self.exit_button.destroy()

        self.scoreboard_frame = Frame(self.bg_frame)
        self.scoreboard_frame.place(anchor='c', relx=0.5, rely=0.5)

        header_frame = Frame(self.scoreboard_frame, bg=self.bg_color)
        header_frame.pack(side='top')

        name_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, text=f'Name')
        name_label.pack(side='left', anchor='s')

        for n in range(self.num_rounds):
            round_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, text=f'R{n+1}')
            round_label.pack(side='left', anchor='s')

        for p in range(self.num_players):
            temp_list = list()

            temp_frame = Frame(self.scoreboard_frame)
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

        score_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, text=f'Score')
        wins_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, text=f'Wins')
        score_label.pack(side='left', anchor='s')
        wins_label.pack(side='left', anchor='s')

        button_frame = Frame(self.scoreboard_frame, bg=self.bg_color)
        button_frame.pack(side='bottom', expand=True, fill='both')

        reset_button = Button(button_frame, command=self.reset_board, bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.button_font, text='Reset Board', pady=5)
        end_button = Button(button_frame, command=self.end_game, bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.button_font, text='End Game', pady=5)
        reset_button.pack(side='left', anchor='c', expand=True, fill='x')
        end_button.pack(side='left', anchor='c', expand=True, fill='x')

        self.data = dict(enumerate(self.board))
        

if __name__ == '__main__':
    scoreboard = Scoreboard(10, 10)
