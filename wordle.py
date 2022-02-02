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
#Exit wordle help screen
actions.move_by_offset(10,10).click().perform()


correct_letters = {}
semi_correct_letters = {}
incorrect_letters = []
guess = ""


#Use provided word bank
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

    #Choose a random remaining word from word bank
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

    #Need this to access shadow DOM
    shadow = pyshadow.main.Shadow(driver)


    #Calculate feedback from wordle
    num_correct_letters = 0
    for j in range(5):
        wordle_letter = shadow.find_element('#board > game-row:nth-child('+str(i+1)+') > game-tile:nth-child('+str(j+1)+')')

        feedback = wordle_letter.get_attribute('evaluation')

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


    #Prune word bank
    word_bank_copy = word_bank.copy()
    #Correct letter pruning
    for word in word_bank_copy:
        for letter in correct_letters.keys():
            if letter != word[correct_letters[letter]]:
                word_bank.remove(word)
                break
            else:
                pass

    #Semicorrect letter pruning
    word_bank_copy = word_bank.copy()
    for word in word_bank_copy:
        for letter in semi_correct_letters.keys():
            if letter not in word:
                word_bank.remove(word)
                break
            if letter == word[semi_correct_letters[letter]]:
                word_bank.remove(word)
                break
            else:
                pass

    #incorrect letter pruning
    word_bank_copy = word_bank.copy()
    for word in word_bank_copy:
        for letter in incorrect_letters:
            if letter in word and letter not in semi_correct_letters and letter not in correct_letters:
                word_bank.remove(word)
                break
            else:
                pass

    time.sleep(2)
