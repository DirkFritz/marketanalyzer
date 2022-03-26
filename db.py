import mysql.connector
from mysql.connector import Error


class Db:
    def __init__(self):

        try:
            self.connection = mysql.connector.connect(
                host="34.141.0.22",
                unix_socket="/cloudsql/marketdata-339820:europe-west3:stocksdata",
                database="stockprices",
                user="root",
                password="ltcapital",
            )
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.connection.cursor()

        except Error as e:
            print("Error processing database", e)

    def close(self):
        print("Close mysql connection")
        self.cursor.close()
        self.connection.close()

    def select_historic(self):
        self.cursor = self.connection.cursor()

        sql = "SELECT COUNT(*) FROM historic"
        self.cursor.execute(sql)
        print(self.cursor.fetchall())
        sql = "SELECT * FROM historic"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def select_historic_date(self, date):
        sql = f"SELECT * FROM historic WHERE date >='{date}'"

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_unique_values(self, col):
        sql = f"SELECT DISTINCT({col}) FROM historic"

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_min_max_historic(self, column):
        sql = f"SELECT MIN({column}) FROM historic"
        self.cursor.execute(sql)
        min = self.cursor.fetchall()
        sql = f"SELECT MAX({column}) FROM historic"
        self.cursor.execute(sql)
        max = self.cursor.fetchall()

        return [min[0][0], max[0][0]]
