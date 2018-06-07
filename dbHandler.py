import psycopg2
import datetime
import os


class DatabaseHandler:
    def __init__(self, db):
        try:
            self.connection = psycopg2.connect(
                "dbname = {} user = 'postgres' host = 'localhost' password = 'allan' port = '5432'".format(db))
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            return({"error": "Could not connect to the database"})

    def create_table(self, tbl_name):
        create_table_cmd = "CREATE TABLE {}(id serial PRIMARY KEY, username varchar(400), title varchar(400), department varchar(100), detail text, status text, created timestamp)".format(
            tbl_name)
        self.cursor.execute(create_table_cmd)

    def insert_new_record(self, tbl_name, **kwargs):
        col_str = ""
        val_tup = ()
        returnObject = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                col_str = col_str + key + ","
                val_tup = val_tup + (value,)

            col_str = col_str.rstrip(",")

            insert_cmd = "INSERT INTO {}".format(
                tbl_name) + "(" + col_str + ")" + "VALUES" + str(val_tup)

            try:
                self.cursor.execute(insert_cmd)
                get_back_cmd = "SELECT * FROM {} ORDER BY created DESC LIMIT 1".format(
                    tbl_name)

                self.cursor.execute(get_back_cmd)
                request = self.cursor.fetchone()

                return list(request)
            except:
                return {"error": "Couldn't Insert into Database"}

    def get_all_records(self, tbl_name, username=None):
        if username:
            select_cmd = "SELECT * FROM {} WHERE username = '{}' ORDER BY id ASC".format(
                tbl_name, username)
        else:
            select_cmd = "SELECT * FROM {} ORDER BY id ASC".format(
                tbl_name, username)

        self.cursor.execute(select_cmd)
        requests = self.cursor.fetchall()
        return list(requests)

    def get_single_record(self, column, value, tbl_name, username=None):
        if username:
            select_cmd = "SELECT * FROM {} WHERE {} = {} AND username = '{}'".format(
                tbl_name, column, value, username)
        else:
            select_cmd = "SELECT * FROM {} WHERE {} = {}".format(
                tbl_name, column, value)
        try:
            self.cursor.execute(select_cmd)
            request = self.cursor.fetchone()
            return request
        except:
            return {"error": "Couldn't select item"}

    def update_record(self, id, tbl_name, **kwargs):
        statement = ""

        if kwargs is not None:
            for key, value in kwargs.items():
                statement = statement + key + " = '" + value + "',"

            statement = statement.rstrip(",")

            update_cmd = "UPDATE {} SET ".format(
                tbl_name) + statement + " WHERE id = {}".format(id)

            try:
                self.cursor.execute(update_cmd)
                get_back_cmd = "SELECT * FROM {} WHERE id = {}".format(
                    tbl_name, id)
                self.cursor.execute(get_back_cmd)
                request = self.cursor.fetchone()

                return list(request)
            except:
                return {"error": "Couldn't insert into database"}

    def delete_record(self, tbl_name, id):
        delete_cmd = "DELETE FROM {} WHERE id={}".format(tbl_name, id)

        self.cursor.execute(delete_cmd)


class UserDatabaseHandler(DatabaseHandler):

    def create_table(self, tbl_name):
        create_table_cmd = "CREATE TABLE {}(id serial PRIMARY KEY, username varchar(400), password varchar(100), type varchar(20), created timestamp)".format(
            tbl_name)
        
        self.cursor.execute(create_table_cmd)

    def get_single_record(self, username, tbl_name):
        try:
            self.cursor.execute(
                "SELECT * FROM {} WHERE username = '{}'".format(tbl_name, username))
            request = self.cursor.fetchone()
            return request
        except:
            return {"error": "Couldn't select"}

    def delete_record(self, tbl_name, username):

        delete_cmd = "DELETE FROM {} WHERE username='{}'".format(
            tbl_name, username)
        pprint(delete_cmd)
        self.cursor.execute(delete_cmd)
