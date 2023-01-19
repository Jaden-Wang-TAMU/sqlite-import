import sqlite3
import csv

con = sqlite3.connect("data.sqlite")
cur = con.cursor()

object="books"

a_file = open(object+".csv")
rows = csv.reader(a_file)

command=""
columns=""
num_of_values=0

with open(object+'.csv', newline='') as f:
  reader = csv.reader(f)
  row1 = next(reader) # gets the first line
  num_of_values=len(row1)
  for x in range(num_of_values):
    # print(row1[x])
    columns+=row1[x]+", "
    command+=row1[x]+" TEXT NOT NULL, "

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
cur.executemany(insert_records, rows)

cur.execute("SELECT * FROM "+object)
final_rows = cur.fetchall()

# for r in final_rows:
#     print(r)

con.commit()
con.close()
