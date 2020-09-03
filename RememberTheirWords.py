# For GUI
# import tkinter

# For random word output
from random import randrange

def main():
    # Prep list file
    fileName = 'list.txt'
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
    # toplevel = tkinter.Tk()

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