from dataclasses import dataclass, field
from typing import Optional
import sqlite3

  
def get_carpets_for_display():
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM stanje ORDER BY kolekcija ASC;""")
    result_set = cursor.fetchall()
    cursor.close()
    carpets = list(result_set)
    return carpets
