import random

wod = 'SHIRE'

correct_letters = {}
semi_correct_letters = []
incorrect_letters = []
guess = ""

with open ('5_words.txt', 'r') as f:
    word_bank = f.readlines()
    word_bank = [word.strip().upper() for word in word_bank]

for i in range (99):
    guess = random.choice(word_bank)
    print(guess)
    if guess == wod:
        print(i)
        break
    else:
        for i in range(5):
            print("Guess letter: " + guess[i] + " wod letter: " + wod[i])
            if guess[i] == wod[i]:
                print("Correct letter!")
                #correct_letters = {i: guess[i]}
                correct_letters = {guess[i]: i}
                print(correct_letters)
            elif guess[i] in wod:
                print("Semi Correct letter!")
                if guess[i] not in semi_correct_letters:
                    semi_correct_letters.append(guess[i])
                print(semi_correct_letters)
            else:
                print("Incorrect letter!")
                if guess[i] not in incorrect_letters:
                    incorrect_letters.append(guess[i])
                print(incorrect_letters)

    #Trim word bank
    word_bank_copy = word_bank
    for word in word_bank_copy:
        for letter in correct_letters.keys():
            print("Correct letter loop... " + letter)
            print(letter)
            print(correct_letters[letter])
            if letter != word[correct_letters[letter]]:
                print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            else:
                print("Keeping " + word)
    word_bank_copy = word_bank
    for word in word_bank_copy:
        for letter in semi_correct_letters:
            print("Semi correct letter loop... " + letter)
            if letter not in word:
                print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            else:
                print("Keeping " + word)
    word_bank_copy = word_bank
    for word in word_bank_copy:
        for letter in incorrect_letters:
            print("incorrect letter loop... " + letter)
            if letter in word:
                print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            else:
                print("Keeping " + word)

print("Guess is: " + guess + " Word was: " + wod)
