from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_kv = request.form['motorkV']
        user_batteryVolt = request.form['batteryVolt']
        user_pinion = request.form['pinion']
        user_spur = request.form['spur']
        user_fgr = request.form['fgr']
        user_wheelradius = request.form['wheelradius']
        totalrpm = user_kv*user_batteryVolt
        speed = (totalrpm/((user_spur/user_pinion)*user_fgr)*user_wheelradius*(60/5280))
        return render_template("index.html", speed_display=speed)


    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)