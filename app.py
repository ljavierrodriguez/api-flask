import os
from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Test

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://lrodriguez:123456@localhost/prueba'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'prueba.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/api/tests", methods=['GET', 'POST'])
@app.route("/api/tests/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def tests(id=None):
    if request.method == 'GET':
        if id is not None:
            test = Test.query.get(id)
            return jsonify(test.serialize()), 200
        else:
            tests = Test.query.all()
            tests = list(map(lambda test: test.serialize(), tests))
            return jsonify(tests), 200

    if request.method == 'POST':
        name = request.json.get('name')
        phone = request.json.get('phone')

        test = Test()
        test.name = name
        test.phone = phone

        db.session.add(test)
        db.session.commit()

        return jsonify(test.serialize()), 201
        
    if request.method == 'PUT':
        name = request.json.get('name')
        phone = request.json.get('phone')

        test = Test.query.get(id)
        test.name = name
        test.phone = phone

        db.session.commit()

        return jsonify(test.serialize()), 200

    if request.method == 'DELETE':
        test = Test.query.get(id)
        db.session.delete(test)
        db.session.commit()
        
        return jsonify({"msg": "Prueba Eliminada"}), 200


if __name__ == '__main__':
    manager.run()