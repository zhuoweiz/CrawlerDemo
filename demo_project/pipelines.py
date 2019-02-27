# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import mysql.connector
from mysql.connector import errorcode

class MongoDbPipeline(object):
    collection = 'RecentlySold'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # get env variables
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    # when to open and close
    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri) #
        self.db = self.client[self.mongo_db] # connect to db called goodreads

    def close_spider(self, spider):
        self.client.close()

    
    def process_item(self, item, spider):
        # print("TESTING..." + dict(item)['listPrice'])
        self.db[self.collection].insert_one(dict(item))
        return item

class MySQLPipeline(object):
    DB_NAME = 'houses'
    TABLES = {}
    TABLES['soldHouses'] = "CREATE TABLE soldHouses ("
    "soldID INT(10) PRIMARY KEY AUTO_INCREMENT,"
    "listPrice VARCHAR(15) NOT NULL,"
    "salePrice VARCHAR(15) NOT NULL," 
    "zipcode VARCHAR(10) NOT NULL,"
    "daysOnMarket VARCHAR(30) NOT NULL);"
    
    def __init__(self, mysql_db, mysql_host, mysql_user, mysql_pw):
        self.mysql_db = mysql_db
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_pw = mysql_pw

    # get env variables
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_db = crawler.settings.get('MYSQL_DB'),
            mysql_host = crawler.settings.get('MYSQL_HOST'),
            mysql_user = crawler.settings.get('MYSQL_USR'),
            mysql_pw = crawler.settings.get('MYSQL_PW')
        )

    def open_spider(self, spider):
        # try to connect to sql server
        try:
            self.cnx = mysql.connector.connect(user=self.mysql_user, password=self.mysql_pw,host=self.mysql_host,database=self.mysql_db)
            self.cursor = self.cnx.cursor()
            self.create_table(self.cursor)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close_spider(self, spider):
        self.cnx.close()
        self.cursor.close()
    
    def process_item(self, item, spider):
        self.cursor.execute("INSERT INTO soldHouses (listPrice, salePrice, zipcode, daysOnMarket) VALUES ({},{},{},{});".format(dict(item)['listPrice'],dict(item)['salePrice'],dict(item)['zipcode'],dict(item)['daysOnMarket']))
        return item
        
    # helper function
    def create_database(self, cursor):
        try:
            cursor.execute("DROP DATABASE IF EXISTS {};CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME, self.DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_table(self, cursor):
        try:
            cursor.execute("USE {}".format(self.DB_NAME))

            for table_name in self.TABLES:
                table_description = self.TABLES[table_name]
                try:
                    print("Creating table {}: ".format(table_name), end='')
                    cursor.execute(table_description)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                    else:
                        print(err.msg)
                else:
                    print("OK")

        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(cursor)
                print("Database {} created successfully.".format(self.DB_NAME))
                self.cnx.database = self.DB_NAME
            else:
                print(err)
                exit(1)