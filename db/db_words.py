import sqlite3
from db import queries

def create_table_words():
    con = sqlite3.connect('words.db')
    cursor = con.cursor()

    cursor.execute(queries.CREATE_TABLE_WORDS)

    con.commit()
    con.close()

def insert_word_with_theme_id(word, translated, theme_id):
    con = sqlite3.connect("words.db")
    cursor = con.cursor()

    cursor.execute(queries.INSERT_WORD_WITH_THEMEID, (word, translated, theme_id))

    con.commit()
    con.close()

def get_words_by_theme(id):
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()

    result = cursor.execute(queries.SELECT_WORD_BY_THEME, (id,)).fetchall()

    conn.commit()
    conn.close()
    
    return result

def get_words():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    
    cursor.execute(queries.SELECT_WORD)
    get_words = cursor.fetchall()

    return get_words


'''Card themes'''

def create_table_themes():

    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()

    cursor.execute(queries.CREATE_TABLE_THEME)

    conn.commit()
    conn.close()


def insert_theme(theme):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()

    cursor.execute(queries.INSERT_THEME, (theme,))

    conn.commit()
    conn.close()

def get_theme_id(theme_name):
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()

    id = cursor.execute(queries.GET_THEME_ID, (theme_name,)).fetchone()
    conn.commit()
    conn.close()
    return id

def get_theme_by_id(id):
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()

    theme = cursor.execute(queries.GET_THEME_BY_ID, (id,)).fetchone()
    conn.commit()
    conn.close()
    return theme

def get_theme():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    
    cursor.execute(queries.SELECT_THEME)
    get_themes = cursor.fetchall()

    return get_themes

