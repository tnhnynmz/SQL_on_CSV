# -*- coding: utf-8 -*-

"""
@author: TY
TUNAHAN YANMAZ 2018510105
"""

import csv
import re
import operator
import json

#OPEN CSV FILE AND READ WITH ',' DELIMITER
with open('students.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    a=list(csv_reader)
#CREATE A LIST OF DICTIONARY SORT FOR 'id'
    for row in a:
        row["id"]=int(row["id"])
        row["grade"]=int(row["grade"])
    records = sorted(a, key = lambda d: d['id'])
#ASSIGN POSSIBLE OPERATORS FOR READABILITY 
ops = {
    "=" : operator.eq,
    "!=" : operator.ne,
    "<" : operator.lt,
    ">" : operator.gt,
    "<=" : operator.le,
    ">=": operator.ge,
    "!<" : operator.ge,
    "!>" : operator.le    
}

query_records = records

#RUN PROGRAM UNTIL USER ENTERS 'exit'
select_cols = []
while True:
    sql_command = input()
    if (sql_command == "exit"):
        break
    decider_string = sql_command.split()
    #IF QUERY STARTS WITH 'SELECT' THEN DO SELECT OPERATIONS AND WRITE TO JSON FILE
    if (decider_string[0] == 'SELECT'):
        
        query_records_1 = list()
        sql_command= re.split(' |SELECT|FROM|WHERE|ORDER BY',sql_command)
        while("" in sql_command) :
            sql_command.remove("")
        select_cols = re.split(',', sql_command[0])        
        table_name = sql_command[1]
        where_col_1 = sql_command[2]
        where_op_1 = sql_command[3]
        where_op_2 = ""
        where_andor = ""
        #CHECK IF CONDITION CONTAINS A NUMERIC VALUE
        if (sql_command[4].isnumeric()):
            where_col_2 = int(sql_command[4])
        else:
            where_col_2 = re.findall(r"\'(.*?)\'", sql_command[4])
            where_col_2 = where_col_2.pop()
        #CHECK IF THERE ARE MORE THAN ONE CONDITION AFTER 'WHERE'            
        if (sql_command[5] == 'AND' or sql_command[5] == 'OR'):
            where_andor = sql_command[5]
            where_col_3 = sql_command[6]
            where_op_2 = sql_command[7]
            if (sql_command[8].isnumeric()):
                where_col_4 = int(sql_command[8])
            else:
                where_col_4 = re.findall(r"\'(.*?)\'", sql_command[8])
                where_col_4 = where_col_4.pop()
            order_by = sql_command[9]

        else:
            order_by = sql_command[5]            

        op_func_1 = ops[where_op_1]
        if (where_op_2 != ""):
            op_func_2 = ops[where_op_2]
        
        #IF THERE IS ONLY ONE CONDITION AFTER WHERE       
        if (where_andor == ""):
            for record in query_records:
                if (op_func_1(record.get(where_col_1), where_col_2)):
                    query_records_1.append(record)
        #IF THERE ARE MORE THAN ONE CONDITIONS AFTER WHERE  
        if(where_andor == 'AND'):
            for record in query_records:
                if (op_func_1(record.get(where_col_1), where_col_2) and op_func_2(record.get(where_col_3), where_col_4)):
                    query_records_1.append(record)
        if(where_andor == 'OR'):
            for record in query_records:
                if (op_func_1(record.get(where_col_1), where_col_2) or op_func_2(record.get(where_col_3), where_col_4)):
                    query_records_1.append(record)
                    
        #ORDER FOR ASC OR DSC
        if(order_by == "ASC"):
            query_records_1 = sorted(query_records_1, key = lambda d: d['id'])
        elif(order_by == "DSC"):
            query_records_1 = sorted(query_records_1, key = lambda d: d['id'], reverse = True)
        query_records = query_records_1
            
        
                

    #IF QUERY STARTS WITH 'INSERT'
    if (decider_string[0] == 'INSERT'):
        sql_command= re.split(' |INSERT INTO|VALUES',sql_command)
        while("" in sql_command) :
            sql_command.remove("")
        
        values_not_seperated = sql_command[1][sql_command[1].find('(')+1:sql_command[1].find(')')]
        values = re.split(',', values_not_seperated)
        
        valid_flag = True
        #PROGRAM CHECKS IF ENTERED 'id' HAS ALREADY TAKEN, IF SO GIVES ERROR MESSAGE (PROGRAM ONLY CHECKS SAME IDs NOT OTHER VARIABLES)
        for record in query_records:
            if (record.get('id') == int(values[0])):
                print ("Id has already taken.")
                valid_flag = False
                break
        #IF 'id' IS NOT TAKEN THEN INSERT RECORD TO LIST
        if (valid_flag):
            record_to_insert = {'id' : int(values[0]),'name' : values[1],'lastname' : values[2],'email' : values[3],'grade' : int(values[4])}
            query_records.append(record_to_insert)

    if (decider_string[0] == 'DELETE'):
        sql_command= re.split(' |DELETE|FROM|WHERE',sql_command)
        while("" in sql_command) :
            sql_command.remove("")
        table_name = sql_command[0]
        where_col_1 = sql_command[1]
        where_op_1 = sql_command[2]
        where_op_2 = ""
        where_andor = ""
        if (sql_command[3].isnumeric()):
            where_col_2 = int(sql_command[3])
        else:
            where_col_2 = re.findall(r"\'(.*?)\'", sql_command[3])
            where_col_2 = where_col_2.pop()
            
        if (len(sql_command) > 5 and (sql_command[4] == 'AND' or sql_command[4] == 'OR')):
            where_andor = sql_command[4]
            where_col_3 = sql_command[5]
            where_op_2 = sql_command[6]
            if (sql_command[7].isnumeric()):
                where_col_4 = int(sql_command[7])
            else:
                where_col_4 = re.findall(r"\'(.*?)\'", sql_command[7])
                where_col_4 = where_col_4.pop()

        op_func_1 = ops[where_op_1]
        if (where_op_2 != ""):
            op_func_2 = ops[where_op_2]
        
        if(where_andor == 'AND'):
            query_records = [item for item in query_records if not(op_func_1(item.get(where_col_1), where_col_2) and op_func_2(item.get(where_col_3), where_col_4))]
            
        elif(where_andor == 'OR'):
            query_records = [item for item in query_records if not (op_func_1(item.get(where_col_1), where_col_2) or op_func_2(item.get(where_col_3), where_col_4))]
        else:
            query_records = [item for item in query_records if not op_func_1(item.get(where_col_1), where_col_2)]




#WRITE TO JSON FILE OPERATIONS
with open('json_data.json', 'w') as outfile:
    for record in query_records:
        #IF SELECT CONTAINS ONE KEY (SELECT name eg.)
        if len(select_cols)==1 and select_cols[0] != 'ALL':
            data = {
                select_cols[0] : record[select_cols[0]]
                }
            json.dump(data, outfile)
            outfile.write("\n")
        #IF SELECT CONTAINS MORE THAN ONE KEY (SELECT name,lastname eg.)
        elif len(select_cols) == 2 :
            data = {
                select_cols[0] : record[select_cols[0]],
                select_cols[1] : record[select_cols[1]]
                }
            json.dump(data, outfile)
            outfile.write("\n")
        #IF SELECT CONTAINS 'ALL'
        else:
            json.dump(record, outfile)  
            outfile.write("\n")







