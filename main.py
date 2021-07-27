from flask import Flask, render_template, url_for, request, redirect
from math import pi
import mysql.connector

db = mysql.connector.connect(
   host='localhost',
   user='devMatt',
   password='D3V3l0pm3ntS3rV3rcbjfan2009',
   database='webapp_user_input'
   )


app = Flask(__name__)


def sql_query():
    with mysql.connector.connect(host='localhost',
   user='devMatt',
   password='D3V3l0pm3ntS3rV3rcbjfan2009',
   database='webapp_user_input') as db:
        dbcursor = db.cursor()
        dbcursor.execute('SELECT * FROM speed_estimation_inputs')
        sql_data = dbcursor.fetchall()
    return sql_data


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
    sqldata = sql_query()
    return render_template("estimator_data.html", sql_data=sqldata)


if __name__ == "__main__":
    app.run(debug=True)
