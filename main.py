from tkinter import  Button, Entry, Frame, Label, OptionMenu, messagebox, StringVar, Tk, Toplevel
from sys import exit


class Scoreboard:
    def __init__(self):
        self.height = 4
        self.width = 8

        self.bg_color = 'black'
        self.fg_color = 'white'
        
        self.button_font = ('Arial', 12, 'bold')
        self.large_button_font = ('Arial', 28, 'bold')
        self.logo_font = ('Terminal', 64, 'underline')

        self.board = list()
        self.players_range = [i for i in range(1, 11)]
        self.rounds_range = [i for i in range(1, 16)]

        self.players_val = '4'
        self.rounds_val = '10'
        
        self.root = Tk()
        self.root.title('PyScore')
        self.root.wm_attributes('-fullscreen', True)

        self.bg_frame = Frame(self.root, bg=self.bg_color)
        x_button = Button(self.bg_frame, bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.button_font, text='X', command=exit, padx=10, pady=5)
        
        self.bg_frame.pack(expand=True, fill='both')
        x_button.pack(side='top', anchor='ne')

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
        prompt_label = Label(win, text=prompt)
        text_entry = Entry(win)
        button_frame = Frame(win)
        ok_button = Button(button_frame, text='OK', command=ok)
        cancel_button = Button(button_frame, text='Cancel', command=cancel)
        
        prompt_label.pack(anchor='c', padx=5, pady=5, side='top')
        text_entry.pack(anchor='c', padx=5, pady=5, side='top')
        button_frame.pack(anchor='c', side='top')
        ok_button.pack(anchor='c', padx=5, pady=5, side='left')
        cancel_button.pack(anchor='c', padx=5, pady=5, side='left')

        text_entry.focus()
        text_entry.bind('<Return>', ok)
        text_entry.bind('<Escape>', cancel)
        win.wm_attributes('-topmost', True)


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
            topscore = 0
            index = 0
            scores = [round[i] for i in range(self.num_players)]
            
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
        self.menu_frame = Frame(self.bg_frame, bd=5, relief='ridge', bg=self.bg_color)
        self.players_frame = Frame(self.menu_frame, bg=self.bg_color)
        self.rounds_frame = Frame(self.menu_frame, bg=self.bg_color)

        self.logo_label = Label(self.menu_frame, bg=self.bg_color, fg=self.fg_color, font=self.logo_font, text='PyScore')
        self.players_label = Label(self.players_frame, bg=self.bg_color, fg=self.fg_color, font=self.large_button_font, text='Players:')
        self.rounds_label = Label(self.rounds_frame, bg=self.bg_color, fg=self.fg_color, font=self.large_button_font, text='Rounds:')

        self.players_var = StringVar(self.menu_frame, self.players_val)
        self.rounds_var = StringVar(self.menu_frame, self.rounds_val)
        
        self.start_button = Button(self.menu_frame, command=self.generate_board, bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Start Game')
        self.exit_button = Button(self.menu_frame, command=exit, bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Exit')
        
        self.players_opts = OptionMenu(self.players_frame, self.players_var, *self.players_range)
        self.rounds_opts = OptionMenu(self.rounds_frame, self.rounds_var, *self.rounds_range)

        self.players_opts.config(bg=self.bg_color, fg=self.fg_color, font=self.large_button_font, width=2)
        self.players_opts['menu'].config(font=self.large_button_font)

        self.rounds_opts.config(bg=self.bg_color, fg=self.fg_color, font=self.large_button_font, width=2)
        self.rounds_opts['menu'].config(font=self.large_button_font)
        
        self.menu_frame.place(relx=0.5, rely=0.5, anchor='c')
        self.logo_label.pack(side='top', padx=40, pady=40)
        self.players_frame.pack(side='top', pady=25)
        self.rounds_frame.pack(side='top', pady=25)
        self.players_label.pack(side='left', padx=5, pady=10)
        self.rounds_label.pack(side='left', padx=5, pady=10)
        self.players_opts.pack(side='right', padx=10)
        self.rounds_opts.pack(side='right', padx=10)
        self.start_button.pack(side='left', anchor='c', padx=40, pady=50)
        self.exit_button.pack(side='left', anchor='c', padx=40)


    def generate_board(self):
        self.players_val = self.players_var.get()
        self.rounds_val = self.rounds_var.get()
        self.num_players = int(self.players_var.get())
        self.num_rounds = int(self.rounds_var.get())

        self.menu_frame.destroy()
        self.start_button.destroy()
        self.exit_button.destroy()

        self.scoreboard_frame = Frame(self.bg_frame)
        header_frame = Frame(self.scoreboard_frame, bg=self.bg_color)
        
        name_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.button_font, text=f'Name')

        self.scoreboard_frame.place(anchor='c', relx=0.5, rely=0.5)
        header_frame.pack(side='top')
        name_label.pack(side='left', anchor='s')

        for n in range(self.num_rounds):
            round_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.button_font, text=f'R{n+1}')
            round_label.pack(side='left', anchor='s')

        for p in range(self.num_players):
            temp_list = list()

            temp_frame = Frame(self.scoreboard_frame)
            temp_frame.pack(side='top')

            temp_button1 = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text=f'Player {p+1}')
            temp_button1.config(command=lambda b=temp_button1: self.set_value(b, 'Enter a player/team name:'))
            temp_button1.pack(side='left')

            temp_list.append(temp_button1)

            for n in range(self.num_rounds):
                temp_button2 = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font,)
                temp_button2.config(command=lambda b=temp_button2: self.set_value(b, 'Enter a score for this round:', True))
                temp_button2.pack(side='left')

                temp_list.append(temp_button2)
            
            temp_button3 = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text='0')
            temp_button4 = Button(temp_frame, bg=self.bg_color, fg=self.fg_color, height=self.height, width=self.width, font=self.button_font, text='0')

            temp_button3.pack(side='left')
            temp_button4.pack(side='left')

            temp_list.extend([temp_button3, temp_button4])
            self.board.extend([temp_list])

        button_frame = Frame(self.scoreboard_frame, bg=self.bg_color)

        score_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.button_font, text=f'Score')
        wins_label = Label(header_frame, bd=4, bg=self.bg_color, fg=self.fg_color, height=self.height//2, width=self.width, font=self.button_font, text=f'Wins')

        reset_button = Button(button_frame, command=self.reset_board, bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='Reset Board', pady=5)
        end_button = Button(button_frame, command=self.end_game, bg=self.bg_color, fg=self.fg_color, bd=5, relief='ridge', font=self.large_button_font, text='End Game', pady=5)

        score_label.pack(side='left', anchor='s')
        wins_label.pack(side='left', anchor='s')
        button_frame.pack(side='bottom', expand=True, fill='both')
        reset_button.pack(side='left', anchor='c', expand=True, fill='x')
        end_button.pack(side='left', anchor='c', expand=True, fill='x')

        self.data = dict(enumerate(self.board))
        

if __name__ == '__main__':
    scoreboard = Scoreboard()
