import os
import sqlite3
import pandas as pd
  
# create database connection
connection = sqlite3.connect("quiz.db")
# create cursor
cursor = connection.cursor()
# execute SQL query
cursor.execute("""
  CREATE TABLE IF NOT EXISTS "Test" (
    "QuestionID"		INTEGER NOT NULL,
    "Question"	    TEXT NOT NULL,
    "ChoiceA"		    TEXT NOT NULL,
    "ChoiceB"		    TEXT NOT NULL,
    "ChoiceC"		    TEXT NOT NULL,      
    "ChoiceD"		    TEXT NOT NULL,
    "CChoice"		    TEXT NOT NULL,
    PRIMARY KEY("QuestionID")
  );
""")
cursor.execute("""
  CREATE TABLE IF NOT EXISTS "User" (
    "UserID"		INTEGER NOT NULL,
    "Name"	    TEXT NOT NULL,
    "ClassID"		TEXT NOT NULL,
    PRIMARY KEY("UserID")
  );
""")
# Insert DataFrame to Tables
Test = pd.read_csv(r'\uploads\Test.csv')  
dft = pd.DataFrame(data=Test, columns= ['QuestionID','Question','ChoiceA','ChoiceB','ChoiceC','ChoiceD',"CChoice"])
for row in dft.itertuples():
  intot = "INSERT INTO Test VALUES (?,?,?,?,?,?,?)"
  valt = (row.QuestionID,row.Question,row.ChoiceA,row.ChoiceB,row.ChoiceC,row.ChoiceD,row.CChoice)
  cursor.execute(intot, valt)
# make changes permanent
connection.commit()