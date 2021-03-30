from flask import Flask, render_template, url_for, request, redirect
from math import pi

app = Flask(__name__)


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
        speed = (totalrpm / ((user_spur / user_pinion) * user_fgr) * (wheel_circum/12) * (60 / 5280))
        return render_template("index.html", speed_display=speed)

    else:
        return render_template("index.html")

@app.route('/hiddenpage')
def hiddenpage():
    return render_template("hiddenpage.html")



if __name__ == "__main__":
    app.run(debug=True)
