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

def insert_word(connection, word):
    if word == '':
        tkinter.messagebox.showinfo(title="Error",message="No word entered")
        return
    if search_words(connection, word) == True:
        tkinter.messagebox.showinfo(title="Error",message="Word already exists in database")
        return
    sql = 'INSERT INTO wordTable(word) VALUES(?)'
    c = connection.cursor()
    c.execute(sql, [word])
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
    c = connection.cursor()
    c.execute('SELECT word FROM wordTable')
    lines = c.fetchall()
    stringWords = ''
    for line in lines:
        stringWords += str(line[0]) + '\n'
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

def main():

    # Connect/create database
    database = r"database.sqlite3"
    connection = create_connection(database)

    # Define database table
    sql_create_table = """ CREATE TABLE IF NOT EXISTS wordTable (
        id integer PRIMARY KEY, word text NOT NULL
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
    ttk.Button(mainframe, text="Enter word", command=lambda: [insert_word(connection, wordEntry.get()),wordEntry.delete(0,'end')]).grid(column=3, row=1, sticky=W)

    # Retrieve random word
    wordRetrieval = ttk.Entry(mainframe, width = 14)
    wordRetrieval.grid(column = 2, row = 2, sticky = (W, E))
    # Word retrieval button
    ttk.Button(mainframe, text="Retrieve random word", command=lambda: [wordRetrieval.delete(0,'end'),wordRetrieval.insert(0, grab_word(connection))]).grid(column=3, row=2, sticky=W)

    # List all words
    wordList = lambda: tkinter.messagebox.showinfo(title="All Words",message=list_words(connection))
    ttk.Button(mainframe, text="List all words", command=wordList).grid(column=3, row=3, sticky=W)

    # Delete word
    wordDeletion = ttk.Entry(mainframe, width = 14)
    wordDeletion.grid(column = 2, row = 4, sticky = (W, E))
    ttk.Button(mainframe, text="Delete word", command=lambda: [delete_word(connection, wordDeletion.get()),wordDeletion.delete(0,'end')]).grid(column=3, row=4, sticky=W)

    # Exit program
    ttk.Button(mainframe, text="Exit", command=root.destroy).grid(column=3, row=5, sticky=W)

    root.mainloop()

main()