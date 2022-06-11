import os
import pymysql

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
        return cnx
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user='root', password='',
                              host=host, db='fica')
        return cnx


def get():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM fish;')
        fishes = cursor.fetchall()
        if result > 0:
            return fishes
        else:
            return {'message': 'No fishes found'}


def get_one(prediction):
    conn = open_connection()
    predict_list = {}
    with conn.cursor() as cursor:
        for i in range(len(prediction)):
            result = cursor.execute('SELECT * FROM fish WHERE label=%s', (prediction[i][0])) 
            fish = cursor.fetchall()
            if result > 0:
                fish = fish[0]
                res = {}
                for _ in range(len(fish)):
                    res["label"] = fish[1]
                    res["name"] = fish[2]
                    res["description"] = fish[3]
                    res["min_price"] = fish[4]
                    res["max_price"] = fish[5]
                    res["probability"] = float(prediction[i][1])
                predict_list[i] = res #return res
            else:
                return {'message': 'No fishes found'}
        return predict_list

def create(fish):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO fishes (label, name, description, min_price, max_price) VALUES(%s, %s, %s, %s, %s)',
                       (fish["label"], fish["name"], fish["description"], fish["min_price"], fish["max_price"]))
    conn.commit()
    conn.close()