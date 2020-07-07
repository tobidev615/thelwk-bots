# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import pymysql
from scrapy.exceptions import NotConfigured

class PMNewsPipeline(object):
    
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
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='naija-news-box')
        self.curr= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title')
        date_sql = item.get('date')
        pictures = item.get('pic')
        thumb = item.get('news_thumb')
        react = item.get('reaction')
        story = item.get('full_story')
        linker = item.get('news_Linker')
        category = item.get('tags')
        source = item.get('source')
        page = item.get('page')
        commando="INSERT INTO pm_store_import(title, sql_date, image, thumb, body, link, category, source, reactions, page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.curr.execute('SAVEPOINT last_save')
        try: 
            self.curr.execute(commando,(title, date_sql, pictures, thumb, story, linker, category, source, react, page))
        except:
            self.curr.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item

class ConciseNewsPipeline(object):
    
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
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='naija-news-box')
        self.curr= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title')
        date_sql = item.get('date')
        pictures = item.get('image')
        brief = item.get('brief')
        story = item.get('body')
        media = item.get('media')
        link = item.get('link')
        category = item.get('tag')
        source = item.get('source')
        page = item.get('page')
        commando="INSERT INTO concise_store(title, sql_date, image, brief, body, media, link, category, source, page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.curr.execute('SAVEPOINT last_save')
        try: 
            self.curr.execute(commando,(title, date_sql, pictures, brief, story, media, link, category, source, page))
        except:
            self.curr.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item

class TheNationNewsPipeline(object):
    
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
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='naija-news-box')
        self.curr= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title')
        date_sql = item.get('date')
        pictures = item.get('image')
        brief = item.get('brief')
        story = item.get('body')
        link = item.get('link')
        category = item.get('tag')
        source = item.get('source')
        page = item.get('page')
        commando="INSERT INTO thenation_store(title, sql_date, image, brief, body, link, category, source, page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.curr.execute('SAVEPOINT last_save')
        try: 
            self.curr.execute(commando,(title, date_sql, pictures, brief, story, link, category, source, page))
        except:
            self.curr.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item

class TribuneNewsPipeline(object):
    
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
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='naija-news-box')
        self.curr= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title')
        date_sql = item.get('date')
        pictures = item.get('image')
        brief = item.get('brief')
        story = item.get('body')
        link = item.get('link')
        category = item.get('tag')
        source = item.get('source')
        page = item.get('page')
        commando="INSERT INTO tribune_store(title, sql_date, image, brief, body, link, category, source, page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.curr.execute('SAVEPOINT last_save')
        try: 
            self.curr.execute(commando,(title, date_sql, pictures, brief, story, link, category, source, page))
        except:
            self.curr.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item


class PunchNewsPipeline(object):
    
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
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='naija-news-box')
        self.curr= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title')
        date_sql = item.get('date')
        pictures = item.get('image')
        brief = item.get('brief')
        story = item.get('body')
        link = item.get('link')
        category = item.get('tag')
        source = item.get('source')
        page = item.get('page')
        commando="INSERT INTO punch_store(title, sql_date, image, brief, body, link, category, source, page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.curr.execute('SAVEPOINT last_save')
        try: 
            self.curr.execute(commando,(title, date_sql, pictures, brief, story, link, category, source, page))
        except:
            self.curr.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item

class VangaurdNewsPipeline(object):
    
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
        self.conn = pymysql.connect(host=self.host ,user=self.user,password=self.passwd,db='naija-news-box')
        self.curr= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title')
        date_sql = item.get('date')
        pictures = item.get('pic')
        brief = item.get('brief')
        story = item.get('full_story')
        link = item.get('news_Link')
        category = item.get('tags')
        source = item.get('source')
        page = item.get('page')
        commando="INSERT INTO vanguard_store3(title, sql_date, image, brief, body, link, category, source, page) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.curr.execute('SAVEPOINT last_save')
        try: 
            self.curr.execute(commando,(title, date_sql, pictures, brief, story, link, category, source, page))
        except:
            self.curr.execute('ROLLBACK TO SAVEPOINT last_save')        
        self.conn.commit()
        return item
