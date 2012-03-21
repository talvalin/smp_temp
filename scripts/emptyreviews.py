#!/usr/bin/python
# encoding: utf-8
import psycopg2
import sys
import pprint
import fnmatch
import os
import os.path
import collections
from psycopg2.extras import NamedTupleConnection
from psycopg2.extensions import QuotedString
#import unicodedata
import logging

#Define our connection string
conn_string = "host='localhost' port='5433' dbname='SMP' user='postgres' password='Foundation'"

logging.basicConfig(filename='log_importreview.txt', level=logging.INFO)

def updatereviews(idmap):
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    for k,v in idmap.iteritems():
        # load file using path of v
        with open(v, 'r') as f:
            text = f.read().decode("windows-1252")

            try:
                # need to replace all non-ascii characters with their ascii equivalents or a blank character
                text = text.replace(u'’', u"'")
                text = text.replace (u'\u2018', u"'")
                text = text.replace (u'\u2013', u"-")
                text = text.replace (u'\u201c', u'"')
                text = text.replace (u'\u201d', u'"')
                text = text.replace (u'\xe5', u'')
                text = text.replace (u'\xe9', u'')
                text = text.replace (u'\u2026', u'...')
                text = text.replace (u'\xef', u'')
                text = text.replace (u'\xfc', u'')
                text = text.replace (u'\xa9', u'')
                text = text.replace (u'\xeb', u'')
                text = text.replace (u'\xa3', u'')
                text = text.replace (u'\xe1', u'')
                text = text.replace (u'\xe0', u'')
                text = text.replace (u'\xe7', u'')
                text = text.replace (u'\xf3', u'')
                text = text.replace (u'\xfa', u'')
                text = text.replace (u'\xe8', u'')

                text.encode("ascii")
                text = QuotedString(text).getquoted()

                # execute our Query
                querystring = 'UPDATE eiga_article set body={0} where id={1}'.format(text, k)
                logging.info(querystring)
                cursor.execute(querystring)
                conn.commit()
                logging.info("eiga_article row id=%s updated!" % (k))
            except:
                # Get the most recent exception
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                # Exit the script and print an error telling what happened.
                print text
                sys.exit("Database connection failed!\n ->%s" % (exceptionValue))


            #except Exception:
            #    error = "Parsing fail for file %s" % (v)
            #    logging.info(error)
            #    sys.exc_clear()
            #    pass





def getreviewfiles():
    path = '/Users/Lal/PycharmProjects/SMP Data/SMP files/Reviews'

    list_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename[-4:] == '.txt':
                if 'dvd' not in filename:
                    list_of_files[filename] = os.sep.join([dirpath, filename])

    return list_of_files


def getreviewids():
    try:
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

        # execute our Query
        cursor.execute("SELECT id, body FROM eiga_article")
        
        # retrieve the records from the database
        return cursor.fetchall()

    except:
        # Get the most recent exception
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        # Exit the script and print an error telling what happened.
        sys.exit("Database connection failed!\n ->%s" % (exceptionValue))

def matchreviewidwithtext(ids, filenames):
    idmap = {}

    for i in ids:
        for k,v in filenames.iteritems():
            if k[:-4] in i.body:
                idmap[i.id] = v
                break

    return idmap

if __name__ == "__main__":
    logging.info('Starting review import script!')

    # get eiga_article ids and body text
    ids = getreviewids()

    # load the reviews into a dictionary of filename: review text
    filenames = getreviewfiles()
    idmap = matchreviewidwithtext(ids, filenames)
    for k,v in idmap.iteritems():
        print k, v
    updatereviews(idmap)