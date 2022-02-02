import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from pyshadow.main import Shadow
import pyshadow


#Go to wordle page
driver = webdriver.Firefox()
actions = ActionChains(driver)
driver.get("https://www.powerlanguage.co.uk/wordle/")
time.sleep(2)
#Exit help screen
actions.move_by_offset(10,10).click().perform()


correct_letters = {}
semi_correct_letters = {}
incorrect_letters = []
guess = ""

with open ('5_words.txt', 'r') as f:
    word_bank = f.readlines()
    word_bank = [word.strip().upper() for word in word_bank]


# Six guesses
for i in range (6):

    print("Words remaining in word bank:" + str(len(word_bank)))
    #Uncomment this block to specify a first word of your choosing and comment out the line "guess = random.choice(word_bank)" below
    #if i == 0:
    #    guess = "ARISE"
    #else:
    #    guess = random.choice(word_bank)

    guess = random.choice(word_bank)

    print("Try: " + str(i+1))
    print(guess)

    #Enter guess into wordle
    time.sleep(2)
    for char in guess:
        actions.send_keys(char).perform()
        time.sleep(0.5)

    actions.send_keys(Keys.RETURN).perform()
    time.sleep(2)

    shadow = pyshadow.main.Shadow(driver)

    num_correct_letters = 0


    #Calculate feedback from wordle
    for j in range(5):
        wordle_letter = shadow.find_element('#board > game-row:nth-child('+str(i+1)+') > game-tile:nth-child('+str(j+1)+')')

        #print("Wordle letter: " + str(wordle_letter.text))

        feedback = wordle_letter.get_attribute('evaluation')
        #print("Guess: " + str(guess[j]))
        #print(feedback)

        if feedback == 'absent':
            incorrect_letters.append(guess[j])
        elif feedback == 'present':
            semi_correct_letters[guess[j]] = j
        else:
            num_correct_letters += 1
            correct_letters[guess[j]] = j

    if num_correct_letters == 5:
        print("Word guessed!")
        exit(0)

    #print("Absent: " + str(incorrect_letters))
    #print("Present: " + str(semi_correct_letters))
    #print("Correct: " + str(correct_letters))

    #Trim word bank
    word_bank_copy = word_bank.copy()
    #Correct letter pruning
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
                #print("Keeping " + word)
                pass

    #Semicorrect letter pruning
    word_bank_copy = word_bank.copy()
    for word in word_bank_copy:
        for letter in semi_correct_letters.keys():
            #print("Semi correct letter loop... " + letter)
            if letter not in word:
                #print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            if letter == word[semi_correct_letters[letter]]:
                #print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            else:
                #print("Keeping " + word)
                pass

    #incorrect letter pruning
    word_bank_copy = word_bank.copy()
    for word in word_bank_copy:
        for letter in incorrect_letters:
            #print("incorrect letter loop... " + letter)
            if letter in word and letter not in semi_correct_letters and letter not in correct_letters:
                #print("Removing " + word + " due to " + letter)
                word_bank.remove(word)
                break
            else:
                #print("Keeping " + word)
                pass

    time.sleep(2)
