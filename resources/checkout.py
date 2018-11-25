from flask_restful import reqparse, Resource
from Visa.common.parsers import checkout_parser
# from python_shared.validators import beacon
from Visa.common.token import TokenValidator

import requests


class Checkout(Resource):
    def __init__(self, **kwargs):
        self.mongo = kwargs['mongo'].db

    def post(self, beacon_id):
        args = checkout_parser.parse_args()
        token = TokenValidator(args['token'])
        if token.is_valid():
            del args['token']
            beacon = self.mongo.Beacons.find_one_or_404(beacon_id)
            if token.user == beacon['seller']:
                self.mongo.Beacons.update({'_id': beacon['_id']}, {'value': args['value']})

    def get(self, beacon_id):
        beacon = self.mongo.Beacons.find_one_or_404({'beacon_id': beacon_id}, {'_id': 0})
        return beacon, 200





