from flask_restplus import fields, reqparse

session_only = reqparse.RequestParser()
session_only.add_argument('session_id', type=str)



