import sqlite3

connector = sqlite3.connect('food_diary_database.db')
cursor = connector.cursor()
cursor.execute("""CREATE TABLE foods
                  (date text, description text)""")
cursor.execute("""CREATE TABLE supplements
                  (date text, description text)""")
cursor.execute("""CREATE TABLE depositions
                  (date text, bristol_level real)""")
cursor.execute("""CREATE TABLE symptoms
                  (date text, description text)""")
cursor.execute("""CREATE TABLE comments
                  (date text, description text)""")