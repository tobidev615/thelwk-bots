# -*- coding: utf-8 -*-
import os
from scrapy.exceptions import NotConfigured
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class localTrendPipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings: # if we don't define db config in settings
            raise NotConfigured # then reaise error
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host) # returning pipeline instance

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='twitterng')
        self.cur= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()


    def process_item(self, item, spider):
        trend = item.get('trend')
        date  = item.get('date')
        rank = item.get('trend_type')
        tweet = item.get('tweets')
        number = item.get('number')
        link = item.get('link')
        self.cur.execute('SAVEPOINT last_save')
        commando = 'INSERT INTO trends_ng(trend, date, rank, tweets, number, tweet_link) VALUES(%s,%s,%s,%s,%s,%s)'
        try:
            self.cur.execute(commando,(trend, date, rank, tweet, number, link))
        except :
            self.cur.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item


class localFeedPipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings: # if we don't define db config in settings
            raise NotConfigured # then reaise error
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host) # returning pipeline instance

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='twitterng')
        self.cur= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        number = item.get('number')
        post  = item.get('post')
        tweet_type = item.get('type')
        poster = item.get('poster')
        videos = item.get('videos')
        images = item.get('images')
        time = item.get('time')
        link = item.get('link')
        commando ="INSERT INTO tweetfeedng_store(post, tweet_type, poster, videos, images, date, tweet_link) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        self.cur.execute('SAVEPOINT last_save')
        try:
            self.cur.execute(commando,(post, tweet_type, poster, videos, images, time, link))
        except :
            self.cur.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item
        

class localNetflixPipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod 
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings: # if we don't define db config in settings
            raise NotConfigured # then reaise error
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host) # returning pipeline instance

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='chartsng')
        self.cur= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        date = item.get('date')
        category  = item.get('category')
        name = item.get('name')
        rank = item.get('rank')
        image = item.get('image')
        self.cur.execute('SAVEPOINT last_save')
        commando ='INSERT INTO netflixng_store (date, category, rank, title, img_link) VALUES(%s,%s,%s,%s,%s)'
        self.cur.execute('SAVEPOINT last_save')
        try:        
            self.cur.execute(commando,(date, category, rank, name, image))
        except :
            self.cur.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item

class SelchartsngPipeline(object):
    def process_item(self, item, spider):
        return item
