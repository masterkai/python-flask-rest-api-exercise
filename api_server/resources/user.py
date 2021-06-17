from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import pymysql
import traceback
from api_server.server import db
from api_server.models import UserModel

parse = reqparse.RequestParser()
parse.add_argument('name')
parse.add_argument('gender')
parse.add_argument('birth')
parse.add_argument('description')


class User(Resource):
    def db_init(self):
        db = pymysql.connect('localhost', 'root', 'password', 'api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * From api.users where id = '{}' and deleted is not True """.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()

        return jsonify({'data': user})

    def patch(self, id):
        # db, cursor = self.db_init()
        arg = parse.parse_args()
        # user = {
        #     'name': arg['name'],
        #     'gender': arg['gender'],
        #     'birth': arg['birth'],
        #     'description': arg['description']
        # }
        # query = []
        # for key, value in user.items():
        #     if value != None:
        #         query.append(key + " = " + "'{}'".format(value))
        # query = ", ".join(query)
        # sql = """
        # UPDATE `api`.`users` SET {} WHERE (`id` = '{}');
        # """.format(query, id)
        user = UserModel.query.filter_by(id=id, deleted=None).first()
        if arg['name'] != None:
            user.name = arg['name']

        response = {}
        try:
            db.session.commit()
            response['msg'] = 'success'
            # cursor.execute(sql)
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        # db.commit()
        # db.close()
        return jsonify(response)

    def delete(self, id):
        # db, cursor = self.db_init()
        # sql = """
        #     UPDATE `api`.`users` SET deleted = True WHERE (`id` = '{}');
        # """.format(id)
        user = UserModel.query.filter_by(id=id, deleted=None).first()

        response = {}
        try:
            db.session.delete(user)
            db.session.commit()
            # cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        # db.commit()
        # db.close()
        return jsonify(response)


class Users(Resource):
    def db_init(self):
        db = pymysql.connect('localhost', 'root', 'password', 'api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    # @property
    def get(self):
        # db, cursor = self.db_init()
        # arg = parse.parse_args()
        # sql = 'Select * From api.users where deleted is not True'
        # if arg['gender'] != None:
        #     sql += ' and gender = "{}"'.format(arg['gender'])
        # cursor.execute(sql)
        # db.commit()
        # users = cursor.fetchall()
        # db.close()
        print(UserModel)
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        print(users)
        return jsonify({'data': list(map(lambda user: user.serialize(), users))})
        # return jsonify({'data':users})

    def post(self):
        # db, cursor = self.db_init()
        arg = parse.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or '1999-01-01',
            'description': arg['description'],
        }
        # sql = """INSERT INTO `api`.`users` ( `name`, `gender`, `birth`,`description`) VALUES ('{}', '{}', '{}', '{}');""".format(
        #     user['name'], user['gender'], user['birth'], user['description'])
        #
        response = {}
        status_code = 200

        try:
            # cursor.execute(sql)
            new_user = UserModel(name=user['name'], gender=user['gender'], birth=user['birth'],
                                 description=user['description'])
            db.session.add(new_user)
            db.session.commit()
            response['msg'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'failed'
        # db.commit()
        # db.close()
        return make_response(jsonify(response), status_code)
