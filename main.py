from flask import Flask, render_template, request, redirect
import sqlite3
import os
import pandas as pd

# remove existing database to clear data, then re-import data from csv into database
dbFilePath = 'quiz.db'
if os.path.exists(dbFilePath):
    os.remove(dbFilePath)

conn = sqlite3.connect(dbFilePath)

# create the table
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Test (
	QuestionID	INTEGER NOT NULL,
	Question		TEXT NOT NULL,
	ChoiceA	  	TEXT NOT NULL,
	ChoiceB	  	TEXT NOT NULL,
	ChoiceC	    TEXT NOT NULL,
	ChoiceD	    TEXT NOT NULL,
  CChoice	    TEXT NOT NULL,
	PRIMARY KEY(QuestionID)
);""")
# make changes permanent
conn.commit()

# insert csv data to database
testCsvReader = pd.read_csv ('uploads/Test.csv')
testDataFrame = pd.DataFrame(data=testCsvReader, columns= ['QuestionID','Question','ChoiceA','ChoiceB','ChoiceC','ChoiceD','CChoice'])
#print("data in testDataFrame:\n")
#print(testDataFrame)

cursor = conn.cursor()
for row in testDataFrame.itertuples():
    sql = "INSERT INTO Test (QuestionID,Question,ChoiceA,ChoiceB,ChoiceC,ChoiceD,CChoice) VALUES (?,?,?,?,?,?,?)"
    values = (row.QuestionID, row.Question, row.ChoiceA, row.ChoiceB, row.ChoiceC, row.ChoiceD, row.CChoice)
    cursor.execute(sql, values)
conn.commit()

conn.close()


app = Flask(__name__)


@app.route('/')
def Home():
  results = []

  conn = sqlite3.connect(dbFilePath)
  try:
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Test''')
    results = cursor.fetchall()
    conn.commit()
  except:
    conn.rollback()
  finally:
    conn.close()
    return render_template('quiz.html', results=results)

@app.route('/check_result',methods = ['POST'])
def CheckResult():
  conn = sqlite3.connect(dbFilePath)

  score = 0
  amountOfYes = 0
  amountOfQuestion = 0

  try:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Test")
    amountOfQuestion = cursor.fetchall()[0][0]
    print("amount of Question: %d" %amountOfQuestion)

    predicates = []
    for QuestionID in request.form:
      CChoice = request.form[QuestionID]
      predicates.append("(QuestionID=" + QuestionID + " AND CChoice='" + CChoice + "')")
    sql = "SELECT COUNT(*) FROM Test WHERE " + " OR ".join(predicates)
    cursor.execute(sql)

    amountOfYes = cursor.fetchall()[0][0]
    conn.commit()

    print("amount of yes: %d" %amountOfYes)

    score = int(amountOfYes * 100.0 / amountOfQuestion)
    print("score: %d" %score)
  except:
    conn.rollback()
  finally:
    conn.close()
    return render_template("checkResult.html", score=score, amountOfQuestion=amountOfQuestion, amountOfYes=amountOfYes)

app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
  app.run(debug=True)
