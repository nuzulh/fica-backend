import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
        return cnx
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)
        return cnx


def get():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM fish;')
        fishes = cursor.fetchall()
        if result > 0:
            return jsonify(fishes)
        return 'No fish found by id'+id


def get_one(id):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM fish WHERE label=%s', (id))
        fish = cursor.fetchall()
        if result > 0:
            return jsonify(fish)
        return 'No fish found by id'+id


def create(fish):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO fishes (label, name, description, min_price, max_price) VALUES(%s, %s, %s, %s, %s)',
                       (fish["label"], fish["name"], fish["description"], fish["min_price"], fish["max_price"]))
    conn.commit()
    conn.close()
