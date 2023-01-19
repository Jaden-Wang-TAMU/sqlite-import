import sqlite3
import json

con = sqlite3.connect("data.sqlite")
cur = con.cursor()

object="books"

rows = json.load(open(object+".json", 'r', encoding='utf-8'))

command=""
columns=""
num_of_values=len(rows[0])

list = []
for key in rows[0].keys():
  list.append(key)
  command+=key+" TEXT NOT NULL, "
  columns+=key+", "

command=command[0:len(command)-2]
columns=columns[0:len(columns)-2]

# print(command)
# print(columns)

full_command='''CREATE TABLE IF NOT EXISTS '''+object+'''('''+command+''');'''
cur.execute(full_command)

question_marks=""
for x in range(num_of_values):
    question_marks+="?, "
question_marks=question_marks[0:len(question_marks)-2]
insert_records="INSERT INTO "+object+" VALUES("+question_marks+")"

final_values=[]
for x in rows:
  value_list=[]
  for value in x.values():
    value_list.append(value)
  final_values.append(value_list)

cur.executemany(insert_records, final_values)

cur.execute("SELECT * FROM "+object)
cur.fetchall()

con.commit()
con.close()
