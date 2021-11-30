import sqlite3

connector = sqlite3.connect('food_diary_database.db')
cursor = connector.cursor()
cursor.execute("""CREATE TABLE foods
                  (user_id integer, date text, description text)""")
cursor.execute("""CREATE TABLE supplements
                  (user_id integer, date text, description text)""")
cursor.execute("""CREATE TABLE depositions
                  (user_id integer, date text, bristol_level integer)""")
cursor.execute("""CREATE TABLE symptoms
                  (user_id integer, date text, description text)""")
cursor.execute("""CREATE TABLE comments
                  (user_id integer, date text, description text)""")