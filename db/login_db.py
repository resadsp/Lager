from flask import Blueprint, render_template, request, redirect, session
from dataclasses import asdict
import messages.error_list as el
import messages.success_list as sl
import db as db 
import sqlite3
import globals.globals as gl
import bcrypt
from dataclasses import dataclass, field
from typing import Optional

def check_passwords(password: str, hash: str) -> bool:
    password = password.encode("utf-8")
    hash = hash.encode("utf-8")
    return bcrypt.checkpw(password, hash)

def login_(username: str, password: str):
    connection = sqlite3.connect("./orders.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM login WHERE username = ?;", (username,))
    result_set = cursor.fetchone()
    if result_set is None:
        cursor.close()
        return False 
    
    user_id = result_set[0]
    cursor.execute("SELECT password FROM login WHERE user_id = ?;", (user_id,))
    
    result_set = cursor.fetchone()
    hashed_password = result_set[0]
    
    if not check_passwords(password, hashed_password):
        cursor.close()
        return False 
    cursor.execute("""SELECT user_id, username, password
                    FROM login
                    WHERE user_id = ?;""", (user_id,))
    
    result_set = cursor.fetchone()
    cursor.close()
    return result_set


