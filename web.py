from flask import Flask, request, jsonify
import json
import os
from flask_sqlalchemy import SQLAlchemy
from flask_expects_json import expects_json
from sqlalchemy_utils import create_database, database_exists

schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'firstName': {'type': 'string'},
        'lastName': {'type': 'string'},
        'nationality': {'type': 'string'}
    },
    'required': ['id', 'firstName', 'lastName', 'nationality']
}
schema_id = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'}
    },
    'required': ['id']
}


def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(
                    convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


app = Flask(__name__)
url = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(os.environ['MYSQL_USER'], os.environ['MYSQL_PASSWD'], os.environ['MYSQL_HOST'], '3306', 'User')
if not database_exists(url):
    create_database(url)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    nationality = db.Column(db.String(80), nullable=False)

    def __init__(self, id, firstName, lastName, nationality):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.nationality = nationality

    @property
    def json(self):
        return to_json(self, self.__class__)


db.create_all()
db.session.commit()


@app.route('/', methods=['POST'])
@expects_json(schema)
def createUser():
    try:
        content = request.json
        temp = content.keys()
        expected_f = {'id', 'firstName', 'lastName', 'nationality'}
        list_extra_f = [ele for ele in temp if ele not in expected_f]
        if len(list_extra_f) != 0:
            return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}

        exists = db.session.query(db.session.query(
            User).filter_by(id=content['id']).exists()).scalar()
        if exists:
            return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}
        else:
            user = User(content['id'], content['firstName'],
                        content['lastName'], content['nationality'])
            db.session.add(user)
            db.session.commit()
            return user.json, 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}


@app.route('/', methods=['PUT'])
def updateUser():
    try:
        content = request.json

        temp = content.keys()
        expected_f = {'id', 'firstName', 'lastName', 'nationality'}
        list_extra_f = [ele for ele in temp if ele not in expected_f]
        if len(list_extra_f) != 0:
            return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}

        exists = db.session.query(db.session.query(
            User).filter_by(id=content['id']).exists()).scalar()
        if exists:
            user = db.session.query(User).filter_by(id=content['id']).one()
            if 'firstName' in content:
                user.firstName = content['firstName']
            if 'lastName' in content:
                user.lastName = content['lastName']
            if 'nationality' in content:
                user.nationality = content['nationality']
            db.session.commit()
            user = db.session.query(User).filter_by(id=content['id']).one()
            return user.json, 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'status': 'Not Found'}), 404, {'ContentType': 'application/json'}
    except:
        return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}


@app.route('/', methods=['DELETE'])
@expects_json(schema_id)
def delUser():
    try:
        content = request.json

        temp = content.keys()
        expected_f = {'id'}
        list_extra_f = [ele for ele in temp if ele not in expected_f]
        if len(list_extra_f) != 0:
            return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}

        exists = db.session.query(db.session.query(
            User).filter_by(id=content['id']).exists()).scalar()
        if exists:
            user = db.session.query(User).filter_by(id=content['id']).one()
            db.session.delete(user)
            db.session.commit()
            return json.dumps({'status': 'User removed'}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'status': 'Not Found'}), 404, {'ContentType': 'application/json'}
    except:
        return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}


@app.route('/', methods=['GET'])
@expects_json(schema_id)
def getUser():
    try:
        content = request.json

        temp = content.keys()
        expected_f = {'id'}
        list_extra_f = [ele for ele in temp if ele not in expected_f]
        if len(list_extra_f) != 0:
            return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}

        exists = db.session.query(db.session.query(
            User).filter_by(id=content['id']).exists()).scalar()
        if exists:
            user = db.session.query(User).filter_by(id=content['id']).one()
            return user.json, 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'status': 'Not Found'}), 404, {'ContentType': 'application/json'}
    except:
        return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return json.dumps({'status': 'Healthy'}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
