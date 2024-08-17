from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
import sqlite3

def save_carpet(
              kolekcija: str, 
              sifra: str, 
              D80x150: int, 
              D80x300: int, 
              D120x200: int, 
              D160x230: int, 
              D200x300: int,
              slika1: str,
              kvadratura: float,
              D120x120: int,
              D160x160: int,
              D200x200: int
              ):
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO stanje VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(kolekcija, sifra, D80x150, D80x300, D120x200, D160x230, D200x300, slika1, kvadratura, D120x120, D160x160, D200x200))
    connection.commit()
    cursor.close()
    if cursor.execute:
        return True
    
def save(kolekcija: str, 
              sifra: str, 
              D80x150: int, 
              D80x300: int,
              D120x200: int,
              D160x230: int,
              D200x300: int,
              kvadratura: float,
              D120x120: int,
              D160x160: int,
              D200x200: int
              ) -> bool:
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE stanje SET kolekcija=?, d80x150=?, d80x300=?, d120x200=?, d160x230=?, d200x300=?, kvadratura=?, d120x120=?, d160x160=?, d200x200=?  WHERE sifra=?;",(kolekcija,D80x150,D80x300,D120x200,D160x230,D200x300, kvadratura, D120x120, D160x160, D200x200, sifra))
    connection.commit()
    cursor.close()
    if cursor.execute is None:
        return False 
    else:
        return True 
    
def find_in_stock():
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stanje ORDER BY kolekcija ASC, sifra ASC;")
    result_set = cursor.fetchall()
    cursor.close()
    if result_set is None:
        return []
    return list(result_set)

    
def find_in_stock_pass(sifra: str):
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stanje WHERE sifra = ?;", (sifra,))
    result_set = cursor.fetchone()
    cursor.close()
    if result_set is None:
        return []
    return list(result_set)

def saldo_metres():
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stanje;")
    result_set = cursor.fetchall()
    cursor.close()
    if result_set is None:
        return []
    return list(result_set)

def save_saldo(
              datum: str, 
              pazar: float
              ):
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO avgust VALUES (?,?)",(datum, pazar))
    connection.commit()
    cursor.close()
    if cursor.execute:
        return True
    
def find_saldo():
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM avgust;")
    result_set = cursor.fetchall()
    cursor.close()
    if result_set is None:
        return []
    return list(result_set)
    
