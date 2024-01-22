# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
TOTAL_SCORE = 0
WILDCARD = "*"
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	
def get_word_score(word, n):
    """
    Returns the score for a word. 
  
	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    score = 0
    word = word.lower()
    #calculate the sum of the points of the letters used
    letters_list = list(word)
    for c in letters_list:
        score += SCRABBLE_LETTER_VALUES[c]
    #calculate the second component and if the result is less than one or the string is empty, set it equal to one
    second_component = (7*len(word)) - 3*(n-len(word))

    if second_component <= 1:
       if word == "" or word == " ":
           second_component = 0
       else:
           second_component = 1
    return score*second_component

def display_hand(hand):
    """
    Displays the letters currently in the hand.
    """
    hand_display = "Current Hand: "
    for letter in hand.keys():
        for j in range(hand[letter]):
            hand_display += letter
            hand_display += " "
    return hand_display

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    num_vowels -= 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    wildcard_present = False
    for c in hand:
        if hand[c] == "*":
            wildcard_present = True 
            break
    if wildcard_present == False:
        hand["*"] = 1
    return hand

def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    returns: dictionary (string -> int)
    """
    word = word.lower()
    new_hand = hand.copy()
    real_new_hand = {}
    word_list = list(word)
    for c in word_list:
        if c in new_hand:
            new_hand[c] -= 1
        else:
            new_hand[c] = 0
    for c in new_hand:
        if new_hand[c] > 0:
            if new_hand[c] in real_new_hand:
                real_new_hand[c] += 1
            else:
                real_new_hand[c] = 1
    return real_new_hand

def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    """
    word = word.lower()
    hand_copy = hand.copy()
    wildcard_valid = False
    wildcard_used = False
    valid_word = False
    wildcard_index = -1
    
    for char in word:
        if char =="*":
            wildcard_index = word.index("*")
            wildcard_used = True
    if wildcard_index > -1:
        vowels = ["a","e","i","o","u"]
        for vowel in vowels:
            list_of_word = list(word)
            list_of_word[wildcard_index] = vowel
            updated_word = "".join(list_of_word)
            if updated_word in word_list:
                wildcard_valid = True
                break
            
    if wildcard_used == True:
         if wildcard_valid == True:
             valid_word = True
    elif word in word_list:
        valid_word = True
        
    listed_word =list(word)     #Makes sure the char are in the hand
    for c in listed_word:
        if c in hand_copy:
            hand_copy[c] -= 1
        else:
            hand_copy[c] = -1
    for c in hand_copy:
        if hand_copy[c] < 0:
            valid_word = False
    return valid_word

def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    """
    length = 0
    for c in hand:
        length += hand[c]
    return length

def play_hand(hand, word_list):
    """
    Allows the user to play a hand
    """
    global TOTAL_SCORE 
    play = True
    total_points = 0
    while play == True:
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print(display_hand(hand))
        user_guess = str(input("Enter word or '!!' to indicate that you are finsihed: "))
        if user_guess == "!!":
            play == False
            break 
        valid_word = False
        valid_word = is_valid_word(user_guess,hand,word_list)
        if valid_word == True:
             score = get_word_score(user_guess, len(hand))
             total_points += score
             print("'"+user_guess+"' earned",score,"points. Total",total_points)
             hand = update_hand(hand, user_guess)
        elif valid_word == False:
            print("That is not a valid word, try again")
    print()        
    print("Game over! Total Score:",total_points)
    TOTAL_SCORE += total_points
 
def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.
    """

    new_char = ""
    letter_odds = random.randint(1, 26)
    if letter_odds in range(1,5):
        new_char = random.choice(VOWELS)
    else:
        new_char = random.choice(CONSONANTS)
    copy_hand = hand.copy()
    for char in hand.keys():
        if char == letter:
            del copy_hand[char]
    copy_hand[new_char] = hand[letter]

    return copy_hand

def play_game(word_list):
    """
    Allows the user to play a game, with a desired number of hands
    """
    num_hands = int(input("Enter total number of hands: "))
    count = 0
    deal = True
    while count < num_hands:
        if deal ==  True:
            hand = deal_hand(HAND_SIZE)
        print(display_hand(hand))
        sub = str(input("Would you like to substitute a letter? (yes/no) "))
        sub = sub.lower()
        if sub == "yes":
            sub_letter = str(input("Which letter would you like to substitute? "))
            hand = substitute_hand(hand, sub_letter)
        play_hand(hand, word_list)
        if count == (num_hands - 2):
            again = str(input("Would you like to replay that hand? "))
            again = again.lower()
            if again == "yes":
                deal == False
        count += 1
    print("Score Across Hands: ", TOTAL_SCORE)
            

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
