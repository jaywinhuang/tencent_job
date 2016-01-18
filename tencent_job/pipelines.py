# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log, signals
from scrapy.exporters import CsvItemExporter
import MySQLdb
from twisted.enterprise import adbapi
from tencent_job import settings
from scrapy.exceptions import DropItem


class TencentJobPipeline(object):

    def __init__(self,dbpool):
        log.msg('start dualing item pipelines  1========================>>')
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        log.msg('start dualing item pipelines  2========================>>')
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)
        return cls(dbpool)

    def process_item(self,item,spider):
        log.msg('start dualing item pipelines========================>>')
        d = self.dbpool.runInteraction(self._do_upsert,item,spider)
        d.addErrback(self._handle_error,item,spider)
        d.addBoth(lambda _: item)
        return d

    def _do_upsert(self,conn,item,spider):
        log.msg('start insert mysql @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        conn.execute("""SELECT EXISTS (SELECT 1 from all_job where id = %s)""",(item['id']))
        job_id_exist = conn.fetchone()[0]

        if job_id_exist:
            conn.execute("""UPDATE all_job SET issue_time = %s""",(item['issue_time']))

        else:
            conn.execute("""INSERT INTO all_job (company,title,id,duty,requirement,location,category,first_time,issue_time,link)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,(item['company'],item['title'],item['id'],item['duty'],item['requirement'],item['location'],item['category'],item['issue_time'],item['issue_time'],item['link']))

    def _handle_error(self, failure, item, spider):

        log.err(failure)



    # def __init__(self):
    #     self.conn = MySQLdb.connect(host=settings.MYSQL_HOST,port=settings.MYSQL_PORT, user=settings.MYSQL_USER,passwd=settings.MYSQL_PASSWORD,db=settings.MYSQL_DBNAME)
    #     # self.conn = MySQLdb.connect(host='localhost',port=3306, user='root',passwd='jaywin',db='local_db')
    #     self.cursor = self.conn.cursor()
    #
    # def parse_item(self,item,spider):
    #     try:
    #         self.cursor.excute("""INSERT INTO job_list_tencent () values ()""",)

# class TencentJobPipeline(object):
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         pipeline = cls()
#         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#         return pipeline
#
#     def spider_opened(self,spider):
#         file = open('tencent_job_list.csv','w')
#         self.exporter = CsvItemExporter(file)
#         self.exporter.start_exporting()
#
#     def spider_closed(self,spider):
#         self.exporter.finish_exporting()
#         file.close()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
