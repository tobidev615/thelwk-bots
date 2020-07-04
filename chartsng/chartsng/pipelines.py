# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AppleChartPipeline(object):
    
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
        self.curr= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        date = item.get('date')
        playlist  = item.get('playlist')
        rank = item.get('rank')
        title = item.get('title')
        artist = item.get('artist')
        artwork = item.get('art_work')
        link = item.get('link_to')
        commando ='INSERT INTO appleng_playlist(date, playlist, rank, title, artist, img_link, song_link) VALUES(%s,%s,%s,%s,%s,%s,%s)'
        self.curr.execute('SAVEPOINT last_save')
        try: 
            self.curr.execute(commando,(date, playlist, rank, title, artist, artwork, link))
        except:
            self.curr.execute('ROLLBACK TO SAVEPOINT last_save') 
        self.conn.commit()
        return item


class CovidChartPipeline(object):
    
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
        self.curr= self.conn.cursor()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        date = item.get('date')
        samples_tested  = item.get('samples_tested')
        state = item.get('state')
        total = item.get('total')
        active = item.get('active')
        discharged = item.get('discharged')
        death = item.get('death')
        commando="INSERT INTO covidng_store(date, samples_tested, state, total_cases, active_cases, discharged, death) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        self.curr.execute('SAVEPOINT last_save')
        try: 
            self.curr.execute(commando,(date, samples_tested, state, total, active, discharged, death))
        except:
            self.curr.execute('ROLLBACK TO SAVEPOINT last_save') 

        self.conn.commit()
        return item

class ChartsngPipeline(object):
    def process_item(self, item, spider):
        return item
