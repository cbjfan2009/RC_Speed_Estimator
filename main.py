from flask import Flask, render_template, url_for, request, redirect
from math import pi
# import mysql.connector
import psycopg2

# mysql connection -- if MySQL server is going to be used
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


# postgresql connection -- if PostgreSQL is going to be used, like with Heroku!
# postgres://vlinujzpemehpy:81bb09e53a2532c52b6a8696ebf0497b253e0a0516f0c1c741d5ceae3e10806e@ec2-54-211-160-34.compute-1.amazonaws.com:5432/df5p5d20v6pbf9
pgdb = psycopg2.connect(
   host='ec2-54-211-160-34.compute-1.amazonaws.com',
   user='vlinujzpemehpy',
   password='81bb09e53a2532c52b6a8696ebf0497b253e0a0516f0c1c741d5ceae3e10806e',
   port='5432',
   database='df5p5d20v6pbf9'
   )
pgcursor = pgdb.cursor()


def check_connection():
   pgcursor.execute("select version()")
   data = pgcursor.fetchone()
   print("Connection established to: ", data)


def create_table():
   sql = '''CREATE TABLE estimation_data 
   ("User" text PRIMARY KEY,
    Motor_kV integer,
     Batt_Volt decimal,
      Pinion integer,
       Spur integer,
        Final_Ratio decimal,
         Wheel_Rad decimal);'''
   pgcursor.execute(sql)
   pgdb.commit()


def pg_add_data(sql,val):
   pgcursor.executemany(sql, val)
   pgdb.commit()


def pg_query():
    pgcursor.execute('SELECT * FROM estimation_data')
    sql_data = pgcursor.fetchall()
    return sql_data


app = Flask(__name__)


# Routing for HTML

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_kv = int(request.form['motorkV'])
        user_batteryVolt = float(request.form['battVolt'])
        user_pinion = int(request.form['pinion'])
        user_spur = int(request.form['spur'])
        user_fgr = float(request.form['fgr'])
        user_wheelradius = float(request.form['wheelradius'])
        totalrpm = user_kv * user_batteryVolt
        wheel_circum = 2*pi*user_wheelradius
        speed = round((totalrpm / ((user_spur / user_pinion) * user_fgr) * (wheel_circum/12) * (60 / 5280)), 2)
        return render_template("index.html", speed_display=speed)

    else:
        return render_template("index.html")


@app.route('/hiddenpage')
def hiddenpage():
    return render_template("hiddenpage.html")


@app.route('/poll')
def poll():
    return render_template("poll.html")


@app.route('/estimator_data', methods=['POST', 'GET'])
def estimator_data():
    try:
        check_connection()
        pgdata = pg_query()
        return render_template("estimator_data.html", sql_data=pgdata)
    except:
        return "Something went wrong with the database connection!"
    #sqldata = sql_query() <--if using mysql
    #return render_template("estimator_data.html", sql_data=sqldata)


if __name__ == "__main__":
    app.run(debug=True)
