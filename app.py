import os
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc
import psycopg2


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/events'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)

    def __init__(self, date):
        self.date = date


class EventSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date')


event_schema = EventSchema()
events_schema = EventSchema(many=True)

db.create_all()
db.session.commit()


@app.route('/', methods=['GET'])
def add_event():
    event_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_event = Event(event_date)

    db.session.add(new_event)
    db.session.commit()

    return "added new event, with date = " + event_date


@app.route('/all_events', methods=["GET"])
def get_events():
    all_events = Event.query.order_by(desc(Event.id)).limit(50).all()
    result = events_schema.dump(all_events)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=3020)
