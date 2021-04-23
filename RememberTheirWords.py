# For GUI
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error

# For random word output
from random import randrange

def create_connection(db_file):
    # create a database connection to a SQLite database
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return connection

def create_table(connection, create_table_sql):
    """ create a table from the `create_table_sql` statement
    :param connection: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_word(connection, word, date):
    if word == '':
        tkinter.messagebox.showinfo(title="Error",message="No word entered")
        return
    if search_words(connection, word) == True:
        tkinter.messagebox.showinfo(title="Error",message="Word already exists in database")
        return
    sql = 'INSERT INTO wordTable(word, wordDate) VALUES(?,?)'
    c = connection.cursor()
    c.execute(sql, [word,date])
    connection.commit()
    return c.lastrowid

def grab_word(connection):
    sql = 'SELECT word FROM wordTable ORDER BY RANDOM() LIMIT 1'
    c = connection.cursor()
    c.execute(sql)
    lines = c.fetchall()
    stringWords = ''
    for line in lines:
        stringWords += str(line[0])
    return stringWords

def list_words(connection):
    sql = 'SELECT word,wordDate FROM wordTable'
    c = connection.cursor()
    c.execute(sql)
    lines = c.fetchall()
    stringWords = ''
    for line in lines:
        stringWords += str(line[0]) + ' (' + str(line[1]) + ')\n'
    return stringWords

def search_words(connection, word):
    sql = 'SELECT word FROM wordTable WHERE word = ?'
    c = connection.cursor()
    c.execute(sql, [word])
    lines = c.fetchall()
    if lines == []:
        return False
    return True

def delete_word(connection, word):
    if search_words(connection, word) == True:
        sql = 'DELETE FROM wordTable WHERE word = ?'
        c = connection.cursor()
        c.execute(sql, [word])
        connection.commit()
        tkinter.messagebox.showinfo(title="Success",message="Word deleted")
    else:
        tkinter.messagebox.showinfo(title="Error",message="Word does not exist")

def export_list(connection):
    sql = 'SELECT word,wordDate FROM wordTable'
    c = connection.cursor()
    c.execute(sql)
    lines = c.fetchall()

    # store list in stringWords
    stringWords = ''
    for line in lines:
        stringWords += str(line[0]) + ' (' + str(line[1]) + ')\n'

    # filename constant
    FILENAME = "list.txt"

    # Open list for append+read, or create if it doesn't exist
    try:
        file = open(FILENAME)
    except IOError:
        print("IO Error")
        exit
    except TypeError:
        print("Type Error")
        exit

    # write stringWords to txt
    open(FILENAME, 'w').write(stringWords)

    # Close list file
    file.close()

    tkinter.messagebox.showinfo(title="Success",message="List exported to list.txt")

def main():

    # Connect/create database
    database = r"database.sqlite3"
    connection = create_connection(database)

    # Define database table
    sql_create_table = """ CREATE TABLE IF NOT EXISTS wordTable (
        id integer PRIMARY KEY, word text NOT NULL, wordDate date
        ) """

    # Create table if it doesn't exist
    if connection is not None:
        create_table(connection, sql_create_table)
    else:
        print("No database connection")

    # Prep GUI
    root = tkinter.Tk()
    root.title("Remember Their Words")

    # GUI Mainframe
    # Create frame widget to hold everything (within the root window); include padding
    mainframe = ttk.Frame(root, padding=(6,6,12,12))
    # Set mainframe up as grid structure
    mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))

    # Set main window root to resize columns and rows
    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 1)

    # Set up various widgets
    # Word entry box
    wordEntryLabel = ttk.Label(mainframe, text = "Enter word here: ")
    wordEntryLabel.grid(column = 1, row = 1, sticky = (E))
    wordEntry = ttk.Entry(mainframe, width = 14)
    wordEntry.grid(column = 2, row = 1, sticky = (W, E))

    # Date entry box
    dateEntryLabel = ttk.Label(mainframe, text = "Enter date (yyyy-mm-dd) here: ")
    dateEntryLabel.grid(column = 1, row = 2, sticky = (E))
    dateEntry = ttk.Entry(mainframe, width = 14)
    dateEntry.grid(column = 2, row = 2, sticky = (W,E))

    # Word entry button
    ttk.Button(mainframe, text="Enter word", command=lambda: [insert_word(connection, wordEntry.get(), dateEntry.get()),wordEntry.delete(0,'end'),dateEntry.delete(0,'end')]).grid(column=3, row=1, rowspan=2, sticky=W, pady = 7, ipady = 10, ipadx = 10)

    # Retrieve random word
    wordRetrieval = ttk.Entry(mainframe, width = 14)
    wordRetrieval.grid(column = 2, row = 3, sticky = (W, E), pady = 7)
    # Word retrieval button
    ttk.Button(mainframe, text="Retrieve random word", command=lambda: [wordRetrieval.delete(0,'end'),wordRetrieval.insert(0, grab_word(connection))]).grid(column=3, row=3, sticky=W)

    # Delete word
    wordDeletion = ttk.Entry(mainframe, width = 14)
    wordDeletion.grid(column = 2, row = 4, sticky = (W, E), pady = 7)
    ttk.Button(mainframe, text="Delete word", command=lambda: [delete_word(connection, wordDeletion.get()),wordDeletion.delete(0,'end')]).grid(column=3, row=4, sticky=W)

    # List all words
    wordList = lambda: tkinter.messagebox.showinfo(title="All Words",message=list_words(connection))
    ttk.Button(mainframe, text="List all words", command=wordList).grid(column=3, row=5, sticky=W, pady = 7)

    # Export list
    ttk.Button(mainframe, text="Export list to txt", command=lambda: export_list(connection)).grid(column=3, row=6, sticky=W)

    # Exit program
    ttk.Button(mainframe, text="Exit", command=root.destroy).grid(column=3, row=7, sticky=W, pady = 7)

    root.mainloop()

main()