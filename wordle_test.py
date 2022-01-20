import random

#TODO play with feedback from player/wordle itself
wod = 'POINT'

guess = ""
correct=0
incorrect=0

with open ('5_words.txt', 'r') as f:
    word_bank = f.readlines()
    word_bank = [word.strip().upper() for word in word_bank]


wod_bank = word_bank.copy()
#for wod in wod_bank:
for i in range(200):
    correct_letters = {}
    semi_correct_letters = []
    incorrect_letters = []
    print("Word of day: " + wod)
    word_bank = wod_bank.copy()
    print(len(word_bank))
    #print(word_bank)

    for i in range (6):
        #guess = random.choice(word_bank)
        guess_i = random.randint(0, len(word_bank)-1)
        print("Guess i: " + str(guess_i))
        print("Len of word bank: " + str(len(word_bank)))
        guess = word_bank[guess_i]
        print("Guess: " + guess)
        print("Try: " + str(i+1))
        #print(guess)
        #print("Input feedback from wordle..\nA = absent\nC = correct\nP = present")
        #feedback = input().upper()
        #for i in range(5):
        #    if feedback[i] == 'A':
        #        incorrect_letters.append(guess[i])
        #    elif feedback[i] == 'P':
        #        semi_correct_letters.append(guess[i])
        #    else:
        #        correct_letters[guess[i]] = i

        #print("Absent: " + str(incorrect_letters))
        #print("Present: " + str(semi_correct_letters))
        #print("Correct: " + str(correct_letters))
        if guess == wod:
            print("Word guessed")
            correct += 1
            break
        else:
            for i in range(5):
                #print("Guess letter: " + guess[i] + " wod letter: " + wod[i])
                if guess[i] == wod[i]:
                    #print("Correct letter!")
                    #correct_letters = {i: guess[i]}
                    correct_letters = {guess[i]: i}
                    #print(correct_letters)
                elif guess[i] in wod:
                    #print("Semi Correct letter!")
                    if guess[i] not in semi_correct_letters:
                        semi_correct_letters.append(guess[i])
                    #print(semi_correct_letters)
                else:
                    #print("Incorrect letter!")
                    if guess[i] not in incorrect_letters:
                        incorrect_letters.append(guess[i])
                    #print(incorrect_letters)

        #Trim word bank
        word_bank_copy = word_bank.copy()
        for word in word_bank_copy:
            for letter in correct_letters.keys():
                #print("Correct letter loop... " + letter)
                #print(letter)
                #print(correct_letters[letter])
                if letter != word[correct_letters[letter]]:
                    #print("Removing " + word + " due to " + letter)
                    word_bank.remove(word)
                    break
                else:
                    pass
                    #print("Keeping " + word)
        word_bank_copy = word_bank.copy()
        for word in word_bank_copy:
            for letter in semi_correct_letters:
                #print("Semi correct letter loop... " + letter)
                if letter not in word:
                    #print("Removing " + word + " due to " + letter)
                    word_bank.remove(word)
                    break
                else:
                    pass
                    #print("Keeping " + word)
        word_bank_copy = word_bank.copy()
        for word in word_bank_copy:
            for letter in incorrect_letters:
                #print("incorrect letter loop... " + letter)
                if letter in word:
                    #print("Removing " + word + " due to " + letter)
                    word_bank.remove(word)
                    break
                else:
                    pass
                    #print("Keeping " + word)

    if guess != wod:
        print("Word not guessed.")
        incorrect += 1

print("Correct: " + str(correct))
print("Incorrect: " + str(incorrect))
print(str(correct/(correct+incorrect) * 100) + "% accuracy")
