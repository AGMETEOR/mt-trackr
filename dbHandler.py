import psycopg2
from pprint import pprint
import datetime
import os

#to do get the database to use from environment

class DatabaseHandler:
    def __init__(self,db):
        try:
            self.connection = psycopg2.connect("dbname = {} user = 'postgres' host = 'localhost' password = 'allan' port = '5432'".format(db))
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Could not connect to the database")

    def create_table(self,tbl_name):
        create_table_cmd = "CREATE TABLE {}(id serial PRIMARY KEY, username varchar(400), title varchar(400), department varchar(100), detail text, status text, created timestamp)".format(tbl_name)
        self.cursor.execute(create_table_cmd)

    
    def insert_new_record(self, tbl_name, **kwargs):
        col_str = ""
        val_tup = ()
        returnObject = {}
        if kwargs is not None:
            for key,value in kwargs.items():
                col_str = col_str + key + ","
                val_tup = val_tup + (value,)

            col_str = col_str.rstrip(",")

            insert_cmd  = "INSERT INTO {}".format(tbl_name) + "("+ col_str + ")" + "VALUES" + str(val_tup)
            pprint(insert_cmd)
            
            try:
                self.cursor.execute(insert_cmd)
                get_back_cmd = "SELECT * FROM {} ORDER BY created DESC LIMIT 1".format(tbl_name)
                pprint(get_back_cmd)
                self.cursor.execute(get_back_cmd)
                request = self.cursor.fetchone()
                pprint(list(request))
                return list(request)
            except:
                return {"error":"Couldn't Insert into Database"}

    def get_all_records(self,tbl_name):
        self.cursor.execute("SELECT * FROM {} ORDER BY id ASC".format(tbl_name))
        requests = self.cursor.fetchall()
        for request in requests:
            pprint(request)
        return list(requests)
            #return all the records

    def get_single_record(self,column, value, tbl_name):
        self.cursor.execute("SELECT * FROM {} WHERE {} = {}".format(tbl_name,column, value))
        request = self.cursor.fetchone()
        return list(request)


    def update_record(self, id,tbl_name, **kwargs):
        statement = ""
       
        if kwargs is not None:
            for key, value in kwargs.items():
                statement = statement + key + " = '" + value + "',"

            pprint(statement.rstrip(","))
            statement = statement.rstrip(",")

            update_cmd = "UPDATE {} SET ".format(tbl_name) + statement + " WHERE id = {}".format(id)
            pprint(update_cmd)
            try:
                self.cursor.execute(update_cmd)
                get_back_cmd = "SELECT * FROM {} WHERE id = {}".format(tbl_name,id)
                self.cursor.execute(get_back_cmd)
                request = self.cursor.fetchone()
                pprint(list(request))
                return list(request)
            except:
                return {"error":"Couldn't insert into database"}
            
        pprint(update_cmd)

    def delete_record(self, tbl_name, id):
        delete_cmd = "DELETE FROM {} WHERE id={}".format(tbl_name, id)
        pprint(delete_cmd)
        self.cursor.execute(delete_cmd)


class UserDatabaseHandler(DatabaseHandler):


    def create_table(self,tbl_name):
        create_table_cmd = "CREATE TABLE {}(id serial PRIMARY KEY, username varchar(400), password varchar(100), type varchar(20), created timestamp)".format(tbl_name)
        pprint(create_table_cmd)
        self.cursor.execute(create_table_cmd)

    def get_single_record(self,username,tbl_name):
        self.cursor.execute("SELECT * FROM {} WHERE username = '{}'".format(tbl_name, username))
        request = self.cursor.fetchall()
        print(request)

    def delete_record(self,tbl_name, username):

        delete_cmd = "DELETE FROM {} WHERE username='{}'".format(tbl_name,username)
        pprint(delete_cmd)
        self.cursor.execute(delete_cmd)


if __name__ == "__main__":
    db = DatabaseHandler("test_db")
    # userdb = UserDatabaseHandler("test_db")
    db.update_record(125,"requests_db",username = "allan@gmail.com",title = "Elevator Maintenance",department = "Admin Department26668",detail = "This is better detail2")
    # items = db.get_all_records("requests_db")
    # pprint(items)
    # userdb.get_all_records("users_db")
    # userdb.get_single_record("allan@gmail.com","users_db")
    # userdb.delete_record("users_db","allan@gmail.com")
    # _list = list(db.get_single_record("id", "3" ,"requests_db"))
    # pprint(_list)
    # db.delete_record(1)
    # db.create_table("requests_db")
    # userdb.create_table("users_db")

    # _list = db.insert_new_record("requests_db",username = "allan@gmail.com", title = "Elevator Maintenance2",department = "Admin Department2",detail = "This is better detail2",status="pending",created = str(datetime.datetime.utcnow()))
    # pprint(_list[0])
    # userdb.insert_new_record("users_db",username = "allan@gmail.com", password = "Elevator Maintenance2",type="Admin")
    

