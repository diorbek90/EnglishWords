CREATE_TABLE_THEME = """
    CREATE TABLE IF NOT EXISTS theme (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
"""

SELECT_THEME = "SELECT id, name FROM theme"
INSERT_THEME = "INSERT INTO theme (name) VALUES (?)"
UPDATE_THEME = "UPDATE theme SET name = ? WHERE id = ?"
DELETE_THEME = "DELETE FROM theme WHERE id = ?"
GET_THEME_ID = "SELECT id FROM theme WHERE name = ?"
GET_THEME_BY_ID = "SELECT name FROM theme WHERE id = ?"


# words

CREATE_TABLE_WORDS = """
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        translated TEXT NOT NULL,
        theme_id INTEGER,
        FOREIGN KEY (theme_id) REFERENCES theme(id) ON DELETE CASCADE
    )
"""

SELECT_WORD = "SELECT id, word, translated FROM words"
INSERT_WORD = "INSERT INTO words (word, translated) VALUES (?, ?)"
UPDATE_WORD = "UPDATE words SET word = ?, translated = ? WHERE id = ?"
DELETE_WORD = "DELETE FROM words WHERE id = ?"

INSERT_WORD_WITH_THEMEID = "INSERT INTO words (word, translated, theme_id) VALUES (?,?,?)"
SELECT_WORD_BY_THEME = "SELECT words.id, words.word, words.translated FROM words JOIN theme ON words.theme_id = theme.id WHERE theme.id = ?"
SELECT_ID_BY_WORDTHEME = "SELECT id FROM words WHERE word = ? AND theme_id = ?"




SELECT_ONLY_ID_WORD = "SELECT id FROM words WHERE theme_id=?"
GET_EXIST_ID = 'SELECT id FROM theme ORDER BY id' 
SELECT_WORD_BY_ID = "SELECT word, translated FROM words WHERE id=?"


