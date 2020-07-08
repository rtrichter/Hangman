# Hangman by Ryan Richter
#
# Based on the classic game
# This is a text only based version of hangman
# In place of the hanging man there is a guess counter that can be manipulated.
# The counter can have any number of guesses to make the game near impossible or childs play
#
# To run in another file use the one of the following scripts
#
#import hangman
#hangman.run_game()
#
#       OR
#
#from hangman import run_game
#run_game()

import re
import random


def welcome():
    # Welcomes the players and gives some essential information
    print('Welcome to hangman')
    print('One person will pick a word or phrase then the other will guess')
    print("Make sure the guesser isn't looking when you pick")
    print('The guesser will see a line for each character and a space when appropriate')
    print('When prompted the guesser will enter a letter or word they think is correct')
    print('If it is correct, the skeleton of the word will begin to fill in')
    print('If not the guesses left count will decrease by one')
    print('The game is not case sensitive and numbers are allowed')
    print('The game will now begin')
    print('Good luck to both of you!')
    print('')
    input('Press enter to continue')
    print('')


def random_word():
    # Generates a random word for lonely people like me.
    with open('1-1000.txt') as lines:
        line = lines.readlines()
        word = random.choice(line)
        return word


def use_bot(var):
    # Determines if a word should be generated or if another player will pick a word
    bot = input('For 1 player, type 1. \nFor 2 players type 2: ')
    if bot == '1':
        var['bot'] = 'true'
    return var


def setup():
    # Begins dict containing some variables
    variables = {'num_of_guesses': int(input('How many guesses will you give? ')),
                 'letters_guessed': [],
                 'words_guessed': []}
    variables['bot'] = use_bot(variables)
    if variables['bot']:
        variables['hang_word'] = random_word()
    else:
        variables['hang_word'] = input('What is your word or phrase? ')
    variables['guess_prog'] = start_guess_prog(variables['hang_word'])
    clear()
    return variables


def start_guess_prog(hang_word):
    # Makes list of blanks and spaces - skeleton - to show guesser
    # This list represents characters in hang_word
    skeleton1 = []
    for i in range(len(hang_word)):
        skeleton1.append('_ ')
    skeleton2 = [x.start() for x in re.finditer(' ', hang_word)]
    for ele in skeleton2:
        skeleton1[ele] = ' '
    return skeleton1


def status(var):
    # Gives the player a status update on their current position
    print(''.join(var['guess_prog']))
    print('guesses_remaining: ', var['num_of_guesses'])
    print('letters_guessed: ', var['letters_guessed'])
    print('words_guessed: ', var['words_guessed'])


def get_guess():
    # Gets the players guess
    guess = {'player_guess': input('Guess a letter, word, or phrase')}
    return guess


def clear():
    # "clears" the console
    for i in range(15):
        print('')


def already_guessed(var, guess):
    # Ensures the guesser doesn't guess the same word or letter twice
    if guess['let_or_word'] == 'let' and guess['player_guess'] in var['letters_guessed']:
        clear()
        print('your already guessed that \n ')
    elif guess['let_or_word'] == 'word' and guess['player_guess'] in var['words_guessed']:
        clear()
        print('your already guessed that \n ')
    else:
        return 'valid'


def let_or_word(guess):
    # determines if the guess is a letter or word
    if len(guess['player_guess']) != 1:
        guess['let_or_word'] = 'word'
    else:
        guess['let_or_word'] = 'let'
    return guess


def is_letter_match(var, guess):
    # Determines if the letter is a match
    if guess['player_guess'] in var['hang_word']:
        guess['match'] = 'true'
    else:
        guess['match'] = 'false'
    return guess


def is_word_match(var, guess):
    # Determines if the word is a match
    if guess['player_guess'] == var['hang_word']:
        win(var)
    else:
        guess['match'] = 'false'
    return guess


def match(var, guess):
    # calls the is_..._match functions to determine if the guess is correct
    if guess['let_or_word'] == 'let':
        guess = is_letter_match(var, guess)
    else:
        guess = is_word_match(var, guess)
    return guess


def guessed(var, guess):
    # Appends player guess to letters_guessed or words_guessed appropriately
    if guess['let_or_word'] == 'let':
        var['letters_guessed'].append(guess['player_guess'])
    else:
        var['words_guessed'].append(guess['player_guess'])
    return var


def lose_guess(var, guess):
    # Takes guess if wrong. Ignores if correct
    print(str(guess))
    if guess['match'] == 'false':
        var['num_of_guesses'] -= 1
    print(var['num_of_guesses'])
    return var


def win(var):
    # Tells the player they won
    clear()
    print('The Guesser Won!')
    print('The answer was "', var['hang_word'], '"')
    play_again()


def lose(var):
    # Tells the player they lost **sad face**
    clear()
    print('Sorry but you lost **sad face**')
    print('The answer was ', var['hang_word'])
    play_again()


def guess_progress(var, guess):
    # If the guess is a letter and correct, the letter appears in var['guess_prog']
    if guess['let_or_word'] == 'let':
        templst1 = [x.start() for x in re.finditer(guess['player_guess'], var['hang_word'])]
        for ele in templst1:
            var['guess_prog'][ele] = guess['player_guess']
    return var


def guess_prog_done(var):
    # Checks if the guess progress is complete.
    # If it is calls the win function
    if ''.join(var['guess_prog']) == var['hang_word']:
        win(var)


def play_game(var):
    # Calls all functions used in gameplay
    while var['num_of_guesses'] > 0:
        status(var)
        guess = get_guess()
        guess = let_or_word(guess)
        not_prev_guess = already_guessed(var, guess)
        if not_prev_guess:
            guess = match(var, guess)
            var = guessed(var, guess)
            var = lose_guess(var, guess)
            var = guess_progress(var, guess)
            guess_prog_done(var)
            clear()

    lose(var)
    play_again()


def run_game():
    welcome()
    var = setup()
    play_game(var)


def play_again():
    again = input(' \n Type "again" to play again. Type anything else to leave').lower()
    if 'again' in again:
        var = setup()
        play_game(var)
        print('')
    else:
        exit()


if __name__ == '__main__':
    run_game()
