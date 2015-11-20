# coding:utf-8

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


class Train(Resource):
    def get(self):
        pass
