import random
import requests
import json

TOTAL_WORDS = 166432

def main():
    global hints, mis, guessed, word, res, coins, stpdwd, secret, game, message, mean
    while True:
        resetVars()
        coins = 0
        message = "Welcome to Hangman!"
        while mis < 5 or game:
            renderMan()
            if game == True:
                 handleGuess()
        handleEnd()

def resetVars():
    global hints, mis, guessed, word, res, coins, stpdwd, secret, game, message, mean
    hints = 0
    mis = 0
    guessed = []
    roll()
    stripWord()
    updateSecret()
    game = True

# Picks a (new) random word from freeDictionaryAPI (https://github.com/meetDeveloper/freeDictionaryAPI)
def roll():
    global word, res, mean
    while True:
        try: 
            # Gets Random Word out of list in file
            word  = random.choice(open('dictionary.txt', encoding='utf-8').readlines()).strip().lower()            # Dictionary definition as JSON object
            res = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}').json()
            mean = res[0]["meanings"]
            break
        except:
            pass

# Prints each definition the player has unlocked

def renderMan():
    global mis, coins, hints, mean, message, word, secret
    print("\n=======================================================================\n")
    print(f"{('❤️' * (5 - mis) + ('❌' * mis))}  -  Coins: {coins}  -  Hints: {hints} / {len(mean)}")
    # format secret string
    scrt = ""
    for i in secret:
        scrt += i + " "
    message = message.upper()
    print(str(guessed).replace("'", "").upper() + "\n")
    # the man, the message and the secret
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
    printHints()

def handleGuess():
    global message, secret, mis, guessed, hints, coins
    while True:
        try:
            print("\nPlease, enter a letter, [1] to get a hint or [0] to quit")
            guess = input("\n> Guess a letter: ").lower()
        except:
            print("Error. Goodbye!")
            exit()
        if len(guess) == 1:
            if guess.isalpha():
                if guess in guessed:
                    message = "You already guessed that letter"
                elif guess in word:
                    guessed.append(guess)
                    message = "Good guess"
                    updateSecret()
                else:
                    mis += 1
                    message = "Try Again..."
                    guessed.append(guess)
                break
            elif guess == "1":
                coins -= 1
                newHint()
                break
            elif guess == "0":
                exit()
        else:
            continue
    autoHints()
    if hints > 0:
        printHints()

def updateSecret():
    global secret, word, guessed
    secret = ""
    # has game just begun
    if len(guessed) == 0:
        secret = "?" * len(word) 
    # reveal correctly guessed letters
    else: 
        for i in range(0, len(word)):
            if word[i] not in guessed:
                secret += "?"
            else:
                secret += word[i]
    # has word been guessed
        if secret == word:
            handleEnd()

def stripWord():
    global word, stpdwd
    if word[-3:] == 'ing' or word[-3:] == 'ies':
        stpdwd = word[:-3]
    elif word[-2:] == 'ed':
        stpdwd = word[:-2]
    elif word [-1] == 's':
        stpdwd = word[:-1]
    else:
        stpdwd = word

def printHints():
    global word, mean, hints
    # strip word

    for i in range(hints):
        print(mean[i]["partOfSpeech"], ":")
        print("\t" + mean[i]["definitions"][0]["definition"].lower().replace(word, "*" * len(word)).replace(stpdwd, "*" * len(stpdwd)).capitalize())
        try:
            print('\t"' + mean[i]["definitions"][0]["example"].lower().replace(word, "*" * len(word)).replace(stpdwd, "*" * len(stpdwd)).capitalize() + '" \n')
        except:
            pass

def newHint():
    global hints, mean, message
    if hints == len(mean):
        message = "\t No more available hints!"
    else:
        hints += 1
    
def autoHints():
    global hints, game, mean, mis
    if mis == 2 and hints < 1:
        hints = 1
    if mis == 4 and hints < 2 and len(mean) > 1:
        hints = 2
    if mis == 5:
        game = False

def handleEnd():
    global secret, word, mis, hints, coins

    while True:
        if secret == word:
            print("\n YOU WIN!")
            coins += 5 - mis
        keepPlaying = input("\n\t > > Play Again? (y/n) ").lower()
        if keepPlaying in ['n', 'no', 'not', 'nao', 'não', 'ñ', '0']:
            quit()
        else:
            break
    resetVars()

def quit():
    print("See you later!")
    exit()

if __name__ == "__main__":
    main()
