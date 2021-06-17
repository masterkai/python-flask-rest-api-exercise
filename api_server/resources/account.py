from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback

parse = reqparse.RequestParser()
parse.add_argument('balance')
parse.add_argument('account_number')
parse.add_argument('user_id')


class Account(Resource):
    def db_init(self):
        db = pymysql.connect('localhost', 'root', 'password', 'api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, user_id, id):
        db, cursor = self.db_init()
        sql = """Select * From api.accounts where id = '{}' and deleted is not True """.format(id)
        cursor.execute(sql)
        db.commit()
        account = cursor.fetchone()
        db.close()

        return jsonify({'data': account})

    def patch(self, user_id, id):
        db, cursor = self.db_init()
        arg = parse.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id']
        }
        query = []
        for key, value in account.items():
            if value != None:
                query.append(key + " = " + "'{}'".format(value))
        query = ", ".join(query)
        sql = """
        UPDATE `api`.`accounts` SET {} WHERE (`id` = '{}');
        """.format(query, id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)

    def delete(self, user_id, id):
        db, cursor = self.db_init()
        sql = """
            UPDATE `api`.`accounts` SET deleted = True WHERE (`id` = '{}');
        """.format(id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)


class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect('localhost', 'root', 'password', 'api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, user_id):
        print(self)
        db, cursor = self.db_init()
        sql = 'Select * From api.accounts where user_id = "{}" and deleted is not True'.format(user_id)
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        db.close()

        return jsonify({'data': accounts})

    def post(self, user_id):
        print(self)
        db, cursor = self.db_init()
        arg = parse.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id']
        }
        sql = """INSERT INTO `api`.`accounts` ( `balance`, `account_number`, `user_id`) VALUES ('{}', '{}', '{}');""".format(
            account['balance'], account['account_number'], account['user_id'])

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)
