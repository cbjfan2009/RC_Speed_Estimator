from flask import Flask, render_template, url_for, request, redirect
from math import pi
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import text

app = Flask(__name__)

#set DB for keeping track of motor spec's tested in speed estimator
#db_name = 'estimator_specs.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#db = SQLAlchemy(app)


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





if __name__ == "__main__":
    app.run(debug=True)
