from tkinter import IntVar
from data import texts
import random


class Test:
    def __init__(self):
        """Initializes the parameters that will be used for the test."""
        self.text = ''
        self.current_index = 0
        self.current_sentence = 0
        self.current_correct_words = []
        self.num_correct_words = 0
        self.wpm = 0
        self.total_words = 0
        self.accuracy = 0
        self.net = 0
        self.timer = None
        self.timer_running = False

    def get_text(self):
        """Returns a random text from the database."""
        self.text = random.choice(texts)
        return self.text

    def call_test_ui(self, window):
        """Returns the test screen and provides the sentences for the test."""
        self.text = self.get_text()
        sentences = self.text.split('. ')
        # Clears the previous screen to generate the new one
        for widget in window.winfo_children():
            widget.destroy()
        return window.test_ui(sentences)

    def run_test(self, user_input, tk_text, entry_box):
        self.wpm += 1

        # Divides the whole text to be transcribed into individual sentences
        text_sentences = self.text.split('. ')

        # Gets hold of the last word the user typed and its index
        # and also the word at the same index in the sentence
        current_word = user_input.split()[-1]
        self.current_index = user_input.split().index(user_input.split()[-1])
        sentence_word = text_sentences[self.current_sentence].split()[self.current_index]

        # Checks if it's the first word of the sentence in order to capitalize it
        first_word = False
        if self.current_index == 0:
            first_word = True
        if first_word:
            current_word = current_word.capitalize()

        # Compares the last word the user typed to its equivalent in the sentence
        # to see if the spelling is correct
        if current_word == sentence_word:
            self.current_correct_words.append(current_word)
            self.num_correct_words += 1

        # Checks if the current word being processed has been typed correctly,
        # and if it was, it turns its color to green
        if current_word in self.current_correct_words:
            # Removes a mark (index) left by a previous test
            if self.current_sentence == 0 and self.current_index == 0:
                tk_text.mark_unset('matchEnd')
            # Checks the sentence starting from the last word
            start = 1.0 if 'matchEnd' not in tk_text.mark_names() else 'matchEnd'
            end = 'end'
            count = IntVar()
            regexp = False

            # If the word is found, its color is changed to green
            index = tk_text.search(current_word, start, end, count=count, regexp=regexp)
            if index != "":
                tk_text.mark_set('matchStart', index)
                tk_text.mark_set('matchEnd', '%s+%sc' % (index, count.get()))
                tk_text.tag_config('green', foreground='#B3C890')
                tk_text.tag_add('green', 'matchStart', 'matchEnd')

        # Checks if the user has reached the end of the sentence being transcribed
        # and updates the sentence on screen to a new one
        if len(user_input.split()) == len(text_sentences[self.current_sentence].split()):
            self.total_words += len(text_sentences[self.current_sentence].split())
            self.current_sentence += 1
            self.current_correct_words = []
            self.current_index = 0
            entry_box.delete(0, 'end')
            tk_text.config(state='normal')
            tk_text.delete('1.0', 'end')
            tk_text.tag_config('center', justify='center')
            tk_text.insert('end', text_sentences[self.current_sentence])
            tk_text.tag_add('center', '1.0', 'end')
            tk_text.mark_unset('matchEnd')
            tk_text.config(state='disabled')

    def words_per_minute(self, wpm_text):
        wpm_text.config(state='normal')
        wpm_text.delete('1.0', 'end')
        wpm_text.tag_config('center', justify='right')
        wpm_text.insert('end', f'WPM: {self.wpm}')
        wpm_text.tag_add('center', '1.0', 'end')
        wpm_text.config(state='disabled')

    def start_timer(self, window, timer_label):
        """Initializes the timer and calls the function in charge of
        the timer countdown and also calls the function that
        starts evaluating the user's input versus the text to be transcribed."""
        # Checks if the timer is already running. If it is, the function
        # shouldn't start a new timer.
        if not self.timer_running:
            seconds = 60
            timer_label.config(text=f'0:{seconds}')
            self.timer_countdown(window, timer_label, seconds)
            self.timer_running = True

    def timer_countdown(self, window, timer_label, seconds):
        """Starts the countdown of the timer. If the timer is over,
        it calls the results screen."""
        seconds_string = str(seconds)
        # Handles the formating of the seconds when there's only one digit
        if len(seconds_string) < 2:
            seconds_string = f'0{seconds}'

        if self.timer_running:
            timer_label.config(text=f'0:{seconds_string}')

        if seconds > 0:
            self.timer = window.after(1000, self.timer_countdown, window, timer_label, seconds - 1)
        else:
            self.stop_timer(window)
            self.calculate_results(window)

    def stop_timer(self, window):
        """Stops the timer and updates the total of words to the point
        where the user stopped the test."""
        text_sentences = self.text.split('. ')
        user_input = window.user_input.get()
        user_input = len(user_input.split())
        # Adds the total of words the user attempted to transcribe before pressing the stop button
        # and catches an exception when the user hasn't tried transcribing any word
        if user_input != 0:
            self.total_words += len(text_sentences[self.current_sentence].split()[:self.current_index]) + 1

        # Stops the timer if it was still running
        if self.timer_running:
            window.after_cancel(self.timer)
            self.timer_running = False

    def calculate_results(self, window):
        """Does the math to find out the number of words the user typed per minute,
        the user accuracy (how many words the user typed correctly)
        and the net speed.
        Returns the results screen."""
        # If the user stops the test before it even begins,
        # the number of words typed and total words the user attempted to transcribe
        # will both be 0
        if self.wpm == 0:
            self.accuracy = 0
        elif self.total_words == 0:
            self.accuracy = 0
        else:
            self.accuracy = int((self.num_correct_words / self.total_words) * 100)

        if self.wpm == 0:
            self.net = 0
        else:
            self.net = int(self.wpm * (self.accuracy / 100))

        for widget in window.winfo_children():
            widget.destroy()
        return window.results_ui(self.wpm, self.accuracy, self.net)

    def reset_test(self):
        """Resets all the values left by the previous test."""
        self.text = ''
        self.current_index = 0
        self.current_sentence = 0
        self.current_correct_words = []
        self.num_correct_words = 0
        self.wpm = 0
        self.total_words = 0
        self.accuracy = 0
        self.net = 0
        self.timer = None
        self.timer_running = False
