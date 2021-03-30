# For GUI
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# For random word output
from random import randrange

# filename constant
FILENAME = "list.txt"


def inputWord(word):
    # Word input

    print("Word: " + word)

    # TODO:
    #   Add to database. Sqlite?
    #   Check word against database
    #   Timestamp of entry?

    # See if input word already exists in list
    wordExists = False
    for line in open(FILENAME):
        if word in line:
            wordExists = True
            print("Word already exists")
            break

    # If input word doesn't exist yet, add it to list
    if wordExists == False:
        open(FILENAME, 'a+').write(str(word) + '\n')
        print("Word added")

def grabWord():
    # Count lines in order to randomize
    count = 0
    for line in open(FILENAME):
        count += 1

    # If empty
    if count is 0:
        return "[list is empty]"

    # Select a random number based on # of lines
    randomLine = randrange(count)

    # Return the line based on that random number
    return(open(FILENAME).readlines()[randomLine])

    # TODO: Prevent repeats of words; iterate through list in a random/shuffle way

def listAllWords():
    str1 = ""
    for line in open(FILENAME):
        str1 += line
    return str1

def main():
    # Prep list file
    fileName = FILENAME
    # Open list for append+read, or create if it doesn't exist
    try:
        file = open(fileName, 'a+')
    except IOError:
        print("IO Error")
        exit
    except TypeError:
        print("Type Error")
        exit

    # Prep GUI
    root = tkinter.Tk()
    root.title("Remember Their Words")

    # GUI Mainframe
    # Create frame widget to hold everything (within the root window); include padding
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    # Set mainframe up as grid structure
    mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))

    # Set main window root to resize columns and rows
    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 1)

    # Set up various widgets
    # Word entry box
    wordEntry = ttk.Entry(mainframe, width = 14)
    wordEntry.grid(column = 2, row = 1, sticky= (W, E))
    # Word entry button
    ttk.Button(mainframe, text="Enter word", command=lambda: inputWord(wordEntry.get())).grid(column=3, row=1, sticky=W)

    # Retrieve random word
    wordRetrieval = ttk.Entry(mainframe, width = 14)
    wordRetrieval.grid(column = 2, row = 2, sticky = (W, E))
    # Word retrieval button
    ttk.Button(mainframe, text="Retrieve random word", command=lambda: [wordRetrieval.delete(0,'end'),wordRetrieval.insert(0, grabWord())]).grid(column=3, row=2, sticky=W)

    # List all words
    wordList = lambda: tkinter.messagebox.showinfo(title="All Words",message=listAllWords())
    ttk.Button(mainframe, text="List all words", command=wordList).grid(column=3, row=3, sticky=W)

    # Exit flag for while loop
    exitLoop = 0

    while exitLoop == 0:
        # Start Menu
        print("Press 1 to enter a word, 2 to print a random word, 3 to print all words, or 4 to quit: ")
        choice = input()

        if choice == '1':
            
            # Word input

            # TODO:
            #   Add to database. Sqlite?
            #   Check word against database
            #   Timestamp of entry?

            print("Enter a word to remember: ")
            word = input()

            # See if input word already exists in list
            wordExists = False
            for line in open(fileName):
                if word in line:
                    wordExists = True
                    print("Word already exists")
                    break

            # If input word doesn't exist yet, add it to list
            if wordExists == False:
                file.write(word + '\n')
                print("Word added")

        if choice == '2':
            # Count lines in order to randomize
            count = 0
            for line in open(fileName):
                count += 1

            # Select a random number based on # of lines
            randomLine = randrange(count)

            # Print the line based on that random number
            print(open(fileName).readlines()[randomLine])

            # TODO: Prevent repeats of words; iterate through list in a random/shuffle way

        if choice == '3':
            print(open(fileName).read())

        if choice == '4':
            exitLoop = 1
        

    # Close list file
    file.close()

main()