import sqlite3
import csv
import json
import xml.etree.ElementTree as ET

class Import:
    
    def import_all(self, filename):
        type=filename.split('.')
        if type[1]=='csv':
            Import.import_csv(self, filename)
        elif type[1]=='json':
            Import.import_json(self, filename)
        elif type[1]=='.xml':
            Import.import_xml(self, filename)


    def import_csv(self, filename):
        con = sqlite3.connect("data.sqlite")
        cur = con.cursor()

        object=filename[0:len(filename)-4]

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
                columns+=row1[x]+", "
                command+=row1[x]+" TEXT NOT NULL, "
        command=command[0:len(command)-2]
        columns=columns[0:len(columns)-2]
        print(columns)

        full_command='''CREATE TABLE IF NOT EXISTS '''+object+'''('''+command+''');'''
        cur.execute(full_command)

        question_marks=""
        for x in range(num_of_values):
            question_marks+="?, "
        question_marks=question_marks[0:len(question_marks)-2]
        insert_records="INSERT INTO "+object+" VALUES("+question_marks+")"
        cur.executemany(insert_records, rows)

        cur.execute("SELECT * FROM "+object)
        cur.fetchall()

        con.commit()
        con.close()

    def import_json(self, filename):
        con = sqlite3.connect("data.sqlite")
        cur = con.cursor()

        object=filename[0:len(filename)-4]

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

    def import_xml(self, filename):     
        con = sqlite3.connect("data3.sqlite")
        cur = con.cursor()

        object="books"

        tree = ET.parse(object+'.xml')
        root = tree.getroot()

        tags=[]
        for child in root.iter():
            if (tags.__contains__(child.tag)==False):
                tags.append(child.tag)
        tags.pop(0)
        tags.pop(0)
        print(tags)

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

        print(command)
        print(columns)

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
                    value_list=[]
                    counter=0


        cur.executemany(insert_records, final_values)

        cur.execute("SELECT * FROM "+object)
        cur.fetchall()

        con.commit()
        con.close()


