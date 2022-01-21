import random

#TODO play with feedback from player/wordle itself
#wod = 'SHIRE'

correct_letters = {}
semi_correct_letters = {}
incorrect_letters = []
guess = ""

with open ('5_words.txt', 'r') as f:
    word_bank = f.readlines()
    word_bank = [word.strip().upper() for word in word_bank]

for i in range (99):

    print("Words remaining in word bank:" + str(len(word_bank)))
    guess = random.choice(word_bank)
    print("Try: " + str(i+1))
    print(guess)
    print("Input feedback from wordle..\nA = absent(Gray)\nC = correct(Green)\nP = present(Yellow)")
    feedback = input().upper()
    for i in range(5):
        if feedback[i] == 'A':
            incorrect_letters.append(guess[i])
        elif feedback[i] == 'P':
            semi_correct_letters[guess[i]] = i
        else:
            correct_letters[guess[i]] = i

    print("Absent: " + str(incorrect_letters))
    print("Present: " + str(semi_correct_letters))
    print("Correct: " + str(correct_letters))

    #Trim word bank
    word_bank_copy = word_bank.copy()
    #Correct letter pruning
    for word in word_bank_copy:
        for letter in correct_letters.keys():
            print("Correct letter loop... " + letter)
            #print(letter)
            #print(correct_letters[letter])
            if letter != word[correct_letters[letter]]:
                print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            else:
                print("Keeping " + word)
    #Semicorrect letter pruning
    word_bank_copy = word_bank.copy()
    for word in word_bank_copy:
        for letter in semi_correct_letters.keys():
            print("Semi correct letter loop... " + letter)
            if letter not in word:
                print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            if letter == word[semi_correct_letters[letter]]:
                print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            else:
                print("Keeping " + word)
    #incorrect letter pruning
    word_bank_copy = word_bank.copy()
    for word in word_bank_copy:
        for letter in incorrect_letters:
            print("incorrect letter loop... " + letter)
            if letter in word and letter not in semi_correct_letters and letter not in correct_letters:
                print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            else:
                print("Keeping " + word)
