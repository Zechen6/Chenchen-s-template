import pymysql
from flask import jsonify
from json import dumps,dump
import Dao.Sercurity as sercurity

class DBExecutor():
    # connect database
    def __init__(self):
        self.database = "suggestion_db"
        # db = pymysql.connect(host="localhost", port=3306, user="suggestionadmin", passwd="King9thegod", database=database)

        self.connections = pymysql.connections.Connection(host="localhost", port=3306, user="suggestionadmin", passwd="King9thegod", database=self.database)
        self.cursor = self.connections.cursor()

    def save_entity(self, entity):
        self.is_connected()
        sercurity.injection_attack_detector(entity)
        insert_sql = "insert into " + self.database + "." + entity.table_name
        key_list = ""
        value_list = "values("
        c = 0
        for param in entity.param_list:
            if c == 0:
                key_list = param
                value_list += "\'" + entity.param_dict[param] + "\'"
                c = 1
                continue
            key_list += "," + param
            value_list += ",\'" + entity.param_dict[param] + "\'"
        key_list = "(" + key_list + ")"
        value_list = value_list + ")"
        sentence = insert_sql + key_list + ' ' + value_list
        self.cursor.execute(sentence)
        self.connections.commit()

    def get_entity(self, Id, entity):
        self.is_connected()
        sercurity.injection_attack_detector_single_param(Id)
        key_list = self.get_key_list(entity=entity)
        select_sql = "select " + key_list + " from " + entity.table_name
        sentence = select_sql + " where Id = \'" + Id + "\';"
        self.cursor.execute(sentence)
        result = self.cursor.fetchall()
        res_list = self.resolve_result(result=result, entity=entity)
        return res_list

    def get_count(self, table_name):
        self.is_connected()
        sercurity.injection_attack_detector_single_param(table_name)
        select_sql = "select count(*) as count from " + table_name + ";"
        self.cursor.execute(select_sql)
        result = self.cursor.fetchone()[0]
        res = {"count" : result}
        return res

    def rand_get(self, entity, num):
        self.is_connected()
        sercurity.injection_attack_detector_single_param(num)
        key_list = self.get_key_list(entity=entity)
        select_sql = "select " + key_list + " from " + entity.table_name
        rand_sql = " ORDER BY RAND() LIMIT "+ str(num) +";"
        sentence = select_sql + rand_sql
        self.cursor.execute(sentence)
        result = self.cursor.fetchall()
        res_list = self.resolve_result(result=result, entity=entity)
        return res_list

    def get_all(self, entity):
        self.is_connected()
        key_list = self.get_key_list(entity=entity)
        select_sql = "select " + key_list + " from " + entity.table_name + ";"
        sentence = select_sql
        self.cursor.execute(sentence)
        result = self.cursor.fetchall()
        res_list = self.resolve_result(result=result, entity=entity)
        return res_list

    def get_by_key(self, entity, key, key_value):
        self.is_connected()
        param_list = [key, key_value]
        sercurity.injection_attack_detector_param_list(param_list)
        key_list = self.get_key_list(entity=entity)
        select_sql = "select " + key_list + " from " + entity.table_name
        where_sql = " where " + str(key) + "=\"" + str(key_value) + "\";"
        sentence = select_sql + where_sql
        self.cursor.execute(sentence)
        result = self.cursor.fetchall()
        res_list = self.resolve_result(result=result, entity=entity)
        return res_list

    def delete_by_id(self, entity, id):
        self.is_connected()
        sercurity.injection_attack_detector_single_param(id)
        delete_sql = "update " + entity.table_name + " set is_deleted = 1 "
        where_sql = "where id=\'" + str(id) + "\'"
        sentence = delete_sql + where_sql
        self.cursor.execute(sentence)
        self.connections.commit()
        return 0

    """Static Method"""
    def resolve_result(self, result, entity):
        res_list = []
        for i in range(len(result)):
            for j in range(len(entity.param_list)):
                entity.param_dict[entity.param_list[j]] = result[i][j]
            json = dumps(obj=entity.param_dict, ensure_ascii=False)
            res_list.append(json)
        return jsonify(res_list)

    def get_key_list(self, entity):
        key_list = ""
        c = 0
        for param in entity.param_list:
            if c == 0:
                key_list = param
                c = 1
                continue
            key_list += "," + param
        return key_list

    def is_connected(self):
        """Check if the server is alive"""
        try:
            self.connections.ping(reconnect=True)
            print("db is connecting")
        except:
            self.connections = pymysql.connections.Connection(host="localhost", port=3306, user="suggestionadmin", passwd="King9thegod", database=self.database)
            print("db reconnect")






