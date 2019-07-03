import os
import psycopg2
from flask import Flask, request
from psycopg2 import Error

def is_production():
    """ Determines if app is running on the production server or not.
    Get Current URI.
    Extract root location.
    Compare root location against developer server value 127.0.0.1:5000.
    :return: (bool) True if code is running on the production server, and False otherwise.
    FROM: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:8000/'
    return root_url != developer_url

def query_sql(in_query):
    try:
        connection = []
        if ~is_production():
            connection = psycopg2.connect(user = "cmart",
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "SteamChurn_200k")
        else:
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