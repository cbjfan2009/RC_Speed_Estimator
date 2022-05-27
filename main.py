from flask import Flask, render_template, request, json, redirect
from math import pi
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, Column, Integer, Numeric, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PIL import Image
from os import environ
from boto.s3.connection import S3Connection


# -------------------------------------SQLAlchemy approach-----------------------------------------------

app = Flask(__name__)

s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])

db = create_engine(db_string, echo=True)

meta = MetaData()

base = declarative_base()


class Visitors(base):
    __tablename__ = 'estimation_data'

    pkid = Column(Integer, primary_key=True, autoincrement=True)
    motor_kv = Column('motor_kv', Integer)
    batt_volt = Column('batt_volt', Numeric)
    pinion = Column('pinion', Integer)
    spur = Column('spur', Integer)
    final_ratio = Column('final_ratio', Numeric)
    wheel_rad = Column('wheel_rad', Numeric)
    speed_output = Column('speed_output', Numeric)

    def __init__(self, motor_kv, batt_volt, pinion, spur, final_ratio, wheel_rad, speed_output):

        self.motor_kv = motor_kv
        self.batt_volt = batt_volt
        self.pinion = pinion
        self.spur = spur
        self.final_ratio = final_ratio
        self.wheel_rad = wheel_rad
        self.speed_output = speed_output


class Poll_response(base):
    __tablename__ = 'poll_response'

    response = Column('response', String, primary_key=True)
    count = Column('count', Integer)

    def __init__(self, response, count):
        self.response = response
        self.count = count


Session = sessionmaker(db)

session = Session()

base.metadata.create_all(db)


# Routing for HTML

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_kv = int(request.form['motorkV'])
        user_batteryvolt = float(request.form['battVolt'])
        user_pinion = int(request.form['pinion'])
        user_spur = int(request.form['spur'])
        user_fgr = float(request.form['fgr'])
        user_wheelradius = float(request.form['wheelradius'])
        totalrpm = user_kv * user_batteryvolt
        wheel_circum = 2*pi*user_wheelradius
        speed = round((totalrpm / ((user_spur / user_pinion) * user_fgr) * (wheel_circum/12) * (60 / 5280)), 2)
        new_visitor = Visitors(motor_kv=user_kv, batt_volt=user_batteryvolt, pinion=user_pinion, spur=user_spur,
                               final_ratio=user_fgr, wheel_rad=user_wheelradius, speed_output=speed)
        session.add(new_visitor)
        session.commit()

        return render_template("index.html", speed_display=speed)

    else:
        return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/about_me')
def about_me():
    return render_template("about_me.html")

@app.route('/play_time')
def play_time():
    return render_template("play_time.html")


# Making array of response/count data so I can put it into Google Charts trying list of lists

sql_arr_response = [i.response for i in session.query(Poll_response)]
sql_arr_count = [i.count for i in session.query(Poll_response)]


sql_zipped = zip(sql_arr_response, sql_arr_count)

sql_array = [['Brand', 'Vote Count']]
for x, y in sql_zipped:
    sql_array.append([x, y])



@app.route('/poll', methods=['POST', 'GET'])
def poll():
    poll_data = session.query(Poll_response).all()
    poll_data_dict = {}
    sql_dic_array = {'Brand': 'Vote Count'}

    for item in poll_data:
        poll_data_dict.update({item.response: item.count})
        sql_dic_array.update({item.response: item.count})


    if request.method == 'POST':
        response = request.form['poll']
        session.query(Poll_response).filter(Poll_response.response == response).update(
            {Poll_response.count: Poll_response.count + 1}
        )
        session.commit()
        return redirect(request.referrer)

    return render_template("poll.html", poll_data=poll_data, poll_data_dict=poll_data_dict, sql_dic_array=sql_dic_array)



@app.route('/estimator_data', methods=['POST', 'GET'])
def estimator_data():
    try:
        return render_template("estimator_data.html", sql_data=session.query(Visitors).all())

    except:
        return "Something went wrong with the database connection!"


@app.route('/biography')
def biography():
    return render_template("biography.html")


if __name__ == "__main__":
    app.run(debug=True)

