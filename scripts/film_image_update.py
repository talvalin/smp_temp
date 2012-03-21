#!/usr/bin/python
# encoding: utf-8
import psycopg2
import sys
import pprint
from psycopg2.extras import NamedTupleConnection
import os 
#Define our connection string
conn_string = "host='localhost' port='5433' dbname='SMP' user='postgres' password='Foundation'"

def getgifnames():
    path = '/Users/Lal/Developer/Projects/Current/SMP/static/eiga/img/films'

    list_of_files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename[-4:] == '.gif':
                list_of_files.append(filename)

    return list_of_files
		     
def getreviewids():
    try:
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

        # execute our Query
        cursor.execute("SELECT id, title, thumbnail FROM eiga_film ORDER by title")
        
        # retrieve the records from the database
        return cursor.fetchall()

    except:
        # Get the most recent exception
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        # Exit the script and print an error telling what happened.
        sys.exit("Database connection failed!\n ->%s" % (exceptionValue))

def getthumbnails():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute("select id, title, thumbnail, still from eiga_film where title like 'A %' and still like 'a%'")
    return cursor.fetchall()

def updatethumbnails(ids):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    for i in ids:
        thumbnail = i.thumbnail[1:]
        still = i.still[1:]
        querystring = 'UPDATE eiga_film set thumbnail=\'{0}\', still=\'{1}\' where id={2}'.format(thumbnail, still, i.id)
        cursor.execute(querystring)
        conn.commit()

def getmismatches():
    ids = getreviewids()
    thumbfiles = getgifnames()
   
    results = []
    for i in ids:
        if i.thumbnail not in thumbfiles:
            results.append(i)
    
    return results

    
if __name__ == "__main__":

    #results = getthumbnails()
    #updatethumbnails(results)
    results = getmismatches()
    print len(results)	   
    #for r in results:
     #   print r
