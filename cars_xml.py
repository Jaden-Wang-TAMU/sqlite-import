import sqlite3
import xml.etree.ElementTree as ET

con = sqlite3.connect("data.sqlite")
cur = con.cursor()

object="cars"

tree = ET.parse(object+'.xml')
root = tree.getroot()

# for elem in tree.iter():
#   print(elem.text)
tags=[]
for child in root.iter():
  if (tags.__contains__(child.tag)==False):
    tags.append(child.tag)
tags.pop(0)
tags.pop(0)

command=""
columns=""
num_of_values=len(tags)
categories=[]

for key in tags:
  command+=key+" TEXT NOT NULL, "
  columns+=key+", "
  categories.append(key)

command=command[0:len(command)-2]
columns=columns[0:len(columns)-2]

full_command='''CREATE TABLE IF NOT EXISTS '''+object+'''('''+command+''');'''
cur.execute(full_command)

question_marks=""
for x in range(num_of_values):
    question_marks+="?, "
question_marks=question_marks[0:len(question_marks)-2]
insert_records="INSERT INTO "+object+" VALUES("+question_marks+")"

final_values=[]
value_list=[]
counter=0

for child in root.iter():
  if(child.tag!='record' and child.text!='\n'):
    value_list.append(child.text)
    counter=counter+1
    if(counter==num_of_values):
      final_values.append(value_list)
      # print(value_list)
      value_list=[]
      counter=0

# print(final_values)

# print(value_list) All different values


cur.executemany(insert_records, final_values)

cur.execute("SELECT * FROM "+object)
cur.fetchall()

con.commit()
con.close()
