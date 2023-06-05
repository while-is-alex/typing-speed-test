from tkinter import *
from tkmacosx import Button


class Window(Tk):
    def __init__(self, test):
        super().__init__()
        self.test_brain = test
        self.title('Typing speed test')
        self.config(
            padx=20,
            bg='#F1F7B5'
        )
        self.minsize(width=1200, height=600)
        self.font = 'Verdana'

        # Configures all the rows and columns to occupy space, including empty ones
        for i in range(6):
            self.columnconfigure(i, weight=1)
        for i in range(6):
            self.rowconfigure(i, weight=1)

        self.user_input = ''
        self.sentence = ''
        self.timer = ''

    def home_ui(self):
        """Initializes the home screen. Contains the path to the test."""
        bg_color = '#7286D3'
        title_font_color = '#FAAB78'
        font_color = '#E5E0FF'
        button_color = '#FFF2F2'

        self.config(
            bg=bg_color
        )

        title = Label(
            self,
            text='TYPING SPEED TEST',
            fg=title_font_color,
            bg=bg_color,
            font=(self.font, 40, 'bold')
        )
        title.place(x=340, y=130)

        instructions = Label(
            self,
            text='When you\'re finished with a sentence, just press space bar.\n'
                 'You can ignore capital letters.\n\n'
                 'The test will run for 60 seconds.',
            bg=bg_color,
            fg=font_color,
            font=(self.font, 20))
        instructions.place(x=276, y=300)

        start_button = Button(
            self,
            text='START',
            bg=button_color,
            fg=bg_color,
            highlightbackground=bg_color,
            height=30,
            width=80,
            borderless=1,
            command=lambda: self.test_brain.call_test_ui(self)
        )
        start_button.place(x=532, y=480)

    def call_home(self):
        """Clears the previous widgets on screen.
        Calls the home screen."""
        for widget in self.winfo_children():
            widget.destroy()
        return self.home_ui()

    def test_ui(self, sentences):
        """Initializes the test screen. Contains the path to the test."""
        bg_color = '#D57E7E'
        title_font_color = '#CEAB93'
        font_color = '#FFE1AF'
        button_color = '#CEAB93'

        self.config(
            bg=bg_color
        )

        test_title = Label(
            self,
            text='TEST',
            bg=bg_color,
            fg=title_font_color,
            font=(self.font, 40, 'bold')
        )
        test_title.place(x=520, y=50)

        words_per_minute = Text(
            self,
            bg=bg_color,
            fg=font_color,
            height=2,
            width=20,
            highlightthickness=0,
            font=(self.font, 15, 'bold'),
        )
        words_per_minute.tag_config('right', justify='right')
        words_per_minute.insert(INSERT, 'WPM: ')
        words_per_minute.tag_add('right', '1.0', 'end')
        words_per_minute.place(x=950, y=15)
        words_per_minute.config(state=DISABLED)

        self.sentence = Text(
            self,
            bg=bg_color,
            fg=font_color,
            height=2,
            width=40,
            highlightthickness=0,
            highlightbackground=title_font_color,
            font=(self.font, 30),
            wrap=WORD,
        )
        self.sentence.tag_config('center', justify='center')
        self.sentence.insert(INSERT, sentences[0])
        self.sentence.tag_add('center', '1.0', 'end')
        self.sentence.place(x=175, y=150)
        self.sentence.config(state=DISABLED)

        self.timer = Label(
            self,
            text='0:60',
            bg=bg_color,
            fg='#D49F9F',
            font=(self.font, 20, 'bold')
        )
        self.timer.place(x=548, y=300)

        self.user_input = Entry(
            width=50,
            background='white',
            fg='black',
            bd=1,
            highlightcolor=bg_color,
            highlightthickness=0,
            font=(self.font, 15)
        )
        self.user_input.place(x=325, y=380)
        self.user_input.insert(0, 'Transcribe the text above here')

        def temp_text():
            self.user_input.delete(0, 'end')

        # Deletes the instruction text within the entry
        # when the user clicks on it
        self.user_input.bind('<Button-1>', lambda e: temp_text())

        # Checks for when the user starts the test (inserts a key input into the entry)
        # and starts the timer
        self.user_input.bind(
            '<Key>',
            lambda e: self.test_brain.start_timer(self, self.timer)
        )
        # Checks for matches in user input versus the text on screen
        self.user_input.bind(
            '<space>',
            lambda e: [
                self.test_brain.run_test(self.user_input.get(), self.sentence, self.user_input),
                self.test_brain.words_per_minute(words_per_minute)
            ]
        )

        stop_button = Button(
            self,
            text='STOP',
            bg=button_color,
            fg=font_color,
            highlightbackground=bg_color,
            height=30,
            width=80,
            borderless=1,
            command=lambda: [
                self.test_brain.stop_timer(self, user_input=self.user_input.get()),
                self.test_brain.calculate_results(self)
            ]
        )
        stop_button.place(x=532, y=480)

    def results_ui(self, wpm_count, accuracy_count, net_count):
        """Initializes the results screen. Contains the path to the test."""
        bg_color = '#6D8B74'
        title_font_color = '#D0C9C0'
        font_color = '#EFEAD8'
        button_color = '#EEE4AB'

        self.config(
            bg=bg_color
        )

        result = Label(
            self,
            text='RESULT',
            fg=title_font_color,
            bg=bg_color,
            font=(self.font, 40, 'bold')
        )
        result.place(x=485, y=50)

        explanation = Label(
            self,
            text='The test takes into account every word typed (correct or incorrect)\n'
                 'to calculate the words per minute (WPM).\n'
                 'Your accuracy is how many words you typed correctly.',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 20)
        )
        explanation.place(x=230, y=130)

        wpm = Label(
            self,
            text='WPM',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 30, 'bold'))
        wpm.place(x=170, y=260)

        wpm_number = Label(
            self,
            text=wpm_count,
            fg=font_color,
            bg=bg_color,
            font=(self.font, 60, 'bold'))
        wpm_number.place(x=173, y=330)

        mult_symbol = Label(
            self,
            text='X',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 40, 'bold'))
        mult_symbol.place(x=350, y=340)

        accuracy = Label(
            self,
            text='ACCURACY',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 30, 'bold'))
        accuracy.place(x=480, y=260)

        accuracy_number = Label(
            self,
            text=f'{accuracy_count}%',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 60, 'bold'))
        accuracy_number.place(x=505, y=330)

        equals = Label(
            self,
            text='=',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 55, 'bold'))
        equals.place(x=740, y=332)

        net = Label(
            self,
            text='NET SPEED',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 30, 'bold'))
        net.place(x=850, y=260)

        net_number_wpm = Label(
            self,
            text='\n\n\n\nWPM',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 20, 'bold'))
        net_number_wpm.place(x=913, y=320)

        net_number = Label(
            self,
            text=f'{net_count}',
            fg=font_color,
            bg=bg_color,
            font=(self.font, 60, 'bold'))
        net_number.place(x=900, y=330)

        home_button = Button(
            self,
            text='HOME',
            bg=button_color,
            fg=bg_color,
            highlightbackground=bg_color,
            height=30,
            width=80,
            borderless=1,
            command=lambda: [
                self.call_home(),
                self.test_brain.reset_test()
            ]
        )
        home_button.place(x=532, y=480)
