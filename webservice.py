# -*- coding:utf8 -*-
from spyne import Application, rpc, ServiceBase
from spyne import Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import json
import sys
import pymysql.cursors
from DBUtils.PooledDB import PooledDB


class Person(ComplexModel):
    name = Unicode
    age = Unicode
    sex = Unicode

class SomeSampleServices(ServiceBase):
    # 简单类型调用
    @rpc(Unicode, _returns=Unicode)
    def make_project(self, name):
        print name
        return name

    # 复杂类型调用
    @rpc(Unicode, _returns=Person)
    def make_project_comlex(self, person_in):
        # 连接MySQL数据库
        connection = pymysql.connect(host='192.168.229.129', port=3308, user='root', password='root', db='jpress',
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        # 通过cursor创建游标
        cursor = connection.cursor()

        # 执行数据查询
        sql = "SELECT `id`, `name`,`age`,`sex` FROM `tbPerson` WHERE `name`='%s'" % (person_in)
        cursor.execute(sql)

        # 查询数据库单条数据
        result = cursor.fetchone()
        print(result)

        # 关闭数据连接
        connection.close()

        person2 = Person()
        result
        person2.age = result.has_key('age')
        person2.name = result['name']
        person2.sex = result['sex']

        print person_in
        return person2

    # Json类型调用，与简单类型相同
    @rpc(Unicode, _returns=Unicode)
    def make_project_Json(self, myjson):
        # print myjson
        jsont = json.loads(myjson)
        print jsont
        print jsont['a']
        return myjson

if __name__ == "__main__":
    soap_app = Application([SomeSampleServices],
                           'SampleServices',
                           in_protocol=Soap11(validator="lxml"),
                           out_protocol=Soap11())
    wsgi_app = WsgiApplication(soap_app)
    server = make_server('127.0.0.1', 8080, wsgi_app)

    sys.exit(server.serve_forever())
