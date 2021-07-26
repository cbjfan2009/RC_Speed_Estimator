import mysql.connector

db = mysql.connector.connect(
   host='localhost',
   user='devMatt',
   password='D3V3l0pm3ntS3rV3rcbjfan2009',
   database='webapp_user_input'
   )

dbcursor = db.cursor()

#class users(db.Model):
#   id = db.Column('user', db.Integer, primary_key = True)
#   motkv = db.Column(db.Float)
#   batvolt = db.Column(db.Float)
#   pinion = db.Column(db.Float)
#   spur = db.Column(db.Float)
#   fgratio = db.Column(db.Float)
#   wheeldiam = db.Column(db.Float)

#def __init__(self, user, motkv, batvolt, pinion, spur, fgratio, wheeldiam):
#   self.user = user
#   self.motkv = motkv
#   self.batvolt = batvolt
#   self.pinion = pinion
#   self.spur = spur
#   self.fgratio = fgratio
#   self.wheeldiam = wheeldiam


#use this type of syntax to insert new data into the table
#sql = "INSERT INTO tablename (column1name, column2name) VALUES (%s, %s)"
#val = ("column1", "column2")
#mycursor.execute(sql, val)

#sql = "INSERT INTO *TABLENAME* (--these are the SQL table column names-- User, Motor_kV, Batt_Volt, Pinion, Spur, Final_Ratio, Wheel_Rad) VALUES (%s, %s, %s, %s, %s, %s, %s)"
sql = "INSERT INTO speed_estimation_inputs (User, Motor_kV, Batt_Volt, Pinion, Spur, Final_Ratio, Wheel_Rad) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = [
   ('204.210.165.122', 2400, 16.8, 16, 54, 3.92, 2.5),
   ('204.210.165.123',3500, 12.6, 16, 54, 3.92, 2.5),
   ('204.210.165.124', 4200, 8.4, 12, 54, 3.92, 2.5)
]
#proves I am connected to the database
#dbcursor.execute('SHOW TABLES')
#for x in dbcursor:
#   print(x)

dbcursor.executemany(sql, val)

db = db.commit()




