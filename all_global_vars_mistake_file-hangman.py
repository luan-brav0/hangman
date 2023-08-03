import random
import requests
import json

total_words = 166432

def main():
    hints, mis, guessed, word, res, coins, stpdwd, secret, game, message, mean = resetVars ()
    while True:
        reset()
        message = "Welcome to Hangman!"

        while mis < 5 or game:
            renderMan()
            if game == True:
                handleGuess()
        handleEnd()

def resetVars():
    hints = 0
    mis = 0
    guessed = []
    roll()
    coins = 0
    stripWord()
    secret = updateSecret()
    game = True
    return hints, mis, guessed, word, res, coins, stpdwd, secret, game, message, mean


def quit():
    print("See you later!")
    exit()

def handleEnd():
    while True:
        renderMan()
        keepPlaying = input("\n> Play Again? (y/n) ").lower()
        if keepPlaying != "n" or keepPlaying != "no":
            quit()
        else:
            game = True
            return
    autoHints()
    if hints > 0:
        printHints()

def renderMan(mis, secret, message, word, hints):
    #{min}m{sec}s   - {coins} Moedas")
    # Man
    scrt = ""
    for i in secret:
        scrt += i + " "
    message = message.upper()
    print("\n"+str(guessed).replace("'", "").upper())
    if mis == 0:
        print("     ______|")
    else:
        print("     _______")
    if mis >= 1:
        print("    |       |")
    else:
        print("    |       ")
    if mis == 5:
        print(f"    |       X    YOU LOSE // {word.upper()}")
    elif mis == 4:
        print(f"    |      !O!   LAST CHANCE // {message}")
    elif mis >= 2 and mis < 4:
        print(f"    |       O    {message}")
    else:
        print(f"    |            {message}")
    if mis >= 3:
        print("    |      /|\\")
    else:
        print("    |")
    if mis >= 4:
        print("    |      / \\")
    else:
        print("    |")
    # Secret and base
    print(f"____|_    {(scrt).upper()}")

def handleGuess(guessed, message, mis, secret, word):
    while True:
        try:
            print("\nPlease, enter a letter, [1] to get a hint or [0] to quit")
            guess = input("\n> Guess a letter: ").lower()
        except:
            print("Error. Goodbye!")
            exit()
            break
        #guess = guess.lower()
        if guess.isalpha():
            if guess in guessed:
                message = "You already guessed that letter"
            elif guess in word:
                guessed.append(guess)
                message = "Good guess"
                secret = updateSecret()
            else:
                mis += 1
                message = "Try Again..."
                guessed.append(guess)
            break

        elif guess == "1":
            newHint()
            break
        elif guess == "0":
            exit()
            return
        else:
            continue

def stripWord(word, stpdwd):
    if word[-3:] == 'ing' or word[-3:] == 'ies':
        stpdwd = word[:-3]
    elif word[-2:] == 'ed':
        stpdwd = word[:-2]
    elif word [-1] == 's':
        stpdwd = word[:-1]
    else:
        stpdwd = word

def updateSecret(guessed, game):
    secret = ""

    # has game just begun
    if len(guessed) == 0:
        secret = "? " * len(word) 
        return secret

    # reveal correctly guessed letters
    for i in range(0, len(word)):
        if word[i] not in guessed:
            secret += "?"
        else:
            secret += word[i]

    # has word been guessed
    if secret != word:
        return secret
    else:
        print("\n\tYOU WIN")
        game = False
        return secret

# Picks a (new) random word from freeDictionaryAPI (https://github.com/meetDeveloper/freeDictionaryAPI)
def roll(word, res, mean):
    while True:
        try: 
            # Gets Random Word out of list in file
            word  = random.choice(open('dictionary.txt', encoding='utf-8').readlines()).strip().lower()
            # Dictionary definition as JSON object
            res = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}').json()
            mean = res[0]["meanings"]
            break
        except:
            pass

#print(res, "\n", type(res), len(res))
#print(r, "\n", type(r), len(r))

# Print each word definition with example
#print(word) 

# Clean striped word for censoring the definitions
#print(stpdwd)

def printHints(hints, mean, stpdwd, word):
    # Prints each definition the player has unlocked
    for i in range(hints):
        print(mean[i]["partOfSpeech"], ":")
        print("\t" + mean[i]["definitions"][0]["definition"].lower().replace(word, "*" * len(word)).replace(stpdwd, "*" * len(stpdwd)).capitalize())
        try:
            print('\t"' + mean[i]["definitions"][0]["example"].lower().replace(word, "*" * len(word)).replace(stpdwd, "*" * len(stpdwd)).capitalize() + '" \n')
        except:
            pass

def newHint(hints, mean, message):
    if hints == len(mean):
        message = "\t No more available hints!"
        return
    else:
        hints += 1
    renderMan()

def autoHints(hints, mis, mean, game):
    if mis == 2 and hints < 1:
        hints = 1
    if mis == 4 and hints < 2 and len(mean) > 1:
        hints = 2
    if mis == 5:
        game = False

if __name__ == "__main__":
    main()
