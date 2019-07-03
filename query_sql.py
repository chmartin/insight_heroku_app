import os
import psycopg2
from psycopg2 import Error

def query_sql(in_query):
    to_return = []
    try:
        #connection = psycopg2.connect(user = "cmart",
        #                                  host = "127.0.0.1",
        #                                  port = "5432",
        #                                  database = "SteamChurn_200k")
        DATABASE_URL = os.environ['DATABASE_URL']
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        
        cursor = connection.cursor()
        cursor.execute(in_query)
        to_return = cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while filling PostgreSQL table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                
    return to_return