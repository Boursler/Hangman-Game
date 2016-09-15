import gi, random
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class HangmanWindow(Gtk.Window):
    def __init__(self, dictionary_file_name):
        Gtk.Window.__init__(self, title="Hangman")
        self.set_size_request(800, 800)

        self.timeout_id=None

        self.hangman_figure_list=["hangman_figures/Hangman0.png",
                                  "hangman_figures/Hangman1.png",
                                  "hangman_figures/Hangman2.png",
                                  "hangman_figures/Hangman3.png",
                                  "hangman_figures/Hangman4.png",
                                  "hangman_figures/Hangman5.png",
                                  "hangman_figures/Hangman6.png",
                                  "hangman_figures/Hangman7.png"]
        self.dictionary_file_name = dictionary_file_name
        self.hangman_game = HangmanGame(dictionary_file_name)
        
        main_hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        self.add(main_hbox)

        self.hangman_image=Gtk.Image.new_from_file("hangman_figures/Hangman0.png")
        main_hbox.pack_start(self.hangman_image, True, True, 0)

        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        main_hbox.pack_start(vbox, True, True, 0)

        self.print_entry = Gtk.Label()
        vbox.pack_start(self.print_entry, True, True, 0)

        self.input_dialog=Gtk.Label()
        vbox.pack_start(self.input_dialog, True, True, 0)

        letters_hbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(letters_hbox, True, True, 0)

        self.letter_spaces=Gtk.Label()
        letters_hbox.pack_start(self.letter_spaces, True, True, 0)
        
        self.guessed_letters_entry=Gtk.Label()
        letters_hbox.pack_start(self.guessed_letters_entry, True, True, 0)

        self.new_guess = Gtk.Entry()
        self.new_guess.set_max_length(1)
        self.new_guess.connect("activate", self.submit_guess)
        self.new_guess.connect("changed", self.update_guess_text)
        vbox.pack_start(self.new_guess, True, True, 0)

        hbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.submit_button = Gtk.Button.new_with_label("Submit")
        self.submit_button.connect("clicked", self.submit_guess)
        hbox.pack_start(self.submit_button, True, True, 0)

        self.new_game_button=Gtk.Button.new_with_label("Start New Game")
        self.new_game_button.connect("clicked", self.start_new_game)
        hbox.pack_start(self.new_game_button,True, True, 0)

        self.draw_screen("Welcome to Hangman")
        

    def submit_guess(self, button):
        guess = self.new_guess.get_text()
        output = self.hangman_game.guess_letter(guess)
        print("guessing " + guess)
        self.draw_screen(output)

    def update_guess_text(self, new_guess):
        user_input=self.new_guess.get_text()
        user_input=user_input.lower()
        if self.hangman_game.is_game_over():
            self.input_dialog.set_text("Game Over")
        elif user_input in self.hangman_game.guessed_letters:
            self.input_dialog.set_text("You have already guessed that!")
        elif user_input=='':
            self.input_dialog.set_text("Guess the next letter!")
        elif not user_input.isalpha():
            self.input_dialog.set_text("Invalid input!")
        else:
            self.input_dialog.set_text("Submit to guess " + user_input + "?")

    def draw_screen(self, last_guess_string):
        self.print_entry.set_text(last_guess_string)
        self.new_guess.set_text('')
        output=list()
        self.hangman_image.set_from_file(self.hangman_figure_list[
            self.hangman_game.total_incorrect_guesses])
        for i in self.hangman_game.guessed_letters:
            if i not in self.hangman_game.hangman_word:
                output.append(i)
        output.sort()
        output=" ,".join(output)
      
        self.guessed_letters_entry.set_text(output)
        self.letter_spaces.set_text(self.guessed_letters_string())

    def guessed_letters_string(self):
        output=list(self.hangman_game.hangman_word)
        for i in range(0, len(output)):
            if output[i] not in self.hangman_game.guessed_letters:
                output[i] = '_'
        output = "".join(output)
        return output

    def start_new_game(self, button):
        print("Starting a new game")
        self.hangman_game = HangmanGame(self.dictionary_file_name)
        self.draw_screen("Welcome to Hangman")


class HangmanGame():
    def __init__(self, dictionary_file_name):
        with open(dictionary_file_name) as f:
            self.dictionary =f.read().split()
        self.total_incorrect_guesses=0
        self.guessed_letters=set()
        self.hangman_word=random.choice(self.dictionary)
        self.unguessed_letters=set(self.hangman_word)
        self.max_guesses=7

    def is_game_over(self):
        if (len(self.unguessed_letters)==0 or
            self.total_incorrect_guesses>=self.max_guesses):
            return True
        else:
            return False

    def guess_letter(self, guess):
        guess=guess.lower()
        if not self.is_game_over():
            if(len(guess) > 1 or not guess.isalpha()):
                return_string = "Invalid response, stay in the spirit of the game."

            elif guess in self.guessed_letters:
                return_string =  'You already guessed that!'

            elif guess in self.unguessed_letters:
                self.unguessed_letters.remove(guess)
                self.guessed_letters.add(guess)
                return_string = 'You chose wisely'

            else:
                self.total_incorrect_guesses += 1
                self.guessed_letters.add(guess)
                return_string = 'You chose poorly'

        if(len(self.unguessed_letters) == 0):
            return_string = "You win!!"

        elif(self.total_incorrect_guesses >= self.max_guesses):
            return_string = "You have lost"

        return return_string


win=HangmanWindow("hangman_words.txt")
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
