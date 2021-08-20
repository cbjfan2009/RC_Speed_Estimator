from flask import Flask, render_template, request
from math import pi
from sqlalchemy import create_engine, Column, Integer, Numeric, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------------------------mysql connection -- if MySQL server is going to be used-----------------------------

# import mysql.connector
# sqldb = mysql.connector.connect(
#   host='localhost',
#   user='devMatt',
#   password='D3V3l0pm3ntS3rV3rcbjfan2009',
#   database='webapp_user_input'
#   )

# mysql query
# def sql_query():
#    dbcursor = sqldb.cursor()
#    dbcursor.execute('SELECT * FROM speed_estimation_inputs')
#    sql_data = dbcursor.fetchall()
#    return sql_data


# ------------------postgresql connection -- if PostgreSQL is going to be used, like with Heroku!-----------------------
# import psycopg2
# postgres://vlinujzpemehpy:81bb09e53a2532c52b6a8696ebf0497b253e0a0516f0c1c741d5ceae3e10806e@ec2-54-211-160-34.compute-1.amazonaws.com:5432/df5p5d20v6pbf9
# pgdb = psycopg2.connect(
#   host='ec2-54-211-160-34.compute-1.amazonaws.com',
#   user='vlinujzpemehpy',
#   password='81bb09e53a2532c52b6a8696ebf0497b253e0a0516f0c1c741d5ceae3e10806e',
#   port='5432',
#   database='df5p5d20v6pbf9'
#   )
# pgcursor = pgdb.cursor()


# def check_connection():
#   pgcursor.execute("select version()")
#   data = pgcursor.fetchone()
#   print("Connection established to: ", data)


# def create_table():
#   sql = '''CREATE TABLE estimation_data
#   (pkid text,
#    Motor_kV integer,
#     Batt_Volt decimal,
#      Pinion integer,
#       Spur integer,
#        Final_Ratio decimal,
#         Wheel_Rad decimal);'''
#   pgcursor.execute(sql)
#   pgdb.commit()


# def pg_add_data(sql, val):
#   pgcursor.execute(sql, val)
#   pgdb.commit()


# def pg_query():
#    pgcursor.execute('SELECT * FROM estimation_data')
#    sql_data = pgcursor.fetchall()
#    return sql_data


# -------------------------------------SQLAlchemy approach-----------------------------------------------
db_string = "postgresql://vlinujzpemehpy:81bb09e53a2532c52b6a8696ebf0497b253e0a0516f0c1c741d5ceae3e10806e@ec2-54-211-160-34.compute-1.amazonaws.com:5432/df5p5d20v6pbf9"

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



Session = sessionmaker(db)

session = Session()

base.metadata.create_all(db)


app = Flask(__name__)


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


@app.route('/poll')
def poll():
    return render_template("poll.html")


@app.route('/estimator_data', methods=['POST', 'GET'])
def estimator_data():
    try:
        return render_template("estimator_data.html", sql_data=session.query(Visitors).all())

    except:
        return "Something went wrong with the database connection!"



if __name__ == "__main__":
    app.run(debug=True)
